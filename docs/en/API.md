# API Documentation

[中文](../zh-CN/API.md) | English

This document describes the REST API endpoints provided by the AI Stick Figure Story Animator.

## Base URL

```
http://localhost:5001
```

## Authentication

Currently, the API does not require authentication. In production, consider implementing API keys or OAuth.

## Endpoints

### GET /

**Description**: Serves the main web interface

**Response**: HTML page

**Example**:
```bash
curl http://localhost:5001/
```

---

### POST /api/generate

**Description**: Generate animation from story description

**Request Body**:
```json
{
  "story": "A person walks in and waves hello"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "title": "Greeting Animation",
    "description": "A person walking and waving",
    "canvas": {
      "width": 800,
      "height": 600
    },
    "characters": [
      {
        "id": "char_1",
        "name": "Person",
        "color": "#2196F3"
      }
    ],
    "scenes": [
      {
        "id": "scene_1",
        "duration": 2000,
        "description": "Walking in",
        "frames": [
          {
            "timestamp": 0,
            "characters": {
              "char_1": {
                "head": {"cx": 200, "cy": 380, "r": 20},
                "body": {"x1": 200, "y1": 400, "x2": 200, "y2": 480},
                "left_arm": {"x1": 200, "y1": 420, "x2": 170, "y2": 470},
                "right_arm": {"x1": 200, "y1": 420, "x2": 230, "y2": 470},
                "left_leg": {"x1": 200, "y1": 480, "x2": 180, "y2": 540},
                "right_leg": {"x1": 200, "y1": 480, "x2": 220, "y2": 540}
              }
            },
            "text": ""
          }
        ]
      }
    ]
  },
  "message": "Animation generated successfully"
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "Error message"
}
```

**Status Codes**:
- `200` - Success
- `400` - Bad request (missing or invalid parameters)
- `500` - Server error

**Example**:
```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{"story": "A person walks in and waves hello"}'
```

**Python Example**:
```python
import requests

response = requests.post(
    'http://localhost:5001/api/generate',
    json={'story': 'A person walks in and waves hello'}
)

data = response.json()
if data['success']:
    animation = data['data']
    print(f"Generated animation: {animation['title']}")
else:
    print(f"Error: {data['message']}")
```

**JavaScript Example**:
```javascript
const response = await fetch('http://localhost:5001/api/generate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        story: 'A person walks in and waves hello'
    })
});

const data = await response.json();
if (data.success) {
    console.log('Animation:', data.data);
} else {
    console.error('Error:', data.message);
}
```

---

### GET /api/health

**Description**: Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "provider": "openai"
}
```

**Example**:
```bash
curl http://localhost:5001/api/health
```

---

## Data Structures

### Animation Data

```typescript
interface AnimationData {
  title: string;
  description: string;
  canvas: Canvas;
  characters: Character[];
  scenes: Scene[];
}

interface Canvas {
  width: number;  // Default: 800
  height: number; // Default: 600
}

interface Character {
  id: string;      // Unique identifier
  name: string;    // Character name
  color: string;   // Hex color code
}

interface Scene {
  id: string;
  duration: number;     // Duration in milliseconds
  description: string;
  frames: Frame[];
}

interface Frame {
  timestamp: number;    // Time in milliseconds from scene start
  characters: {
    [characterId: string]: StickFigure;
  };
  text?: string;        // Optional narration text
}

interface StickFigure {
  head: Circle;
  body: Line;
  left_arm: Line;
  right_arm: Line;
  left_leg: Line;
  right_leg: Line;
}

interface Circle {
  cx: number;  // Center X
  cy: number;  // Center Y
  r: number;   // Radius
}

interface Line {
  x1: number;  // Start X
  y1: number;  // Start Y
  x2: number;  // End X
  y2: number;  // End Y
}
```

### Error Response

```typescript
interface ErrorResponse {
  success: false;
  message: string;
}
```

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider:

- Rate limiting per IP address
- API key-based rate limiting
- Request queuing for expensive operations

## CORS

CORS is enabled for all origins in development. In production, configure specific allowed origins.

## Best Practices

1. **Validate Input**: Always validate story input before sending
2. **Handle Errors**: Check `success` field in response
3. **Set Timeouts**: Animation generation can take 5-15 seconds
4. **Cache Results**: Cache generated animations when possible
5. **Sanitize Output**: Validate animation data before rendering

## Example Integration

### React Component

```jsx
import React, { useState } from 'react';

function AnimationGenerator() {
  const [story, setStory] = useState('');
  const [loading, setLoading] = useState(false);
  const [animation, setAnimation] = useState(null);
  const [error, setError] = useState(null);

  const generateAnimation = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5001/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ story })
      });

      const data = await response.json();

      if (data.success) {
        setAnimation(data.data);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Failed to generate animation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea 
        value={story}
        onChange={(e) => setStory(e.target.value)}
        placeholder="Enter your story..."
      />
      <button onClick={generateAnimation} disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>
      {error && <div className="error">{error}</div>}
      {animation && <AnimationPlayer data={animation} />}
    </div>
  );
}
```

## Related Documentation

- [Getting Started](GETTING_STARTED.md)
- [Configuration](CONFIG.md)
- [Architecture](ARCHITECTURE.md)

---

For questions or issues, please [create an issue](https://github.com/your-repo/issues) on GitHub.
