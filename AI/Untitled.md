You are building a frontend Web App that visualizes personalities as interactive graph nodes using data from the **Personality Database (PDB) API**. Each node represents a fictional or real character and includes visual, interactive, and statistical features. This project integrates personality psychology, socionics theory, and real-time simulation logic.

### 🔗 API SOURCES

#### Base URLs:

- `https://api.personality-database.com/api/v1/`
    
- `https://api.personality-database.com/api/v2/`
    

#### API Endpoints:

1. **Get Detailed Profile**  
    **Endpoint:** `GET /api/v1/profile/{profile_id}`  
    **Returns:** Full profile details of a character, including:
    
    - `id`
        
    - `mbti_type` (e.g., "INTJ")
        
    - `category` (numeric ID, must be mapped to label)
        
    - `profile_image_url`
        
    - `related_subcat_link_info`
        
    - `mbti_profile`, etc.
        
2. **Get Profiles by MBTI Type**  
    **Endpoint:** `GET /api/v2/personalities/{mbti_id}/profiles`  
    **Optional Query Parameters:**
    
    - `category`: restrict results to a specific domain (e.g., Anime, Sports, etc.)
        
    - `limit`: limit number of results
        
    - `nextCursor`: for pagination
        

#### MBTI to ID Map:

```json
{
  "ISTJ": 1, "ESTJ": 2, "ISFJ": 3, "ESFJ": 4,
  "ESFP": 5, "ISFP": 6, "ESTP": 7, "ISTP": 8,
  "INFJ": 9, "ENFJ": 10, "INFP": 11, "ENFP": 12,
  "INTP": 13, "ENTP": 14, "INTJ": 15, "ENTJ": 16
}
```

---

### 🧠 Simulation Design (Inspired by ExAI Engine)

1. **Each node** (character) is an agent with:
    
    - MBTI type
        
    - category
        
    - image (crop to circle)
        
    - signals like: `signal`, `influence`, `mood`, `trust`, etc.
        
    - simulation parameters like update rate and response functions
        
2. **Each connection (link)** is enriched with:
    
    - Socionics relationship (based on MBTI types)
        
    - Calculated using Jungian code similarity or a precomputed lookup table
        
    - Weight, distance, dynamic variables like `intensity`, `trust delta`, etc.
        
3. **Dynamic Simulation Behavior:**
    
    - Users can define variables for nodes and edges.
        
    - Users define update functions (JavaScript or formula DSL).
        
    - Variables update each tick using functions of:
        
        - own state
            
        - neighbor states
            
        - relationship strength
            
        - Socionics type of the link.
            

---

### 🎨 UI Behavior

- Graph rendered using D3 or PixiJS over SVG/Canvas.
    
- **Node appearance**:
    
    - Character image cropped to circle
        
    - **Border color**: based on category
        
    - **Text color**: reflects signal or MBTI category
        
- **On hover**: show floating tooltip with:
    
    - MBTI
        
    - Category
        
    - Relationships
        
    - Influence/signal stats
        
- **On click**:
    
    - Show sidebar with:
        
        - Full profile data
            
        - Links to MBTI subtype, cognitive functions
            
        - Related characters
            

---

### 🌈 Socionics Relations (link classification)

Links should be **color-coded by Socionics intertype relationship**, using this semantic color scale (from most tense to most harmonious):

|Relation|Code|Hex Color|
|---|---|---|
|Conflict|0000|`#ff0000`|
|Supervision|0010|`#ff6600`|
|Quasi-identical|1110|`#ffa500`|
|Contrary|0111|`#ffcc00`|
|Activity|1000|`#ccff00`|
|Mirror|0110|`#99ff33`|
|Identity|1111|`#33cc33`|
|Semi-Duality|0101|`#3399ff`|
|Duality|0001|`#0066ff`|

Use MBTI comparison logic to determine relation:

- Convert MBTI to binary using Jungian dichotomies.
    
- Compare bits to determine relation type using known mappings.
    

---

### ⚙️ Advanced Simulation (ExAI-style)

You will include a **simulation configuration panel** that lets the user:

- Define new properties for nodes and edges (e.g., `trust`, `signal`, `influence`, `morale`)
    
- Define equations for how variables evolve (e.g.):
    
    ```js
    edge.weight = 0.5 * source.signal + 0.3 * target.signal;
    node.signal = node.signal + 0.01 * sum(incoming.weight) - 0.05 * node.signal;
    ```
    
- Optionally export/import simulation presets
    
- Allow simulation to pause/play and reset
    

---

### 🧪 Features

- Import character lists or categories
- Filter by MBTI or category
- Log interactions, evolution of relationships
- Memory/emotion/morality modules (from ExAI)
- Adjust rate of personality change