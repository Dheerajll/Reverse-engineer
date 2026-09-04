"""
TechIntel Platform - Core Module

The core module provides the central orchestration layer that coordinates
all platform components to transform ideas into implementation blueprints.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
from datetime import datetime


class EvidenceConfidence(Enum):
    """Confidence levels for evidence claims."""
    HIGH = "high"       # Direct source, verifiable
    MEDIUM = "medium"   # Inferred with strong support
    LOW = "low"         # Speculative or weakly supported


class EntityType(Enum):
    """Types of entities in the knowledge graph."""
    CONCEPT = "concept"
    SYSTEM = "system"
    API = "api"
    ALGORITHM = "algorithm"
    PROTOCOL = "protocol"
    PAPER = "paper"
    REPOSITORY = "repository"
    PERSON = "person"
    ORGANIZATION = "organization"


@dataclass
class Source:
    """Represents a source of information."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: Optional[str] = None
    title: Optional[str] = None
    source_type: str = "unknown"  # paper, repo, doc, spec, etc.
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class Evidence:
    """A piece of evidence supporting a claim."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    source: Optional[Source] = None
    confidence: EvidenceConfidence = EvidenceConfidence.MEDIUM
    quote: Optional[str] = None
    location: Optional[str] = None  # File path, line number, section, etc.
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "source_url": self.source.url if self.source else None,
            "confidence": self.confidence.value,
            "quote": self.quote,
            "location": self.location,
        }


@dataclass
class Claim:
    """A claim backed by evidence."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    statement: str = ""
    evidences: List[Evidence] = field(default_factory=list)
    category: str = "general"
    
    def add_evidence(self, evidence: Evidence) -> "Claim":
        self.evidences.append(evidence)
        return self
    
    def get_confidence(self) -> EvidenceConfidence:
        if not self.evidences:
            return EvidenceConfidence.LOW
        confidences = [e.confidence for e in self.evidences]
        if EvidenceConfidence.HIGH in confidences:
            return EvidenceConfidence.HIGH
        if EvidenceConfidence.MEDIUM in confidences:
            return EvidenceConfidence.MEDIUM
        return EvidenceConfidence.LOW


@dataclass
class Entity:
    """An entity in the knowledge graph."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    entity_type: EntityType = EntityType.CONCEPT
    description: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    related_claims: List[str] = field(default_factory=list)  # Claim IDs
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.entity_type.value,
            "description": self.description,
            "attributes": self.attributes,
        }


@dataclass
class Relationship:
    """A relationship between two entities."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_entity_id: str = ""
    target_entity_id: str = ""
    relation_type: str = ""  # depends-on, implements, extends, contradicts, etc.
    description: str = ""
    evidence_ids: List[str] = field(default_factory=list)


@dataclass
class KnowledgeGraph:
    """The knowledge graph storing entities and relationships."""
    entities: Dict[str, Entity] = field(default_factory=dict)
    relationships: List[Relationship] = field(default_factory=list)
    
    def add_entity(self, entity: Entity) -> "KnowledgeGraph":
        self.entities[entity.id] = entity
        return self
    
    def add_relationship(self, rel: Relationship) -> "KnowledgeGraph":
        self.relationships.append(rel)
        return self
    
    def get_entity(self, entity_id: str) -> Optional[Entity]:
        return self.entities.get(entity_id)
    
    def find_entities_by_name(self, name: str) -> List[Entity]:
        return [e for e in self.entities.values() if name.lower() in e.name.lower()]
    
    def get_neighbors(self, entity_id: str) -> List[Entity]:
        """Get all entities connected to the given entity."""
        neighbors = []
        neighbor_ids = set()
        for rel in self.relationships:
            if rel.source_entity_id == entity_id:
                neighbor_ids.add(rel.target_entity_id)
            elif rel.target_entity_id == entity_id:
                neighbor_ids.add(rel.source_entity_id)
        for nid in neighbor_ids:
            if nid in self.entities:
                neighbors.append(self.entities[nid])
        return neighbors


@dataclass
class ArchitectureDiagram:
    """Represents an architecture diagram."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    diagram_type: str = "mermaid"  # mermaid, excalidraw, dot, etc.
    content: str = ""  # The diagram definition
    description: str = ""
    layers: List[str] = field(default_factory=list)  # logical, physical, data, etc.
    
    def render_mermaid(self) -> str:
        """Render as Mermaid diagram."""
        if self.diagram_type == "mermaid":
            return f"```mermaid\n{self.content}\n```"
        return self.content


@dataclass
class Blueprint:
    """Implementation blueprint generated from understanding."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    overview: str = ""
    components: List[Dict[str, Any]] = field(default_factory=list)
    code_stubs: Dict[str, str] = field(default_factory=dict)  # filename -> code
    test_plan: List[Dict[str, Any]] = field(default_factory=list)
    migration_steps: List[str] = field(default_factory=list)
    risks: List[Dict[str, str]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    """Complete result of analyzing an idea."""
    query: str = ""
    claims: List[Claim] = field(default_factory=list)
    knowledge_graph: KnowledgeGraph = field(default_factory=KnowledgeGraph)
    diagrams: List[ArchitectureDiagram] = field(default_factory=list)
    blueprint: Optional[Blueprint] = None
    gaps: List[str] = field(default_factory=list)  # Identified knowledge gaps
    reasoning_chain: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def evidence(self) -> List[Evidence]:
        """Get all evidence from all claims."""
        all_evidence = []
        for claim in self.claims:
            all_evidence.extend(claim.evidences)
        return all_evidence
    
    @property
    def architecture(self) -> List[ArchitectureDiagram]:
        """Get architecture diagrams."""
        return self.diagrams
