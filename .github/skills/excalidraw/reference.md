# Excalidraw Complete Reference

## JSON Schema Reference

### File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [/* ExcalidrawElement[] */],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {
    "fileId": {
      "mimeType": "image/png",
      "id": "fileId",
      "dataURL": "data:image/png;base64,...",
      "created": 1699000000000,
      "lastRetrieved": 1699000000000
    }
  }
}
```

## Element Types

### Common Properties (All Elements)

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier (nanoid) |
| `type` | string | Element type |
| `x` | number | X coordinate |
| `y` | number | Y coordinate |
| `width` | number | Width in pixels |
| `height` | number | Height in pixels |
| `angle` | number | Rotation in radians (0 = no rotation) |
| `strokeColor` | string | Border/stroke color (hex) |
| `backgroundColor` | string | Fill color (hex) or "transparent" |
| `fillStyle` | string | "solid" \| "hachure" \| "cross-hatch" |
| `strokeWidth` | number | Border width (1, 2, 4) |
| `strokeStyle` | string | "solid" \| "dashed" \| "dotted" |
| `roughness` | number | Hand-drawn effect (0=none, 1=slight, 2=rough) |
| `opacity` | number | 0-100 |
| `groupIds` | string[] | Group memberships |
| `frameId` | string \| null | Parent frame ID |
| `roundness` | object \| null | Corner rounding config |
| `seed` | number | Random seed for roughness |
| `version` | number | Element version counter |
| `versionNonce` | number | Version random component |
| `isDeleted` | boolean | Soft delete flag |
| `boundElements` | array | Linked elements (arrows, text) |
| `updated` | number | Last modified timestamp |
| `link` | string \| null | Hyperlink URL |
| `locked` | boolean | Prevent modifications |

### Rectangle

```json
{
  "id": "rect-1",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 100,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "angle": 0,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 123456789,
  "version": 1,
  "versionNonce": 987654321,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1699000000000,
  "link": null,
  "locked": false
}
```

### Ellipse

Same properties as rectangle. Use for circles (equal width/height).

### Diamond

Same properties as rectangle. Renders as a rotated square (rhombus).

### Text

| Property | Type | Description |
|----------|------|-------------|
| `text` | string | Text content (supports \n) |
| `fontSize` | number | Font size in pixels |
| `fontFamily` | number | 1=Virgil, 2=Helvetica, 3=Cascadia |
| `textAlign` | string | "left" \| "center" \| "right" |
| `verticalAlign` | string | "top" \| "middle" \| "bottom" |
| `containerId` | string \| null | Parent container ID |
| `originalText` | string | Original text before wrapping |
| `autoResize` | boolean | Auto-resize container |
| `lineHeight` | number | Line height multiplier |

```json
{
  "id": "text-1",
  "type": "text",
  "x": 100,
  "y": 100,
  "width": 100,
  "height": 25,
  "text": "API Gateway",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "containerId": null,
  "originalText": "API Gateway",
  "autoResize": true,
  "lineHeight": 1.25
}
```

### Arrow & Line

| Property | Type | Description |
|----------|------|-------------|
| `points` | number[][] | Array of [x, y] offsets from origin |
| `startArrowhead` | string \| null | "arrow" \| "bar" \| "dot" \| "triangle" |
| `endArrowhead` | string \| null | Same as startArrowhead |
| `startBinding` | object \| null | Start element binding |
| `endBinding` | object \| null | End element binding |

```json
{
  "id": "arrow-1",
  "type": "arrow",
  "x": 300,
  "y": 150,
  "width": 100,
  "height": 0,
  "points": [[0, 0], [100, 0]],
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": {
    "elementId": "rect-1",
    "focus": 0,
    "gap": 5
  },
  "endBinding": {
    "elementId": "rect-2",
    "focus": 0,
    "gap": 5
  }
}
```

### Freedraw

| Property | Type | Description |
|----------|------|-------------|
| `points` | number[][] | Freehand path points |
| `pressures` | number[] | Pressure values per point |
| `simulatePressure` | boolean | Simulate pressure variation |

### Image

| Property | Type | Description |
|----------|------|-------------|
| `fileId` | string | Reference to files object |
| `status` | string | "pending" \| "saved" \| "error" |
| `scale` | [number, number] | X and Y scale factors |

```json
{
  "id": "image-1",
  "type": "image",
  "x": 100,
  "y": 100,
  "width": 100,
  "height": 100,
  "fileId": "abc123",
  "status": "saved",
  "scale": [1, 1]
}
```

### Frame

| Property | Type | Description |
|----------|------|-------------|
| `name` | string \| null | Frame label |

```json
{
  "id": "frame-1",
  "type": "frame",
  "x": 50,
  "y": 50,
  "width": 500,
  "height": 400,
  "name": "Microservices Layer"
}
```

## Element Bindings

### Connecting Arrow to Shape

1. Add `boundElements` to the shape:
```json
{
  "id": "rect-1",
  "type": "rectangle",
  "boundElements": [
    { "id": "arrow-1", "type": "arrow" }
  ]
}
```

2. Add `startBinding` or `endBinding` to the arrow:
```json
{
  "id": "arrow-1",
  "type": "arrow",
  "startBinding": {
    "elementId": "rect-1",
    "focus": 0,
    "gap": 5
  }
}
```

### Text Inside Shape

1. Add `boundElements` to the container:
```json
{
  "id": "rect-1",
  "type": "rectangle",
  "boundElements": [
    { "id": "text-1", "type": "text" }
  ]
}
```

2. Set `containerId` on the text:
```json
{
  "id": "text-1",
  "type": "text",
  "containerId": "rect-1"
}
```

## Grouping Elements

Assign the same `groupIds` array to related elements:

```json
{
  "id": "rect-1",
  "groupIds": ["group-1"]
},
{
  "id": "text-1",
  "groupIds": ["group-1"]
}
```

Nested groups use multiple IDs:
```json
{
  "groupIds": ["inner-group", "outer-group"]
}
```

## ID Generation

Use nanoid-style IDs (21 characters, alphanumeric):
```
pologsyG-tAraPgiN9xP9b
```

For manual generation, use any unique string format.

## Coordinate System

- Origin (0, 0) is at the canvas center
- X increases to the right
- Y increases downward
- All measurements in pixels
- Grid snapping: 20px default

## Recommended Spacing

| Element | Spacing |
|---------|---------|
| Between components | 40-80px |
| Arrow gap from shape | 5-10px |
| Text padding in container | 10-20px |
| Group margin | 20px |
| Frame padding | 40px |

## Color Reference

### Default Palette

| Color | Hex | Use |
|-------|-----|-----|
| Black | `#1e1e1e` | Strokes, text |
| White | `#ffffff` | Backgrounds |
| Light Blue | `#a5d8ff` | Compute services |
| Light Green | `#b2f2bb` | Databases, storage |
| Light Orange | `#ffd8a8` | Networking |
| Light Red | `#ffc9c9` | Security, errors |
| Light Purple | `#d0bfff` | Integration |
| Light Yellow | `#fff3bf` | Highlights |
| Gray | `#dee2e6` | External, users |

