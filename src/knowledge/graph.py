"""
TechIntel Platform - Knowledge Graph Module

Manages entities, relationships, and provides graph-based reasoning.
"""

from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
import json


@dataclass
class GraphNode:
    """A node in the knowledge graph."""
    id: str
    label: str
    node_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "type": self.node_type,
            "properties": self.properties,
        }


@dataclass
class GraphEdge:
    """An edge in the knowledge graph."""
    id: str
    source_id: str
    target_id: str
    relation_type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source_id,
            "target": self.target_id,
            "relation": self.relation_type,
            "properties": self.properties,
        }


class KnowledgeGraph:
    """
    Knowledge graph for storing and querying technical entities.
    
    Supports:
    - Entity storage with typed relationships
    - Graph traversal and neighborhood queries
    - Path finding between concepts
    - Subgraph extraction
    - Export to various formats (Neo4j, GraphML, JSON)
    """
    
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        self.adjacency: Dict[str, Set[str]] = {}  # node_id -> neighbor ids
        self.reverse_adjacency: Dict[str, Set[str]] = {}
        
    def add_node(self, node_id: str, label: str, node_type: str, 
                 properties: Optional[Dict[str, Any]] = None) -> "KnowledgeGraph":
        """Add a node to the graph."""
        self.nodes[node_id] = GraphNode(
            id=node_id,
            label=label,
            node_type=node_type,
            properties=properties or {}
        )
        if node_id not in self.adjacency:
            self.adjacency[node_id] = set()
            self.reverse_adjacency[node_id] = set()
        return self
    
    def add_edge(self, edge_id: str, source_id: str, target_id: str,
                 relation_type: str, properties: Optional[Dict[str, Any]] = None) -> "KnowledgeGraph":
        """Add an edge between two nodes."""
        self.edges[edge_id] = GraphEdge(
            id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            properties=properties or {}
        )
        self.adjacency.setdefault(source_id, set()).add(target_id)
        self.reverse_adjacency.setdefault(target_id, set()).add(source_id)
        return self
    
    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_edge(self, edge_id: str) -> Optional[GraphEdge]:
        """Get an edge by ID."""
        return self.edges.get(edge_id)
    
    def get_neighbors(self, node_id: str, direction: str = "both") -> List[GraphNode]:
        """
        Get neighboring nodes.
        
        Args:
            node_id: The center node
            direction: 'out' for outgoing, 'in' for incoming, 'both' for all
        """
        neighbor_ids = set()
        if direction in ("out", "both"):
            neighbor_ids.update(self.adjacency.get(node_id, set()))
        if direction in ("in", "both"):
            neighbor_ids.update(self.reverse_adjacency.get(node_id, set()))
        
        return [self.nodes[nid] for nid in neighbor_ids if nid in self.nodes]
    
    def find_path(self, source_id: str, target_id: str, max_depth: int = 5) -> List[List[str]]:
        """
        Find all paths between two nodes up to max_depth.
        
        Returns list of paths, where each path is a list of node IDs.
        """
        if source_id == target_id:
            return [[source_id]]
        
        paths = []
        queue = [(source_id, [source_id])]
        
        while queue:
            current, path = queue.pop(0)
            if len(path) > max_depth:
                continue
            
            for neighbor_id in self.adjacency.get(current, set()):
                if neighbor_id in path:
                    continue
                
                new_path = path + [neighbor_id]
                if neighbor_id == target_id:
                    paths.append(new_path)
                else:
                    queue.append((neighbor_id, new_path))
        
        return paths
    
    def find_by_label(self, label: str, case_sensitive: bool = False) -> List[GraphNode]:
        """Find nodes by label (partial match)."""
        results = []
        for node in self.nodes.values():
            if case_sensitive:
                if label in node.label:
                    results.append(node)
            else:
                if label.lower() in node.label.lower():
                    results.append(node)
        return results
    
    def find_by_type(self, node_type: str) -> List[GraphNode]:
        """Find all nodes of a given type."""
        return [n for n in self.nodes.values() if n.node_type == node_type]
    
    def get_subgraph(self, node_ids: Set[str]) -> "KnowledgeGraph":
        """Extract a subgraph containing only specified nodes and their edges."""
        subgraph = KnowledgeGraph()
        
        # Add nodes
        for node_id in node_ids:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                subgraph.add_node(node_id, node.label, node.node_type, node.properties)
        
        # Add edges within the subgraph
        for edge in self.edges.values():
            if edge.source_id in node_ids and edge.target_id in node_ids:
                subgraph.add_edge(
                    edge.id, edge.source_id, edge.target_id,
                    edge.relation_type, edge.properties
                )
        
        return subgraph
    
    def get_ego_graph(self, center_id: str, radius: int = 1) -> "KnowledgeGraph":
        """Get the ego graph (center node and neighbors up to radius hops)."""
        visited = {center_id}
        current_level = {center_id}
        
        for _ in range(radius):
            next_level = set()
            for node_id in current_level:
                neighbors = set(self.adjacency.get(node_id, set()))
                neighbors.update(self.reverse_adjacency.get(node_id, set()))
                new_neighbors = neighbors - visited
                next_level.update(new_neighbors)
                visited.update(new_neighbors)
            current_level = next_level
        
        return self.get_subgraph(visited)
    
    def to_json(self) -> str:
        """Export graph to JSON format."""
        return json.dumps({
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges.values()],
        }, indent=2)
    
    def to_mermaid(self) -> str:
        """Export graph as Mermaid diagram syntax."""
        lines = ["graph TD"]
        
        # Add nodes
        for node in self.nodes.values():
            label = node.label.replace(" ", "_").replace("-", "_")
            lines.append(f"    {node.id}[{label}]")
        
        # Add edges
        for edge in self.edges.values():
            lines.append(f"    {edge.source_id} -- {edge.relation_type} --> {edge.target_id}")
        
        return "\n".join(lines)
    
    def statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        node_types = {}
        edge_types = {}
        
        for node in self.nodes.values():
            node_types[node.node_type] = node_types.get(node.node_type, 0) + 1
        
        for edge in self.edges.values():
            edge_types[edge.relation_type] = edge_types.get(edge.relation_type, 0) + 1
        
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "node_types": node_types,
            "edge_types": edge_types,
            "avg_degree": len(self.edges) * 2 / max(len(self.nodes), 1),
        }


class EntityExtractor:
    """
    Extract entities from text and add them to the knowledge graph.
    
    In a full implementation, this would use:
    - NLP models for named entity recognition
    - Pattern matching for technical terms
    - LLM-based extraction for complex cases
    """
    
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph
    
    def extract_from_text(self, text: str) -> List[GraphNode]:
        """Extract entities from text."""
        # TODO: Implement NLP-based entity extraction
        # For now, returns empty list as placeholder
        return []
    
    def extract_relationships(self, source_entity: str, target_entity: str,
                             context: str) -> Optional[str]:
        """Determine the relationship type between two entities based on context."""
        # TODO: Implement relationship classification
        return None
    
    def build_graph_from_documents(self, documents: List[Dict[str, Any]]) -> KnowledgeGraph:
        """Build a knowledge graph from a collection of documents."""
        # TODO: Implement batch document processing
        return self.graph
