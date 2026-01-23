#!/usr/bin/env python3
"""
Excalidraw Diagram Generator

A Python library for programmatically generating Excalidraw diagrams.
Supports architecture diagrams, flowcharts, and technical documentation.

Usage:
    from excalidraw_generator import ExcalidrawDiagram, Component, Arrow

    diagram = ExcalidrawDiagram()
    api = diagram.add_component("API Gateway", x=100, y=100, style="compute")
    service = diagram.add_component("Service", x=300, y=100, style="compute")
    diagram.connect(api, service)
    diagram.save("architecture.excalidraw")
"""

import json
import random
import string
import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Any
from enum import Enum


class ComponentStyle(Enum):
    """Predefined styles for architecture components."""
    COMPUTE = {"backgroundColor": "#a5d8ff", "strokeColor": "#1971c2"}
    DATABASE = {"backgroundColor": "#b2f2bb", "strokeColor": "#2f9e44"}
    STORAGE = {"backgroundColor": "#b2f2bb", "strokeColor": "#2f9e44"}
    NETWORK = {"backgroundColor": "#ffd8a8", "strokeColor": "#e8590c"}
    SECURITY = {"backgroundColor": "#ffc9c9", "strokeColor": "#c92a2a"}
    INTEGRATION = {"backgroundColor": "#d0bfff", "strokeColor": "#7048e8"}
    EXTERNAL = {"backgroundColor": "#dee2e6", "strokeColor": "#495057"}
    USER = {"backgroundColor": "#dee2e6", "strokeColor": "#495057"}
    QUEUE = {"backgroundColor": "#fff3bf", "strokeColor": "#f08c00"}
    CACHE = {"backgroundColor": "#ffe8cc", "strokeColor": "#d9480f"}


class CloudProvider(Enum):
    """Cloud provider color schemes."""
    AWS = {"primary": "#ff9900", "secondary": "#232f3e"}
    AZURE = {"primary": "#0078d4", "secondary": "#50e6ff"}
    GCP = {"primary": "#4285f4", "secondary": "#34a853"}
    KUBERNETES = {"primary": "#326ce5", "secondary": "#ffffff"}


def generate_id(length: int = 21) -> str:
    """Generate a nanoid-style ID."""
    chars = string.ascii_letters + string.digits + "-_"
    return ''.join(random.choice(chars) for _ in range(length))


def generate_seed() -> int:
    """Generate a random seed for roughness."""
    return random.randint(1, 2147483647)


