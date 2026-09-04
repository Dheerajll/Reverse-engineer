"""
TechIntel Platform - Visualization Module

Generates architecture diagrams in multiple formats:
- Mermaid for documentation
- Excalidraw for interactive exploration
- GraphViz DOT for complex layouts
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import json


@dataclass
class DiagramNode:
    """A node in a diagram."""
    id: str
    label: str
    node_type: str = "box"  # box, circle, diamond, cylinder, etc.
    style: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_mermaid(self) -> str:
        """Generate Mermaid node definition."""
        shape_map = {
            "box": "[]",
            "circle": "(())",
            "diamond": "{{}}",
            "cylinder": "[()]",
            "rounded": "()",
        }
        shape = shape_map.get(self.node_type, "[]")
        return f'    {self.id}{shape}["{self.label}"]'


@dataclass
class DiagramEdge:
    """An edge in a diagram."""
    source_id: str
    target_id: str
    label: str = ""
    edge_type: str = "solid"  # solid, dashed, dotted
    direction: str = "forward"  # forward, backward, both
    style: Dict[str, str] = field(default_factory=dict)
    
    def to_mermaid(self) -> str:
        """Generate Mermaid edge definition."""
        line_map = {
            "solid": "-->",
            "dashed": "-.->",
            "dotted": "....>",
            "bidirectional": "<-->",
        }
        line = line_map.get(self.edge_type, "-->")
        
        if self.direction == "backward":
            line = "<" + line[1:]
        elif self.direction == "both":
            line = "<->"
        
        label_part = f"|{self.label}|" if self.label else ""
        return f"    {self.source_id} {line} {self.target_id}"


@dataclass 
class DiagramLayer:
    """A layer in a multi-layer diagram."""
    name: str
    description: str
    nodes: List[DiagramNode] = field(default_factory=list)
    edges: List[DiagramEdge] = field(default_factory=list)


class ArchitectureVisualizer:
    """
    Generate architecture diagrams from system descriptions.
    """
    
    def __init__(self):
        self.nodes: List[DiagramNode] = []
        self.edges: List[DiagramEdge] = []
        self.layers: List[DiagramLayer] = []
        self.title: str = "Architecture Diagram"
    
    def add_node(self, node: DiagramNode) -> "ArchitectureVisualizer":
        """Add a node to the diagram."""
        self.nodes.append(node)
        return self
    
    def add_edge(self, edge: DiagramEdge) -> "ArchitectureVisualizer":
        """Add an edge to the diagram."""
        self.edges.append(edge)
        return self
    
    def add_layer(self, layer: DiagramLayer) -> "ArchitectureVisualizer":
        """Add a layer to the diagram."""
        self.layers.append(layer)
        return self
    
    def set_title(self, title: str) -> "ArchitectureVisualizer":
        """Set the diagram title."""
        self.title = title
        return self
    
    def to_mermaid(self, graph_type: str = "TD") -> str:
        """
        Export diagram as Mermaid syntax.
        
        Args:
            graph_type: TD (top-down), LR (left-right), TB (top-bottom), etc.
        """
        lines = [f"```mermaid", f"graph {graph_type}", f"    title {self.title}"]
        
        # Add subgraphs for layers if present
        if self.layers:
            for i, layer in enumerate(self.layers):
                lines.append(f"    subgraph layer{i}[{layer.name}]")
                for node in layer.nodes:
                    lines.append(node.to_mermaid())
                lines.append("    end")
                
                for edge in layer.edges:
                    lines.append(edge.to_mermaid())
        else:
            # Flat structure
            for node in self.nodes:
                lines.append(node.to_mermaid())
            
            for edge in self.edges:
                lines.append(edge.to_mermaid())
        
        # Add styling
        if any(n.style for n in self.nodes):
            lines.append("")
            lines.append("    %% Styles")
            for node in self.nodes:
                if node.style:
                    style_str = ",".join(f"{k}:{v}" for k, v in node.style.items())
                    lines.append(f"    style {node.id} {style_str}")
        
        lines.append("```")
        return "\n".join(lines)
    
    def to_excalidraw(self) -> Dict[str, Any]:
        """
        Export diagram as Excalidraw scene.
        
        Returns Excalidraw-compatible JSON structure.
        """
        elements = []
        y_offset = 0
        
        # Create rectangles for nodes
        for i, node in enumerate(self.nodes):
            x = 50 + (i % 4) * 200
            y = 100 + (i // 4) * 150 + y_offset
            
            # Rectangle
            rect = {
                "type": "rectangle",
                "x": x,
                "y": y,
                "width": 180,
                "height": 80,
                "strokeColor": node.style.get("strokeColor", "#000000"),
                "backgroundColor": node.style.get("backgroundColor", "transparent"),
                "fillStyle": "hachure",
                "strokeWidth": 1,
                "roughness": 1,
                "text": node.label,
                "fontSize": 16,
                "fontFamily": 1,
            }
            elements.append(rect)
        
        # Create arrows for edges
        for edge in self.edges:
            source_node = next((n for n in self.nodes if n.id == edge.source_id), None)
            target_node = next((n for n in self.nodes if n.id == edge.target_id), None)
            
            if source_node and target_node:
                arrow = {
                    "type": "arrow",
                    "start": {"x": 0, "y": 0},  # Would need actual coordinates
                    "end": {"x": 0, "y": 0},
                    "strokeColor": "#000000",
                    "strokeWidth": 2,
                    "roughness": 1,
                }
                elements.append(arrow)
        
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "techintel",
            "elements": elements,
            "appState": {
                "viewBackgroundColor": "#ffffff",
                "gridSize": 20,
            },
        }
    
    def to_dot(self) -> str:
        """
        Export diagram as GraphViz DOT format.
        """
        lines = ["digraph Architecture {"]
        lines.append("    rankdir=TB;")
        lines.append(f'    label="{self.title}";')
        lines.append("    labelloc=t;")
        
        # Node definitions
        for node in self.nodes:
            shape_map = {
                "box": "box",
                "circle": "ellipse",
                "diamond": "diamond",
                "cylinder": "cylinder",
            }
            shape = shape_map.get(node.node_type, "box")
            
            attrs = [f'label="{node.label}"', f'shape={shape}']
            if node.style:
                for k, v in node.style.items():
                    attrs.append(f'{k}="{v}"')
            
            lines.append(f'    {node.id} [{", ".join(attrs)}];')
        
        # Edge definitions
        for edge in self.edges:
            attrs = []
            if edge.label:
                attrs.append(f'label="{edge.label}"')
            if edge.edge_type == "dashed":
                attrs.append("style=dashed")
            elif edge.edge_type == "dotted":
                attrs.append("style=dotted")
            
            attr_str = f" [{', '.join(attrs)}]" if attrs else ""
            lines.append(f"    {edge.source_id} -> {edge.target_id}{attr_str};")
        
        lines.append("}")
        return "\n".join(lines)
    
    def generate_system_diagram(self, components: List[Dict[str, Any]]) -> str:
        """
        Generate a system architecture diagram from component list.
        
        Args:
            components: List of component dicts with keys:
                       - name: Component name
                       - type: Component type
                       - dependencies: List of dependency names
        """
        self.nodes = []
        self.edges = []
        
        # Create nodes
        for comp in components:
            node = DiagramNode(
                id=f"comp_{comp['name'].replace(' ', '_')}",
                label=comp["name"],
                node_type=self._get_node_type(comp.get("type", "service")),
            )
            self.nodes.append(node)
        
        # Create edges
        for comp in components:
            source_id = f"comp_{comp['name'].replace(' ', '_')}"
            for dep in comp.get("dependencies", []):
                target_id = f"comp_{dep.replace(' ', '_')}"
                edge = DiagramEdge(
                    source_id=source_id,
                    target_id=target_id,
                    label="depends on",
                    edge_type="dashed",
                )
                self.edges.append(edge)
        
        return self.to_mermaid()
    
    def _get_node_type(self, component_type: str) -> str:
        """Map component type to diagram node type."""
        type_map = {
            "database": "cylinder",
            "queue": "cylinder",
            "decision": "diamond",
            "actor": "circle",
            "user": "circle",
            "service": "box",
            "api": "rounded",
        }
        return type_map.get(component_type.lower(), "box")


def generate_sequence_diagram(actors: List[str], messages: List[Dict[str, str]]) -> str:
    """
    Generate a Mermaid sequence diagram.
    
    Args:
        actors: List of actor names
        messages: List of message dicts with keys:
                 - from: sender
                 - to: receiver
                 - message: message text
    """
    lines = ["```mermaid", "sequenceDiagram"]
    
    # Define participants
    for actor in actors:
        safe_name = actor.replace(" ", "_")
        lines.append(f"    participant {safe_name} as {actor}")
    
    # Add messages
    for msg in messages:
        from_actor = msg["from"].replace(" ", "_")
        to_actor = msg["to"].replace(" ", "_")
        message = msg["message"]
        lines.append(f"    {from_actor}->>{to_actor}: {message}")
    
    lines.append("```")
    return "\n".join(lines)


def generate_flowchart(steps: List[Dict[str, Any]]) -> str:
    """
    Generate a Mermaid flowchart.
    
    Args:
        steps: List of step dicts with keys:
              - id: Step identifier
              - label: Step label
              - type: Step type (process, decision, start, end)
              - next: Next step id(s)
    """
    lines = ["```mermaid", "graph TD"]
    
    type_map = {
        "start": "([",
        "end": "])",
        "process": "[",
        "decision": "{{",
        "data": "[(",
    }
    
    end_map = {
        "start": "])",
        "end": ")",
        "process": "]",
        "decision": "}}",
        "data": ")]",
    }
    
    # Define nodes
    for step in steps:
        start_sym = type_map.get(step.get("type", "process"), "[")
        end_sym = end_map.get(step.get("type", "process"), "]")
        lines.append(f"    {step['id']}{start_sym}{step['label']}{end_sym}")
    
    # Define edges
    for step in steps:
        next_steps = step.get("next", [])
        if isinstance(next_steps, str):
            next_steps = [next_steps]
        for next_id in next_steps:
            lines.append(f"    {step['id']} --> {next_id}")
    
    lines.append("```")
    return "\n".join(lines)
