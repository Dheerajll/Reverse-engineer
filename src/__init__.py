# TechIntel Platform

"""
TechIntel is a genuine technical intelligence platform designed to help engineers 
deeply understand how software systems, programming languages, AI systems, operating 
systems, distributed systems, open-source projects, APIs, protocols, research papers, 
and engineering ideas actually work.
"""

__version__ = "0.1.0"
__author__ = "TechIntel Team"

from src.core.engine import TechIntel
from src.core.models import (
    Source, Evidence, Claim, Entity, Relationship,
    KnowledgeGraph, ArchitectureDiagram, Blueprint,
    EntityType, EvidenceConfidence, AnalysisResult
)

__all__ = [
    "TechIntel",
    "Source",
    "Evidence",
    "Claim",
    "Entity",
    "Relationship",
    "KnowledgeGraph",
    "ArchitectureDiagram",
    "Blueprint",
    "EntityType",
    "EvidenceConfidence",
    "AnalysisResult",
]
