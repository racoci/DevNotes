Awesome idea, Escher — here’s a minimal-but-complete scaffold you can run and then extend into full MARL training.

I put a full working example in the canvas: it defines a **PettingZoo** multi-agent environment with three agents:

* **coder** chooses `(shape, color, motion)` → we synthesize a **GLSL fragment shader** from a template and render a short clip (off-screen, via `moderngl`; falls back to Pillow if OpenGL isn’t available).
* **describer** watches the rendered frames and outputs its own `(shape, color, motion)` “caption”.
* **rater** gets both descriptions and outputs a similarity score in `[0,1]`.

Rewards:

* coder: similarity(task, render)
* describer: similarity(render, caption)
* rater: 1 − (rating − similarity(task, caption))²

What you can do next (quick roadmap):

1. Swap the symbolic captions for natural language (map tuples to text templates, then train a video→text model for describer).
2. Let coder output **actual code tokens**: grow the template family or add a tiny DSL that compiles to GLSL.
3. Train with PPO/A2C per agent (parallel envs); add curriculum (start with one attribute, then two, etc.).
4. Replace the rater with a learned comparator (e.g., contrastive text encoders) and give it its own observation/reward shaping.

Run tips:

* `pip install pettingzoo gymnasium numpy moderngl Pillow`
* If `moderngl` can’t create a context on your machine, it will automatically fall back to Pillow-based rasterization.
* Start by running the `__main__` block to see three random agents interact and print rewards; then drop in your RL learners.

If you want, I can add:

* a tiny PPO trainer loop for each agent (with independent policies),
* a tokenized code action space + grammar checks,
* or a batched renderer that produces frame tensors on GPU.