### Transparent
Use `"transparent"` for no fill.

## Font Families

| ID | Name | Style |
|----|------|-------|
| 1 | Virgil | Hand-drawn |
| 2 | Helvetica | Sans-serif |
| 3 | Cascadia | Monospace |

## Roundness Types

| Type | Effect |
|------|--------|
| 1 | Proportional (legacy) |
| 2 | Adaptive |
| 3 | Rounded corners |

```json
"roundness": { "type": 3 }
```

## Creating Architecture Components

### Service Box with Label

```json
[
  {
    "id": "service-1",
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 120,
    "height": 60,
    "backgroundColor": "#a5d8ff",
    "strokeColor": "#1e1e1e",
    "strokeWidth": 2,
    "roundness": { "type": 3 },
    "boundElements": [
      { "id": "service-1-text", "type": "text" }
    ]
  },
  {
    "id": "service-1-text",
    "type": "text",
    "x": 105,
    "y": 115,
    "text": "API Gateway",
    "fontSize": 16,
    "fontFamily": 2,
    "textAlign": "center",
    "containerId": "service-1"
  }
]
```

### Database Icon

```json
{
  "id": "db-1",
  "type": "ellipse",
  "x": 100,
  "y": 100,
  "width": 80,
  "height": 40,
  "backgroundColor": "#b2f2bb",
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2
}
```

### Connected Components

```json
[
  {
    "id": "rect-1",
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 100,
    "height": 60,
    "boundElements": [
      { "id": "arrow-1", "type": "arrow" }
    ]
  },
  {
    "id": "rect-2",
    "type": "rectangle",
    "x": 300,
    "y": 100,
    "width": 100,
    "height": 60,
    "boundElements": [
      { "id": "arrow-1", "type": "arrow" }
    ]
  },
  {
    "id": "arrow-1",
    "type": "arrow",
    "x": 200,
    "y": 130,
    "width": 100,
    "height": 0,
    "points": [[0, 0], [100, 0]],
    "endArrowhead": "arrow",
    "startBinding": {
      "elementId": "rect-1",
      "focus": 0,
      "gap": 5
    },
    "endBinding": {
      "elementId": "rect-2",
      "focus": 0,
      "gap": 5
    }
  }
]
```

## Library Format (.excalidrawlib)

```json
{
  "type": "excalidrawlib",
  "version": 2,
  "source": "custom",
  "libraryItems": [
    {
      "id": "item-1",
      "status": "published",
      "elements": [/* ExcalidrawElement[] */],
      "name": "AWS Lambda",
      "created": 1699000000000
    }
  ]
}
```

## VS Code Settings

```json
{
  "excalidraw.workspaceLibraryPath": ".excalidraw/library.excalidrawlib",
  "excalidraw.theme": "light"
}
```

## Obsidian Settings

In Excalidraw plugin settings:
- Default template location
- Auto-save interval
- Default font family
- Theme synchronization
- Library folder path

## Mermaid to Excalidraw

Convert Mermaid diagrams using:
```javascript
import { parseMermaidToExcalidraw } from "@excalidraw/mermaid-to-excalidraw";

const { elements, files } = await parseMermaidToExcalidraw(`
  flowchart LR
    A[API] --> B[Service]
    B --> C[Database]
`);
```
