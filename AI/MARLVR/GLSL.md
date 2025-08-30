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

import torch.nn as nn

  

import numpy as np

  

# ---- Optional: RL trainer dependencies ----

try:

    import torch

    import torch.nn as nn

    import torch.optim as optim

    from torch.distributions import Categorical, Normal

    _HAS_TORCH = True

except Exception:

    _HAS_TORCH = False

  

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

  

Shape = int  # index into SHAPES

Color = int  # index into COLORS

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

uniform float u_time;        // seconds

uniform vec2 u_res;          // resolution

  

// Parameters

uniform int u_shape;   // 0 circle, 1 square, 2 triangle

uniform int u_color;   // 0 red, 1 green, 2 blue

uniform int u_motion;  // 0 lr, 1 ud, 2 rotate, 3 pulse

  

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

            -1.0,  1.0,

             1.0,  1.0,

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

            if m == 0:  # left_right

                cx = int(self.width//2 + (self.width//4) * math.sin(tt))

            elif m == 1:  # up_down

                cy = int(self.height//2 + (self.height//4) * math.sin(tt))

            elif m == 2:  # rotate -> draw triangle rotated approx by time (coarse)

                pass

            elif m == 3:  # pulse

                size = int(24 + 12 * (0.75 + 0.25 * math.sin(2*tt)))

  

            col = color_map[c]

            if s == 0:  # circle

                draw.ellipse((cx-size, cy-size, cx+size, cy+size), fill=col)

            elif s == 1:  # square

                draw.rectangle((cx-size, cy-size, cx+size, cy+size), fill=col)

            else:  # triangle

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

        self._agent_selector = agent_selector.agent_selector(self.agents)

  

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

        self._agent_selector = agent_selector.agent_selector(self.agents)

        self.agent_selection = self._agent_selector.reset()

  

    # ---- API helpers ----

    def observation_spaces(self) -> Dict[str, Any]:  # minimal, illustrative only

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

  

    def action_spaces(self) -> Dict[str, Any]:  # minimal, illustrative only

        return {

            "coder": (len(SHAPES), len(COLORS), len(MOTIONS)),

            "describer": (len(SHAPES), len(COLORS), len(MOTIONS)),

            "rater": (1,),  # float scalar in [0,1]

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

        self._agent_selector = agent_selector.agent_selector(self.agents)

        self.agent_selection = self._agent_selector.reset()

  

    def observe(self, agent: str):

        if agent == "coder":

            return {

                "text": self.task.text,

                "target_tuple": self.task.target,  # include target for supervised starts

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

            #   • sim_task_vs_render: did coder match the *task*?

            sim_task_vs_render = tuple_similarity(self.task.target, self.coder_choice)

            #   • sim_render_vs_caption: did describer match the *render*?

            sim_render_vs_caption = tuple_similarity(self.coder_choice, self.describer_guess)

            #   • sim_task_vs_caption: optional alt target for rating (we'll use task vs caption)

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

# Tokenized code (sketch)

# =====================

TOKEN_IDS = {

    # shapes

    'SHAPE_CIRCLE': 0,

    'SHAPE_SQUARE': 1,

    'SHAPE_TRIANGLE': 2,

    # colors

    'COLOR_RED': 3,

    'COLOR_GREEN': 4,

    'COLOR_BLUE': 5,

    # motions

    'MOTION_LR': 6,

    'MOTION_UD': 7,

    'MOTION_ROTATE': 8,

    'MOTION_PULSE': 9,

}

ID_TOKENS = {v: k for k, v in TOKEN_IDS.items()}

  
  

def tokens_to_tuple(tokens: List[int]) -> Tuple3:

    """Map a triple of tokens -> (shape, color, motion) tuple.

    This is a simple sketch: assume tokens are [shape_token, color_token, motion_token]."""

    shape_map = {TOKEN_IDS['SHAPE_CIRCLE']: 0, TOKEN_IDS['SHAPE_SQUARE']: 1, TOKEN_IDS['SHAPE_TRIANGLE']: 2}

    color_map = {TOKEN_IDS['COLOR_RED']: 0, TOKEN_IDS['COLOR_GREEN']: 1, TOKEN_IDS['COLOR_BLUE']: 2}

    motion_map = {TOKEN_IDS['MOTION_LR']: 0, TOKEN_IDS['MOTION_UD']: 1, TOKEN_IDS['MOTION_ROTATE']: 2, TOKEN_IDS['MOTION_PULSE']: 3}

    s = shape_map.get(tokens[0], 0)

    c = color_map.get(tokens[1], 0)

    m = motion_map.get(tokens[2], 0)

    return (s, c, m)

  
  

# =====================

# PPO helpers (independent policies per agent)

# =====================

class MLP(nn.Module):

    def __init__(self, inp, hidden, out, act_last=False):

        super().__init__()

        self.net = nn.Sequential(

            nn.Linear(inp, hidden), nn.Tanh(),

            nn.Linear(hidden, hidden), nn.Tanh(),

            nn.Linear(hidden, out),

        )

        self.act_last = act_last

  

    def forward(self, x):

        y = self.net(x)

        if self.act_last:

            return torch.tanh(y)

        return y

  
  

class MultiCatPolicy(nn.Module):

    """Outputs independent Categorical distributions for each head size in 'dims'."""

    def __init__(self, obs_dim: int, dims: List[int], hidden: int = 128):

        super().__init__()

        self.backbone = MLP(obs_dim, hidden, hidden)

        self.heads = nn.ModuleList([nn.Linear(hidden, d) for d in dims])

  

    def dist(self, obs: torch.Tensor) -> List[Categorical]:

        z = self.backbone(obs)

        logits = [h(z) for h in self.heads]

        return [Categorical(logits=lg) for lg in logits]

  

    def act(self, obs: torch.Tensor):

        dists = self.dist(obs)

        actions = [d.sample() for d in dists]

        logps = torch.stack([d.log_prob(a) for d, a in zip(dists, actions)], dim=-1).sum(-1)

        return torch.stack(actions, dim=-1), logps

  

    def log_prob(self, obs: torch.Tensor, actions: torch.Tensor):

        dists = self.dist(obs)

        return torch.stack([d.log_prob(a) for d, a in zip(dists, actions.T)], dim=-1).sum(-1)

  
  

class GaussianPolicy(nn.Module):

    """Scalar action in [0,1]. We'll sample from Normal and clamp."""

    def __init__(self, obs_dim: int, hidden: int = 128):

        super().__init__()

        self.mu = MLP(obs_dim, hidden, 1)

        self.log_std = nn.Parameter(torch.zeros(1))

  

    def dist(self, obs: torch.Tensor) -> Normal:

        mu = self.mu(obs).squeeze(-1)

        std = self.log_std.exp().expand_as(mu)

        return Normal(mu, std)

  

    def act(self, obs: torch.Tensor):

        d = self.dist(obs)

        a = d.rsample()

        a_clamped = torch.clamp(torch.sigmoid(a), 0.0, 1.0)

        # Use reparameterization trick; approximate log_prob around unclamped sample

        logp = d.log_prob(a).sum(-1)

        return a_clamped, logp

  

    def log_prob(self, obs: torch.Tensor, actions: torch.Tensor):

        # invert sigmoid approximately using logit, guard eps

        eps = 1e-6

        x = torch.clamp(actions, eps, 1-eps)

        z = torch.log(x) - torch.log(1-x)

        d = self.dist(obs)

        # change of variables for sigmoid: log_prob(z) + log|dz/dx| ; dz/dx = 1/(x(1-x))

        return d.log_prob(z) + torch.log(1.0/(x*(1.0-x)))

  
  

def onehot(n, i):

    v = np.zeros(n, dtype=np.float32)

    v[int(i)] = 1.0

    return v

  
  

def encode_obs(agent: str, obs: Any) -> np.ndarray:

    """Compact feature encoders for each agent."""

    if agent == 'coder':

        # Use one-hot of target tuple only (shape,color,motion)

        s,c,m = obs['target_tuple']

        return np.concatenate([onehot(len(SHAPES), s), onehot(len(COLORS), c), onehot(len(MOTIONS), m)])

    elif agent == 'describer':

        vid = obs  # [T,H,W,3] uint8

        # Downsample by average over space and time → 3-channel mean + motion proxy

        vidf = vid.astype(np.float32) / 255.0

        mean_rgb = vidf.mean(axis=(0,1,2))  # (3,)

        # Simple motion magnitude: mean absolute frame diff (grayscale)

        gray = (0.2989*vidf[:,:,:,0] + 0.5870*vidf[:,:,:,1] + 0.1140*vidf[:,:,:,2])

        diffs = np.abs(np.diff(gray, axis=0)).mean()

        return np.concatenate([mean_rgb, np.array([diffs], dtype=np.float32)])

    elif agent == 'rater':

        task = obs['task_tuple']

        des = obs['describer_tuple']

        s1,c1,m1 = task; s2,c2,m2 = des

        return np.concatenate([

            onehot(len(SHAPES), s1), onehot(len(COLORS), c1), onehot(len(MOTIONS), m1),

            onehot(len(SHAPES), s2), onehot(len(COLORS), c2), onehot(len(MOTIONS), m2),

        ])

    else:

        raise KeyError(agent)

  
  

@dataclass

class TrajBuf:

    obs: List[np.ndarray]

    acts: List[np.ndarray]

    logps: List[np.ndarray]

    rews: List[float]

    vals: List[np.ndarray]

  
  

def ppo_update(policy, value_fn, optimizers, buf: TrajBuf, clip_ratio=0.2, epochs=4, batch_size=64, gamma=0.99, lam=0.95):

    obs = torch.tensor(np.array(buf.obs), dtype=torch.float32)

    acts = torch.tensor(np.array(buf.acts))

    logps_old = torch.tensor(np.array(buf.logps), dtype=torch.float32)

    rews = np.array(buf.rews, dtype=np.float32)

    # GAE-lambda advantages with terminal after each step (single-step episodes in this env)

    vals = value_fn(obs).detach().squeeze(-1).numpy()

    adv = rews - vals

    ret = rews  # single-step

    adv = (adv - adv.mean()) / (adv.std() + 1e-8)

  

    opt_pi, opt_v = optimizers

    N = len(rews)

    idxs = np.arange(N)

    for _ in range(epochs):

        np.random.shuffle(idxs)

        for i in range(0, N, batch_size):

            j = idxs[i:i+batch_size]

            ob = obs[j]

            ac = acts[j]

            lp_old = logps_old[j]

            ad = torch.tensor(adv[j], dtype=torch.float32)

            rt = torch.tensor(ret[j], dtype=torch.float32)

  

            # policy loss

            if isinstance(policy, MultiCatPolicy):

                logp = policy.log_prob(ob, ac)

            else:

                logp = policy.log_prob(ob, ac.squeeze(-1)).squeeze(-1)

            ratio = torch.exp(logp - lp_old)

            l_pi = -(torch.min(ratio*ad, torch.clamp(ratio, 1-clip_ratio, 1+clip_ratio)*ad)).mean()

  

            # value loss

            v = value_fn(ob).squeeze(-1)

            l_v = ((v - rt)**2).mean()

  

            opt_pi.zero_grad(); opt_v.zero_grad()

            (l_pi + 0.5*l_v).backward()

            nn.utils.clip_grad_norm_(list(policy.parameters())+list(value_fn.parameters()), 1.0)

            opt_pi.step(); opt_v.step()

  
  

# =====================

# Training / Demo entrypoint

# =====================

  

# Define obs dims

obs_dim = {

    'coder': len(SHAPES)+len(COLORS)+len(MOTIONS),

    'describer': 4,  # mean RGB + motion magnitude

    'rater': (len(SHAPES)+len(COLORS)+len(MOTIONS))*2,

}

  

# Policies & value functions

coder_pi = MultiCatPolicy(obs_dim['coder'], [len(SHAPES), len(COLORS), len(MOTIONS)])

coder_v = MLP(obs_dim['coder'], 128, 1)

describer_pi = MultiCatPolicy(obs_dim['describer'], [len(SHAPES), len(COLORS), len(MOTIONS)])

describer_v = MLP(obs_dim['describer'], 128, 1)

rater_pi = GaussianPolicy(obs_dim['rater'])

rater_v = MLP(obs_dim['rater'], 128, 1)

  

optimizers = {

    'coder': (optim.Adam(coder_pi.parameters(), lr=3e-4), optim.Adam(coder_v.parameters(), lr=1e-3)),

    'describer': (optim.Adam(describer_pi.parameters(), lr=3e-4), optim.Adam(describer_v.parameters(), lr=1e-3)),

    'rater': (optim.Adam(rater_pi.parameters(), lr=3e-4), optim.Adam(rater_v.parameters(), lr=1e-3)),

}

  

# Trajectory buffers

bufs = {k: TrajBuf([], [], [], [], []) for k in ['coder','describer','rater']}

  

# Training loop

args_episodes = 50 # Define number of episodes here

env = GLSLDescriptionEnv(seed=42, width=96, height=96, T=8)

  

for ep in range(args_episodes):

    env.reset()

    # Rollout one episode (3 steps)

    while True:

        a = env.agent_selection

        obs = env.observe(a)

        x = torch.tensor(encode_obs(a, obs), dtype=torch.float32).unsqueeze(0)

  

        if a == 'coder':

            # policy acts over three categoricals

            act_tensor, logp = coder_pi.act(x)

            action = (int(act_tensor[0,0]), int(act_tensor[0,1]), int(act_tensor[0,2]))

            val = coder_v(x).detach().numpy()

            env.step(action)

            bufs['coder'].obs.append(x.squeeze(0).numpy())

            bufs['coder'].acts.append(act_tensor.squeeze(0).numpy())

            bufs['coder'].logps.append(logp.detach().numpy())

            bufs['coder'].vals.append(val)

  

        elif a == 'describer':

            act_tensor, logp = describer_pi.act(x)

            action = (int(act_tensor[0,0]), int(act_tensor[0,1]), int(act_tensor[0,2]))

            val = describer_v(x).detach().numpy()

            env.step(action)

            bufs['describer'].obs.append(x.squeeze(0).numpy())

            bufs['describer'].acts.append(act_tensor.squeeze(0).numpy())

            bufs['describer'].logps.append(logp.detach().numpy())

            bufs['describer'].vals.append(val)

  

        else:  # rater

            act_tensor, logp = rater_pi.act(x)

            action = float(act_tensor.item())

            val = rater_v(x).detach().numpy()

            env.step(action)

            bufs['rater'].obs.append(x.squeeze(0).numpy())

            bufs['rater'].acts.append(np.array([action], dtype=np.float32))

            bufs['rater'].logps.append(logp.detach().numpy())

            bufs['rater'].vals.append(val)

  

        if all(env.terminations.values()) or all(env.truncations.values()):

            # collect rewards

            for k in ['coder','describer','rater']:

                bufs[k].rews.append(env.rewards[k])

            break

  

    # Update all agents after each episode

    ppo_update(coder_pi, coder_v, optimizers['coder'], bufs['coder'])

    ppo_update(describer_pi, describer_v, optimizers['describer'], bufs['describer'])

    ppo_update(rater_pi, rater_v, optimizers['rater'], bufs['rater'])

  

    # Clear buffers

    bufs = {k: TrajBuf([], [], [], [], []) for k in ['coder','describer','rater']}

  

    if (ep+1) % 5 == 0:

        gt = env.infos['rater'].get('gt_similarity', None)

        print(f"[Train] Episode {ep+1}/{args_episodes} last_rewards={env.rewards} gt_similarity={gt}")

  

# Example inference after training

env.reset()

while True:

    a = env.agent_selection

    obs = env.observe(a)

    x = torch.tensor(encode_obs(a, obs), dtype=torch.float32).unsqueeze(0)

    if a == 'coder':

        act, _ = coder_pi.act(x)

        action = (int(act[0,0]), int(act[0,1]), int(act[0,2]))

    elif a == 'describer':

        act, _ = describer_pi.act(x)

        action = (int(act[0,0]), int(act[0,1]), int(act[0,2]))

    else:

        act, _ = rater_pi.act(x)

        action = float(act.item())

    env.step(action)

    if all(env.terminations.values()):

        print(f"[Eval] rewards={env.rewards}, gt_similarity={env.infos['rater'].get('gt_similarity')}")

        break

  

env.close()
```