Canvas:
```python
"""
Multi-Agent Reinforcement Learning environment where:
  • Agent "coder" (A1) generates GLSL fragment shader code from a text description.
  • The shader is rendered into a short video (frames over time).
  • Agent "describer" (A2) looks at the rendered video and outputs a textual description.
  • Agent "rater" (A3) compares the task description with A2's description and outputs a similarity rating.

We implement this as a PettingZoo AEC environment with three agents.

Design choices (kept minimal to run locally):
  1) Action spaces
     - A1 (coder): instead of free-form code synthesis, we parameterize a small family of GLSL templates
       with discrete choices over shape ∈ {circle, square, triangle}, color ∈ {red, green, blue},
       and motion ∈ {left_right, up_down, rotate, pulse}. Agent A1 picks (shape, color, motion),
       and the environment assembles the full fragment shader source.
     - A2 (describer): outputs its own tuple (shape, color, motion) as a symbolic "caption".
       This is a compact stand-in for natural language (you can map to text strings if you prefer).
     - A3 (rater): outputs a scalar rating in [0, 1] estimating the similarity between the task
       tuple and A2's predicted tuple.

  2) Observations
     - A1 observes the task description: a string + (optionally) the target tuple.
       (We pass the symbolic tuple in obs for simplicity and to allow supervised baselines.)
     - A2 observes the T video frames (downsampled) as a tensor float32 [T, H, W, 3].
     - A3 observes the pair of tuples (task vs. A2 prediction) as one-hot vectors, plus a textual summary string.

  3) Rewards
     - A1 (coder): rewarded by the *ground-truth* similarity between the task tuple and the actually rendered
       tuple chosen by A1. (i.e., did the code render what was asked?)
     - A2 (describer): rewarded by the ground-truth similarity between the rendered tuple (chosen by A1) and
       its predicted tuple. (i.e., did the caption match the video?)
     - A3 (rater): rewarded by how close its rating is to the ground-truth similarity (L2 error).

  4) Rendering
     - Uses moderngl to compile a minimal vertex+fragment shader and render off-screen into frames.
       Uniforms control shape/color and motion over time.
       If moderngl is missing, we automatically fall back to a NumPy/Pillow rasterizer of simple shapes.

  5) Dependencies (install as needed):
       pip install pettingzoo gymnasium numpy moderngl Pillow

  6) Notes
     - This file is self-contained to *demonstrate* the environment and random agents interacting with it.
       Replace the random policies with your RL algorithms (e.g., PPO, A2C) per agent.
     - Extending to natural-language is straightforward:
         • Map tuples <shape,color,motion> to/from text via templates.
         • Replace A2 with a video->text model.
         • Replace A3 with a learned textual similarity model.
"""
from __future__ import annotations
import math
import os
import io
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any

import numpy as np

try:
    import moderngl
    _HAS_MODERNGL = True
except Exception:
    _HAS_MODERNGL = False

from PIL import Image, ImageDraw

# --- PettingZoo AEC skeleton ---
try:
    from pettingzoo.utils import agent_selector
    from pettingzoo.utils.env import AECEnv
except Exception as e:
    raise RuntimeError("Please install pettingzoo: pip install pettingzoo") from e


# =====================
# Utility: Tuples & Vocab
# =====================
SHAPES = ["circle", "square", "triangle"]
COLORS = ["red", "green", "blue"]
MOTIONS = ["left_right", "up_down", "rotate", "pulse"]

Shape = int  # index into SHAPES
Color = int  # index into COLORS
Motion = int # index into MOTIONS

Tuple3 = Tuple[Shape, Color, Motion]


def tuple_to_text(t: Tuple3) -> str:
    s, c, m = t
    return f"{COLORS[c]} {SHAPES[s]} {MOTIONS[m].replace('_',' ')}"


def tuple_similarity(a: Tuple3, b: Tuple3) -> float:
    """Simple 0..1 similarity as average of matches across 3 categorical attributes."""
    matches = int(a[0] == b[0]) + int(a[1] == b[1]) + int(a[2] == b[2])
    return matches / 3.0


# =====================
# Task generator
# =====================
@dataclass
class Task:
    target: Tuple3
    text: str


def sample_task(rng: np.random.Generator) -> Task:
    t = (rng.integers(0, len(SHAPES)),
         rng.integers(0, len(COLORS)),
         rng.integers(0, len(MOTIONS)))
    return Task(target=t, text=tuple_to_text(t))


# =====================
# GLSL rendering
# =====================
VERTEX_SHADER = """
#version 330
in vec2 in_vert;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
}
"""

FRAGMENT_TEMPLATE = """
#version 330
out vec4 f_color;
uniform float u_time;        // seconds
uniform vec2 u_res;          // resolution

// Parameters
uniform int u_shape;   // 0 circle, 1 square, 2 triangle
uniform int u_color;   // 0 red, 1 green, 2 blue
uniform int u_motion;  // 0 lr, 1 ud, 2 rotate, 3 pulse

float sdCircle(vec2 p, float r){ return length(p) - r; }
float sdBox(vec2 p, vec2 b){ vec2 d = abs(p) - b; return length(max(d,0.0)) + min(max(d.x,d.y),0.0); }

float sdTriangle(vec2 p){
    // Equilateral centered at origin, side ~1.732 (height=1.5 approx)
    const float k = sqrt(3.0);
    p.x = abs(p.x) - 0.5;
    p.y = p.y + 0.3;
    if (p.x + k*p.y > 0.0) p = vec2(p.x - k*p.y, -k*p.x - p.y) / 2.0;
    p.x -= clamp(p.x, -1.0, 0.0);
    return -length(p) * sign(p.y);
}

float shapeSDF(vec2 p){
    if (u_shape == 0) return sdCircle(p, 0.25);
    if (u_shape == 1) return sdBox(p, vec2(0.25));
    return sdTriangle(p);
}

vec3 pickColor(){
    if (u_color == 0) return vec3(1.0, 0.1, 0.1);
    if (u_color == 1) return vec3(0.1, 1.0, 0.1);
    return vec3(0.1, 0.1, 1.0);
}

void main() {
    vec2 uv = (gl_FragCoord.xy / u_res) * 2.0 - 1.0; // [-1,1]
    uv.x *= u_res.x / u_res.y; // aspect correction

    // motion
    vec2 p = uv;
    if (u_motion == 0) {
        // left-right
        p.x -= 0.5 * sin(u_time);
    } else if (u_motion == 1) {
        // up-down
        p.y -= 0.5 * sin(u_time);
    } else if (u_motion == 2) {
        // rotate around origin
        float a = u_time;
        mat2 R = mat2(cos(a), -sin(a), sin(a), cos(a));
        p = R * p;
    } else if (u_motion == 3) {
        // pulse size
        p *= 0.5 + 0.5 * (0.75 + 0.25 * sin(u_time*2.0));
    }

    float d = shapeSDF(p);
    float edge = 0.005; // thickness for anti-aliased edge
    float mask = smoothstep(edge, -edge, d);

    vec3 col = mix(vec3(0.0), pickColor(), mask);
    f_color = vec4(col, 1.0);
}
"""


class GLSLRenderer:
    def __init__(self, width: int = 128, height: int = 128):
        self.width = width
        self.height = height
        self.ctx = None
        self.fbo = None
        self.quad = None
        self.prog = None

        if _HAS_MODERNGL:
            self._init_mgl()

    def _init_mgl(self):
        self.ctx = moderngl.create_standalone_context()
        self.fbo = self.ctx.simple_framebuffer((self.width, self.height))
        self.fbo.use()
        # Fullscreen quad
        vertices = np.array([
            -1.0, -1.0,
             1.0, -1.0,
            -1.0,  1.0,
             1.0,  1.0,
        ], dtype='f4')
        self.quad = self.ctx.buffer(vertices.tobytes())
        vao_content = [(self.quad, '2f', 'in_vert')]
        self.vao = self.ctx.vertex_array(self._compile_program(), vao_content)

    def _compile_program(self):
        return self.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_TEMPLATE)

    def render_frames(self, tpl: Tuple3, T: int = 12) -> np.ndarray:
        """Return frames as uint8 array [T, H, W, 3]."""
        if _HAS_MODERNGL:
            return self._render_mgl(tpl, T)
        else:
            return self._render_pillow(tpl, T)

    def _render_mgl(self, tpl: Tuple3, T: int) -> np.ndarray:
        s, c, m = tpl
        frames = []
        # Recreate program to ensure fresh uniforms after context loss
        self.prog = self._compile_program()
        vao_content = [(self.quad, '2f', 'in_vert')]
        self.vao = self.ctx.vertex_array(self.prog, vao_content)
        self.prog['u_res'].value = (self.width, self.height)
        self.prog['u_shape'].value = int(s)
        self.prog['u_color'].value = int(c)
        self.prog['u_motion'].value = int(m)

        for t in range(T):
            u_time = float(t) * 0.25
            self.prog['u_time'].value = u_time
            self.fbo.clear(0.0, 0.0, 0.0, 1.0)
            self.vao.render(mode=moderngl.TRIANGLE_STRIP)
            data = self.fbo.read(components=3, alignment=1)
            img = np.frombuffer(data, dtype=np.uint8).reshape((self.height, self.width, 3))
            frames.append(img)
        return np.stack(frames, axis=0)

    def _render_pillow(self, tpl: Tuple3, T: int) -> np.ndarray:
        # Fallback: draw simple shapes that approximately match the motions.
        s, c, m = tpl
        color_map = [(255, 20, 20), (20, 255, 20), (20, 20, 255)]
        frames = []
        for t in range(T):
            img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
            draw = ImageDraw.Draw(img)
            tt = t * 0.25
            cx, cy = self.width//2, self.height//2
            size = 32
            if m == 0:  # left_right
                cx = int(self.width//2 + (self.width//4) * math.sin(tt))
            elif m == 1:  # up_down
                cy = int(self.height//2 + (self.height//4) * math.sin(tt))
            elif m == 2:  # rotate -> draw triangle rotated approx by time (coarse)
                pass
            elif m == 3:  # pulse
                size = int(24 + 12 * (0.75 + 0.25 * math.sin(2*tt)))

            col = color_map[c]
            if s == 0:  # circle
                draw.ellipse((cx-size, cy-size, cx+size, cy+size), fill=col)
            elif s == 1:  # square
                draw.rectangle((cx-size, cy-size, cx+size, cy+size), fill=col)
            else:  # triangle
                ang = tt if m == 2 else 0.0
                r = size
                pts = []
                for k in range(3):
                    a = ang + 2*math.pi*k/3
                    px = cx + int(r * math.cos(a))
                    py = cy + int(r * math.sin(a))
                    pts.append((px, py))
                draw.polygon(pts, fill=col)
            frames.append(np.array(img, dtype=np.uint8))
        return np.stack(frames, axis=0)


# =====================
# AEC Environment
# =====================
class GLSLDescriptionEnv(AECEnv):
    metadata = {"name": "glsl_description_v0"}

    def __init__(self, seed: Optional[int] = None, width: int = 128, height: int = 128, T: int = 12):
        super().__init__()
        self.width = width
        self.height = height
        self.T = T
        self.rng = np.random.default_rng(seed)
        self.agents = ["coder", "describer", "rater"]
        self.possible_agents = list(self.agents)
        self._agent_selector = agent_selector(self.agents)

        self.task: Optional[Task] = None
        self.coder_choice: Optional[Tuple3] = None
        self.frames: Optional[np.ndarray] = None
        self.describer_guess: Optional[Tuple3] = None

        self._renderer = GLSLRenderer(width, height)

        # bookkeeping for AEC
        self.has_reset = False
        self.rewards = {a: 0.0 for a in self.agents}
        self._cumulative_rewards = {a: 0.0 for a in self.agents}
        self.terminations = {a: False for a in self.agents}
        self.truncations = {a: False for a in self.agents}
        self.infos = {a: {} for a in self.agents}
        self.agent_selection = None

    # ---- API helpers ----
    def observation_spaces(self) -> Dict[str, Any]:  # minimal, illustrative only
        return {
            "coder": {
                "text": "str: task description",
                "onehot": (len(SHAPES), len(COLORS), len(MOTIONS)),
            },
            "describer": {
                "video": (self.T, self.height, self.width, 3),
            },
            "rater": {
                "pair_onehot": (len(SHAPES), len(COLORS), len(MOTIONS))*2,
            },
        }

    def action_spaces(self) -> Dict[str, Any]:  # minimal, illustrative only
        return {
            "coder": (len(SHAPES), len(COLORS), len(MOTIONS)),
            "describer": (len(SHAPES), len(COLORS), len(MOTIONS)),
            "rater": (1,),  # float scalar in [0,1]
        }

    # ---- AEC core ----
    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.has_reset = True
        self.task = sample_task(self.rng)
        self.coder_choice = None
        self.frames = None
        self.describer_guess = None

        self.rewards = {a: 0.0 for a in self.agents}
        self._cumulative_rewards = {a: 0.0 for a in self.agents}
        self.terminations = {a: False for a in self.agents}
        self.truncations = {a: False for a in self.agents}
        self.infos = {a: {} for a in self.agents}
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()

    def observe(self, agent: str):
        if agent == "coder":
            return {
                "text": self.task.text,
                "target_tuple": self.task.target,  # include target for supervised starts
            }
        elif agent == "describer":
            if self.frames is None:
                # Blank frames if coder hasn't acted yet
                return np.zeros((self.T, self.height, self.width, 3), dtype=np.uint8)
            return self.frames
        elif agent == "rater":
            des = self.describer_guess if self.describer_guess is not None else (0,0,0)
            return {
                "task_tuple": self.task.target,
                "describer_tuple": des,
            }
        else:
            raise KeyError(agent)

    def step(self, action):
        if not self.has_reset:
            raise RuntimeError("Call reset() before step().")
        agent = self.agent_selection

        if self.terminations[agent] or self.truncations[agent]:
            # If agent already terminated, skip
            self._was_done_step(action)
            return

        if agent == "coder":
            # Action: (shape, color, motion)
            s, c, m = action
            self.coder_choice = (int(s), int(c), int(m))
            # Assemble fragment shader and render frames
            self.frames = self._renderer.render_frames(self.coder_choice, self.T)
            # No reward yet; end coder's turn
            self._advance()

        elif agent == "describer":
            # Action: (shape, color, motion) as predicted caption
            s, c, m = action
            self.describer_guess = (int(s), int(c), int(m))
            self._advance()

        elif agent == "rater":
            # Action: scalar rating in [0,1]
            rating = float(action)
            rating = max(0.0, min(1.0, rating))

            # Compute ground-truth similarities
            #   • sim_task_vs_render: did coder match the *task*?
            sim_task_vs_render = tuple_similarity(self.task.target, self.coder_choice)
            #   • sim_render_vs_caption: did describer match the *render*?
            sim_render_vs_caption = tuple_similarity(self.coder_choice, self.describer_guess)
            #   • sim_task_vs_caption: optional alt target for rating (we'll use task vs caption)
            sim_task_vs_caption = tuple_similarity(self.task.target, self.describer_guess)

            # Rewards
            self.rewards["coder"] = sim_task_vs_render
            self.rewards["describer"] = sim_render_vs_caption
            # Rater tries to predict task vs caption similarity
            self.rewards["rater"] = 1.0 - (rating - sim_task_vs_caption)**2

            # Episode ends after rater acts
            for a in self.agents:
                self.terminations[a] = True

            self.infos["rater"]["gt_similarity"] = sim_task_vs_caption
            self._advance(final=True)
        else:
            raise KeyError(agent)

    def _advance(self, final: bool = False):
        # Accumulate rewards before switching
        for a in self.agents:
            self._cumulative_rewards[a] += self.rewards[a]
        if final:
            return
        self.agent_selection = self._agent_selector.next()

    def render(self):
        # For quick debugging: return the last frame
        if self.frames is None:
            return np.zeros((self.height, self.width, 3), dtype=np.uint8)
        return self.frames[-1]

    def close(self):
        pass


# =====================
# Demo: random policies
# =====================
if __name__ == "__main__":
    env = GLSLDescriptionEnv(seed=42, width=128, height=128, T=12)
    episodes = 3
    for ep in range(episodes):
        env.reset()
        done = False
        traj = []
        while True:
            a = env.agent_selection
            obs = env.observe(a)
            if a == "coder":
                action = (
                    np.random.randint(len(SHAPES)),
                    np.random.randint(len(COLORS)),
                    np.random.randint(len(MOTIONS)),
                )
            elif a == "describer":
                action = (
                    np.random.randint(len(SHAPES)),
                    np.random.randint(len(COLORS)),
                    np.random.randint(len(MOTIONS)),
                )
            else:  # rater
                action = np.random.rand()
            env.step(action)
            if all(env.terminations.values()) or all(env.truncations.values()):
                info = env.infos["rater"].get("gt_similarity", None)
                print(f"Episode {ep}: rewards={env.rewards}, gt_similarity={info}")
                break
    env.close()

```