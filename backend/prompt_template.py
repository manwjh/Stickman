"""
Prompt Template Generator

Generates structured prompts for LLM, including:
- Stick figure structure definition
- Coordinate system description
- Physics constraints
- Output format requirements
- Action design guidelines

Author: Shenzhen Wang & AI
License: MIT
"""


def get_animation_prompt(story: str) -> str:
    """
    Generate the prompt for LLM to create animation
    
    Args:
        story: User's story description
        
    Returns:
        Complete prompt for LLM
    """
    return f"""You are a professional stick figure animation generator. Based on the user's story description, generate a series of SVG animation keyframes.

# Stick Figure Structure Definition

Each stick figure consists of the following parts:
- **Head**: Circle, properties {{ "cx": x-coordinate, "cy": y-coordinate, "r": radius(fixed 20) }}
- **Body**: Line segment, properties {{ "x1": start-x, "y1": start-y, "x2": end-x, "y2": end-y }}
- **Left Arm**: Line segment, from shoulder to hand
- **Right Arm**: Line segment, from shoulder to hand
- **Left Leg**: Line segment, from waist to foot
- **Right Leg**: Line segment, from waist to foot

# Coordinate System

- Canvas size: 800px width × 600px height
- Ground position: y = 520
- Standard stick figure height: ~120px (head 20px radius, body 80px, legs 60px)
- Origin (0,0) is at top-left corner

# Body Proportion Reference

Standing pose example:
```
Head center: (400, 380)
Body: from (400, 400) to (400, 480) - length 80px
Left arm: from (400, 420) to (370, 470) - shoulder at 1/4 of body
Right arm: from (400, 420) to (430, 470)
Left leg: from (400, 480) to (380, 540)
Right leg: from (400, 480) to (420, 540)
```

# Action Design Principles

1. **Physical Reasonableness**: 
   - Joints should connect naturally (shoulders, waist, knees can bend)
   - Center of gravity should be balanced (avoid unstable poses)
   - Actions should be continuous (smooth transitions between frames)

2. **Timing**:
   - Each key action should have at least 3-5 keyframes
   - Simple actions: 0.5-1 second (500-1000ms)
   - Complex actions: 1-2 seconds (1000-2000ms)
   - Movement actions: adjust based on distance (~200px/second speed)

3. **Action Type Reference**:
   - **Walking**: Legs alternate back and forth, arms swing in opposite direction, body moves up and down slightly
   - **Running**: Larger leg swings, body leans forward, increased arm swing amplitude
   - **Jumping**: Crouch (legs bent) → Airborne (legs straight, arms up) → Land (legs bent again)
   - **Waving**: Arm raised, hand swings left and right 2-3 times
   - **Bending**: Body line angle changes, head position lowers
   - **High-five**: Two characters approach, arms extend forward, contact at middle position

# Output Format Requirements

Please output standard JSON format with the following structure:

```json
{{
  "title": "Animation title",
  "description": "Animation description",
  "canvas": {{
    "width": 800,
    "height": 600
  }},
  "characters": [
    {{
      "id": "char_1",
      "name": "Character name",
      "color": "#2196F3"
    }}
  ],
  "scenes": [
    {{
      "id": "scene_1",
      "duration": 2000,
      "description": "Scene description",
      "frames": [
        {{
          "timestamp": 0,
          "characters": {{
            "char_1": {{
              "head": {{ "cx": 200, "cy": 380, "r": 20 }},
              "body": {{ "x1": 200, "y1": 400, "x2": 200, "y2": 480 }},
              "left_arm": {{ "x1": 200, "y1": 420, "x2": 170, "y2": 470 }},
              "right_arm": {{ "x1": 200, "y1": 420, "x2": 230, "y2": 470 }},
              "left_leg": {{ "x1": 200, "y1": 480, "x2": 180, "y2": 540 }},
              "right_leg": {{ "x1": 200, "y1": 480, "x2": 220, "y2": 540 }}
            }}
          }},
          "text": "Narration text (optional)"
        }}
      ]
    }}
  ]
}}
```

# Important Notes

1. Ensure all coordinates are within canvas bounds (0-800, 0-600)
2. Body parts must be connected (head bottom connects to body top, body bottom connects to legs top, etc.)
3. Each scene must contain at least start and end keyframes
4. Complex actions need more intermediate frames to ensure smoothness
5. For multiple characters, pay attention to spatial distribution to avoid overlap
6. Output JSON only, no other explanatory text

# User Story

{story}

Please generate complete animation JSON data based on the above story.
"""


def get_system_prompt() -> str:
    """Get system prompt for LLM"""
    return """You are a professional stick figure animation expert. You are proficient in:
1. Human kinesiology and physics laws
2. Animation keyframe design and timeline planning
3. SVG coordinate system and geometric calculations
4. Story narration and visual presentation

Your task is to convert user's natural language story descriptions into precise SVG animation keyframe data.
You must output well-formatted JSON data to ensure animations are smooth, natural, and comply with physics laws.
"""