@dataclass
class Element:
    """Base class for Excalidraw elements."""
    id: str = field(default_factory=generate_id)
    x: float = 0
    y: float = 0
    width: float = 100
    height: float = 50
    stroke_color: str = "#1e1e1e"
    background_color: str = "transparent"
    fill_style: str = "solid"
    stroke_width: int = 2
    stroke_style: str = "solid"
    roughness: int = 1
    opacity: int = 100
    angle: float = 0
    group_ids: List[str] = field(default_factory=list)
    frame_id: Optional[str] = None
    seed: int = field(default_factory=generate_seed)
    bound_elements: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert element to Excalidraw JSON format."""
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "strokeColor": self.stroke_color,
            "backgroundColor": self.background_color,
            "fillStyle": self.fill_style,
            "strokeWidth": self.stroke_width,
            "strokeStyle": self.stroke_style,
            "roughness": self.roughness,
            "opacity": self.opacity,
            "angle": self.angle,
            "groupIds": self.group_ids,
            "frameId": self.frame_id,
            "seed": self.seed,
            "version": 1,
            "versionNonce": generate_seed(),
            "isDeleted": False,
            "boundElements": self.bound_elements,
            "updated": int(time.time() * 1000),
            "link": None,
            "locked": False,
        }


@dataclass
class Rectangle(Element):
    """Rectangle element."""

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "rectangle"
        data["roundness"] = {"type": 3}
        return data


@dataclass
class Ellipse(Element):
    """Ellipse/circle element."""

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "ellipse"
        data["roundness"] = {"type": 2}
        return data


@dataclass
class Diamond(Element):
    """Diamond/rhombus element."""

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "diamond"
        data["roundness"] = {"type": 2}
        return data


@dataclass
class Text(Element):
    """Text element."""
    text: str = ""
    font_size: int = 20
    font_family: int = 1  # 1=Virgil, 2=Helvetica, 3=Cascadia
    text_align: str = "center"
    vertical_align: str = "middle"
    container_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "text"
        data["text"] = self.text
        data["fontSize"] = self.font_size
        data["fontFamily"] = self.font_family
        data["textAlign"] = self.text_align
        data["verticalAlign"] = self.vertical_align
        data["containerId"] = self.container_id
        data["originalText"] = self.text
        data["autoResize"] = True
        data["lineHeight"] = 1.25
        data["baseline"] = self.font_size
        return data


@dataclass
class Arrow(Element):
    """Arrow/line element."""
    points: List[List[float]] = field(default_factory=lambda: [[0, 0], [100, 0]])
    start_arrowhead: Optional[str] = None
    end_arrowhead: str = "arrow"
    start_binding: Optional[Dict] = None
    end_binding: Optional[Dict] = None

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "arrow"
        data["points"] = self.points
        data["startArrowhead"] = self.start_arrowhead
        data["endArrowhead"] = self.end_arrowhead
        data["startBinding"] = self.start_binding
        data["endBinding"] = self.end_binding
        data["roundness"] = {"type": 2}
        return data


@dataclass
class Line(Arrow):
    """Line element (arrow without arrowheads)."""
    start_arrowhead: Optional[str] = None
    end_arrowhead: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "line"
        return data


@dataclass
class Frame(Element):
    """Frame element for grouping."""
    name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["type"] = "frame"
        data["name"] = self.name
        data["roundness"] = None
        return data


class Component:
    """High-level architecture component with shape and label."""

    def __init__(
        self,
        label: str,
        x: float,
        y: float,
        width: float = 120,
        height: float = 60,
        shape: str = "rectangle",
        style: Optional[ComponentStyle] = None,
        font_size: int = 16,
    ):
        self.id = generate_id()
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shape_type = shape
        self.style = style or ComponentStyle.COMPUTE
        self.font_size = font_size
        self.text_id = generate_id()

    def get_center(self) -> Tuple[float, float]:
        """Get center coordinates."""
        return (self.x + self.width / 2, self.y + self.height / 2)

    def get_right_edge(self) -> Tuple[float, float]:
        """Get right edge center point."""
        return (self.x + self.width, self.y + self.height / 2)

    def get_left_edge(self) -> Tuple[float, float]:
        """Get left edge center point."""
        return (self.x, self.y + self.height / 2)

    def get_top_edge(self) -> Tuple[float, float]:
        """Get top edge center point."""
        return (self.x + self.width / 2, self.y)

    def get_bottom_edge(self) -> Tuple[float, float]:
        """Get bottom edge center point."""
        return (self.x + self.width / 2, self.y + self.height)

    def to_elements(self) -> List[Dict]:
        """Convert component to Excalidraw elements."""
        style_colors = self.style.value

        # Create shape
        if self.shape_type == "rectangle":
            shape = Rectangle(
                id=self.id,
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                background_color=style_colors["backgroundColor"],
                stroke_color=style_colors["strokeColor"],
                bound_elements=[{"id": self.text_id, "type": "text"}]
            )
        elif self.shape_type == "ellipse":
            shape = Ellipse(
                id=self.id,
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                background_color=style_colors["backgroundColor"],
                stroke_color=style_colors["strokeColor"],
                bound_elements=[{"id": self.text_id, "type": "text"}]
            )
        elif self.shape_type == "diamond":
            shape = Diamond(
                id=self.id,
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                background_color=style_colors["backgroundColor"],
                stroke_color=style_colors["strokeColor"],
                bound_elements=[{"id": self.text_id, "type": "text"}]
            )
        else:
            shape = Rectangle(
                id=self.id,
                x=self.x,
                y=self.y,
                width=self.width,
                height=self.height,
                background_color=style_colors["backgroundColor"],
                stroke_color=style_colors["strokeColor"],
                bound_elements=[{"id": self.text_id, "type": "text"}]
            )

        # Create text label
        text = Text(
            id=self.text_id,
            x=self.x + 5,
            y=self.y + (self.height - self.font_size) / 2,
            width=self.width - 10,
            height=self.font_size + 5,
            text=self.label,
            font_size=self.font_size,
            font_family=2,  # Helvetica
            container_id=self.id,
            stroke_color=style_colors["strokeColor"],
        )

        return [shape.to_dict(), text.to_dict()]


class ExcalidrawDiagram:
    """Main class for creating Excalidraw diagrams."""

    def __init__(
        self,
        background_color: str = "#ffffff",
        grid_size: int = 20,
    ):
        self.elements: List[Dict] = []
        self.components: Dict[str, Component] = {}
        self.files: Dict = {}
        self.background_color = background_color
        self.grid_size = grid_size

    def add_component(
        self,
        label: str,
        x: float,
        y: float,
        width: float = 120,
        height: float = 60,
        shape: str = "rectangle",
        style: Optional[ComponentStyle] = None,
        **kwargs
    ) -> Component:
        """Add a labeled component to the diagram."""
        component = Component(
            label=label,
            x=x,
            y=y,
            width=width,
            height=height,
            shape=shape,
            style=style,
            **kwargs
        )
        self.components[component.id] = component
        self.elements.extend(component.to_elements())
        return component

    def add_rectangle(
        self,
        x: float,
        y: float,
        width: float = 100,
        height: float = 50,
        **kwargs
    ) -> Rectangle:
        """Add a simple rectangle."""
        rect = Rectangle(x=x, y=y, width=width, height=height, **kwargs)
        self.elements.append(rect.to_dict())
        return rect

    def add_ellipse(
        self,
        x: float,
        y: float,
        width: float = 100,
        height: float = 50,
        **kwargs
    ) -> Ellipse:
        """Add an ellipse/circle."""
        ellipse = Ellipse(x=x, y=y, width=width, height=height, **kwargs)
        self.elements.append(ellipse.to_dict())
        return ellipse

    def add_text(
        self,
        text: str,
        x: float,
        y: float,
        font_size: int = 20,
        **kwargs
    ) -> Text:
        """Add standalone text."""
        text_elem = Text(
            x=x,
            y=y,
            text=text,
            font_size=font_size,
            width=len(text) * font_size * 0.6,
            height=font_size + 5,
            **kwargs
        )
        self.elements.append(text_elem.to_dict())
        return text_elem

    def add_frame(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        name: Optional[str] = None,
    ) -> Frame:
        """Add a frame for grouping elements."""
        frame = Frame(x=x, y=y, width=width, height=height, name=name)
        self.elements.append(frame.to_dict())
        return frame

    def connect(
        self,
        from_component: Component,
        to_component: Component,
        label: Optional[str] = None,
        direction: str = "horizontal",
        arrow_style: str = "arrow",
    ) -> Arrow:
        """Connect two components with an arrow."""
        if direction == "horizontal":
            start = from_component.get_right_edge()
            end = to_component.get_left_edge()
        elif direction == "vertical":
            start = from_component.get_bottom_edge()
            end = to_component.get_top_edge()
        else:
            start = from_component.get_center()
            end = to_component.get_center()

        arrow = Arrow(
            x=start[0],
            y=start[1],
            points=[[0, 0], [end[0] - start[0], end[1] - start[1]]],
            width=abs(end[0] - start[0]),
            height=abs(end[1] - start[1]),
            end_arrowhead=arrow_style,
            start_binding={
                "elementId": from_component.id,
                "focus": 0,
                "gap": 5
            },
            end_binding={
                "elementId": to_component.id,
                "focus": 0,
                "gap": 5
            }
        )

        # Update bound elements on components
        for elem in self.elements:
            if elem.get("id") == from_component.id:
                elem["boundElements"].append({"id": arrow.id, "type": "arrow"})
            elif elem.get("id") == to_component.id:
                elem["boundElements"].append({"id": arrow.id, "type": "arrow"})

        self.elements.append(arrow.to_dict())

        # Add label if provided
        if label:
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2 - 20
            self.add_text(label, mid_x, mid_y, font_size=14)

        return arrow

    def add_arrow(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        **kwargs
    ) -> Arrow:
        """Add a standalone arrow."""
        arrow = Arrow(
            x=start[0],
            y=start[1],
            points=[[0, 0], [end[0] - start[0], end[1] - start[1]]],
            width=abs(end[0] - start[0]),
            height=abs(end[1] - start[1]),
            **kwargs
        )
        self.elements.append(arrow.to_dict())
        return arrow

    def to_json(self) -> Dict:
        """Export diagram to Excalidraw JSON format."""
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {
                "gridSize": self.grid_size,
                "viewBackgroundColor": self.background_color
            },
            "files": self.files
        }

    def save(self, filename: str) -> None:
        """Save diagram to file."""
        if not filename.endswith(".excalidraw"):
            filename += ".excalidraw"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_json(), f, indent=2)

        print(f"Diagram saved to {filename}")

    def to_json_string(self) -> str:
        """Export diagram to JSON string."""
        return json.dumps(self.to_json(), indent=2)


# ============================================================================
# Template Functions for Common Architecture Patterns
# ============================================================================

def create_microservices_diagram(
    services: List[str],
    filename: str = "microservices.excalidraw"
) -> ExcalidrawDiagram:
    """Create a microservices architecture diagram."""
    diagram = ExcalidrawDiagram()

    # API Gateway
    gateway = diagram.add_component(
        "API Gateway",
        x=100, y=200,
        width=120, height=60,
        style=ComponentStyle.NETWORK
    )

    # Services
    service_components = []
    for i, service_name in enumerate(services):
        service = diagram.add_component(
            service_name,
            x=300 + (i % 2) * 150,
            y=100 + (i // 2) * 100,
            width=120, height=60,
            style=ComponentStyle.COMPUTE
        )
        service_components.append(service)
        diagram.connect(gateway, service)

    # Database
    db = diagram.add_component(
        "Database",
        x=550, y=200,
        width=100, height=50,
        shape="ellipse",
        style=ComponentStyle.DATABASE
    )

    for service in service_components:
        diagram.connect(service, db)

    diagram.save(filename)
    return diagram


def create_three_tier_diagram(
    filename: str = "three-tier.excalidraw"
) -> ExcalidrawDiagram:
    """Create a 3-tier architecture diagram."""
    diagram = ExcalidrawDiagram()

    # Presentation tier
    web = diagram.add_component(
        "Web Tier",
        x=100, y=100,
        width=140, height=60,
        style=ComponentStyle.EXTERNAL
    )

    # Application tier
    app = diagram.add_component(
        "App Tier",
        x=100, y=220,
        width=140, height=60,
        style=ComponentStyle.COMPUTE
    )

    # Data tier
    data = diagram.add_component(
        "Data Tier",
        x=100, y=340,
        width=140, height=60,
        style=ComponentStyle.DATABASE
    )

    # Cache
    cache = diagram.add_component(
        "Cache",
        x=300, y=220,
        width=100, height=50,
        style=ComponentStyle.CACHE
    )

    diagram.connect(web, app, direction="vertical")
    diagram.connect(app, data, direction="vertical")
    diagram.connect(app, cache)

    diagram.save(filename)
    return diagram


def create_event_driven_diagram(
    filename: str = "event-driven.excalidraw"
) -> ExcalidrawDiagram:
    """Create an event-driven architecture diagram."""
    diagram = ExcalidrawDiagram()

    # Producers
    producer1 = diagram.add_component(
        "Producer A",
        x=100, y=100,
        width=100, height=50,
        style=ComponentStyle.COMPUTE
    )
    producer2 = diagram.add_component(
        "Producer B",
        x=100, y=180,
        width=100, height=50,
        style=ComponentStyle.COMPUTE
    )

    # Event bus
    bus = diagram.add_component(
        "Event Bus",
        x=280, y=140,
        width=120, height=60,
        style=ComponentStyle.QUEUE
    )

    # Consumers
    consumer1 = diagram.add_component(
        "Consumer X",
        x=480, y=100,
        width=100, height=50,
        style=ComponentStyle.COMPUTE
    )
    consumer2 = diagram.add_component(
        "Consumer Y",
        x=480, y=180,
        width=100, height=50,
        style=ComponentStyle.COMPUTE
    )

    # Event store
    store = diagram.add_component(
        "Event Store",
        x=280, y=260,
        width=120, height=50,
        style=ComponentStyle.DATABASE
    )

    diagram.connect(producer1, bus)
    diagram.connect(producer2, bus)
    diagram.connect(bus, consumer1)
    diagram.connect(bus, consumer2)
    diagram.connect(bus, store, direction="vertical")

    diagram.save(filename)
    return diagram


def create_data_pipeline_diagram(
    filename: str = "data-pipeline.excalidraw"
) -> ExcalidrawDiagram:
    """Create a data pipeline architecture diagram."""
    diagram = ExcalidrawDiagram()

    # Sources
    sources = diagram.add_component(
        "Data Sources",
        x=100, y=150,
        width=100, height=50,
        style=ComponentStyle.EXTERNAL
    )

    # Ingestion
    ingestion = diagram.add_component(
        "Ingestion",
        x=250, y=150,
        width=100, height=50,
        style=ComponentStyle.QUEUE
    )

    # Processing
    processing = diagram.add_component(
        "Processing",
        x=400, y=150,
        width=100, height=50,
        style=ComponentStyle.COMPUTE
    )

    # Storage
    storage = diagram.add_component(
        "Data Lake",
        x=550, y=150,
        width=100, height=50,
        style=ComponentStyle.STORAGE
    )

    # Analytics
    analytics = diagram.add_component(
        "Analytics",
        x=700, y=150,
        width=100, height=50,
        style=ComponentStyle.INTEGRATION
    )

    diagram.connect(sources, ingestion)
    diagram.connect(ingestion, processing)
    diagram.connect(processing, storage)
    diagram.connect(storage, analytics)

    diagram.save(filename)
    return diagram


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Simple example
    diagram = ExcalidrawDiagram()

    # Add components
    frontend = diagram.add_component(
        "Frontend",
        x=100, y=100,
        style=ComponentStyle.EXTERNAL
    )

    api = diagram.add_component(
        "API Service",
        x=300, y=100,
        style=ComponentStyle.COMPUTE
    )

    db = diagram.add_component(
        "PostgreSQL",
        x=500, y=100,
        shape="ellipse",
        style=ComponentStyle.DATABASE
    )

    cache = diagram.add_component(
        "Redis Cache",
        x=400, y=220,
        style=ComponentStyle.CACHE
    )

    # Connect components
    diagram.connect(frontend, api, label="REST API")
    diagram.connect(api, db)
    diagram.connect(api, cache)

    # Save
    diagram.save("example-architecture.excalidraw")

    # Create template diagrams
    create_microservices_diagram(["Auth", "Users", "Orders", "Payments"])
    create_three_tier_diagram()
    create_event_driven_diagram()
    create_data_pipeline_diagram()

    print("All diagrams created successfully!")
