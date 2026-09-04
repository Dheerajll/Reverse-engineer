"""
TechIntel Platform - Main Entry Point

Provides the main interface for running the platform.
"""

import sys
import json
from typing import Optional


def main():
    """Main entry point for the TechIntel platform."""
    print("=" * 60)
    print("  TechIntel Platform - Technical Intelligence Engine")
    print("=" * 60)
    print()
    print("Transform: IDEA → RESEARCH → EVIDENCE → UNDERSTANDING → ARCHITECTURE → BLUEPRINT")
    print()
    
    # Import core components
    try:
        from src.core.engine import TechIntel
        from src.core.models import (
            Claim, Evidence, Source, Entity, Relationship,
            KnowledgeGraph, ArchitectureDiagram, Blueprint, EntityType,
            EvidenceConfidence
        )
        from src.research.engine import ResearchEngine
        from src.knowledge.graph import KnowledgeGraph as GraphKnowledge
        from src.code_intel.engine import CodeIntelligenceEngine
        from src.visualization.diagrams import ArchitectureVisualizer
        from src.blueprint.generator import BlueprintGenerator
    except ImportError as e:
        print(f"Error importing modules: {e}")
        sys.exit(1)
    
    # Initialize platform
    print("Initializing platform components...")
    platform = TechIntel()
    print("✓ Core engine initialized")
    
    research_engine = ResearchEngine()
    print("✓ Research engine initialized")
    
    code_engine = CodeIntelligenceEngine()
    print("✓ Code intelligence engine initialized")
    
    visualizer = ArchitectureVisualizer()
    print("✓ Visualization module initialized")
    
    blueprint_gen = BlueprintGenerator()
    print("✓ Blueprint generator initialized")
    
    print()
    print("-" * 60)
    print("Platform ready. Example usage:")
    print("-" * 60)
    print()
    print("""
# Analyze a technical question
result = platform.analyze("How does Raft consensus work?")

# Access evidence-backed claims
for claim in result.claims:
    print(f"Claim: {claim.statement}")
    for evidence in claim.evidences:
        print(f"  Source: {evidence.source.url if evidence.source else 'N/A'}")

# View knowledge graph
kg = result.knowledge_graph
print(f"Entities: {len(kg.entities)}")
print(f"Relationships: {len(kg.relationships)}")

# Get architecture diagrams
for diagram in result.diagrams:
    print(diagram.render_mermaid())

# Generate implementation blueprint
blueprint = result.blueprint
if blueprint:
    print(f"Components: {[c['name'] for c in blueprint.components]}")
    """)
    
    print("-" * 60)
    print()
    print("Modules available:")
    print("  - src.core: Core models and engine")
    print("  - src.research: Multi-source research capabilities")
    print("  - src.knowledge: Knowledge graph management")
    print("  - src.code_intel: Code analysis and understanding")
    print("  - src.visualization: Architecture diagram generation")
    print("  - src.blueprint: Implementation blueprint generation")
    print()
    print("For documentation, see README.md")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
