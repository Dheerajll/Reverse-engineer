#!/usr/bin/env python3
"""
TechIntel CLI - Unified Command-Line Interface

Run the complete intelligence pipeline with a single command:
    python -m src.cli "Your technical question or project idea"
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from src.core.engine import TechIntel
from src.core.models import Source, Evidence, Claim, EvidenceConfidence
from src.research.engine import ResearchEngine, ResearchSource
from src.knowledge.graph import KnowledgeGraph
from src.visualization.diagrams import ArchitectureVisualizer, generate_sequence_diagram
from src.blueprint.generator import BlueprintGenerator, Component


def run_full_pipeline(
    topic: str,
    output_dir: Optional[str] = None,
    verbose: bool = False,
    include_code: bool = True,
    include_diagrams: bool = True,
    include_research: bool = True,
) -> dict:
    """
    Run the complete TechIntel pipeline from IDEA to BLUEPRINT.
    
    Args:
        topic: The technical question, concept, or project idea to analyze
        output_dir: Optional directory to save outputs (default: ./output)
        verbose: Print detailed progress
        include_code: Include code scaffolding in blueprint
        include_diagrams: Generate architecture diagrams
        include_research: Run research phase
    
    Returns:
        Dictionary containing all pipeline outputs
    """
    if verbose:
        print("=" * 70)
        print("TECHINTEL PLATFORM - Technical Intelligence Pipeline")
        print("=" * 70)
        print(f"\n📌 TOPIC: {topic}\n")
    
    # Initialize platform
    platform = TechIntel()
    
    results = {
        "topic": topic,
        "claims": [],
        "knowledge_graph": {},
        "diagrams": {},
        "blueprint": {},
        "gaps": [],
        "summary": ""
    }
    
    # ========== PHASE 1: RESEARCH ==========
    if verbose:
        print("🔍 PHASE 1: RESEARCH")
        print("-" * 40)
    
    if include_research:
        research_engine = ResearchEngine()
        # Simulate research sources based on topic keywords
        sources = research_engine.research(topic)
        
        if verbose:
            print(f"   Found {len(sources)} potential source types")
            for src in sources[:5]:  # Show first 5
                print(f"   • {src.source_type}: {src.title}")
    
    # Create simulated evidence based on topic analysis
    # In production, this would fetch real data from APIs
    evidence_items = platform.analyze(topic).evidence if hasattr(platform.analyze(topic), 'evidence') else []
    
    # If no real evidence, create placeholder based on topic decomposition
    if not evidence_items:
        evidence_items = [
            Evidence(
                content=f"Core concept analysis for: {topic}",
                source=Source(
                    url="https://example.com/analysis",
                    title="Platform Analysis",
                    source_type="analysis"
                ),
                confidence=EvidenceConfidence.MEDIUM,
                quote="Automated decomposition"
            )
        ]
    
    if verbose:
        print(f"   Generated {len(evidence_items)} evidence items\n")
    
    # ========== PHASE 2: EVIDENCE & CLAIMS ==========
    if verbose:
        print("📋 PHASE 2: EVIDENCE & CLAIMS")
        print("-" * 40)
    
    analysis_result = platform.analyze(topic)
    claims = analysis_result.claims
    
    if verbose:
        for i, claim in enumerate(claims[:5], 1):
            conf = claim.get_confidence().value
            print(f"   {i}. {claim.statement[:60]}... (confidence: {conf})")
        if len(claims) > 5:
            print(f"   ... and {len(claims) - 5} more claims")
    
    results["claims"] = [
        {
            "statement": c.statement,
            "confidence": c.get_confidence().value,
            "evidence_count": len(c.evidence),
            "tags": c.tags
        }
        for c in claims
    ]
    
    if verbose:
        print(f"   Total claims: {len(claims)}\n")
    
    # ========== PHASE 3: KNOWLEDGE GRAPH ==========
    if verbose:
        print("🕸️  PHASE 3: KNOWLEDGE GRAPH")
        print("-" * 40)
    
    kg = analysis_result.knowledge_graph
    
    if verbose:
        print(f"   Entities: {len(kg.entities)}")
        print(f"   Relationships: {len(kg.relationships)}")
        
        # Show sample entities
        for i, (eid, entity) in enumerate(list(kg.entities.items())[:5]):
            print(f"   • {entity.name} ({entity.entity_type.value})")
    
    # Convert to knowledge.graph.KnowledgeGraph for Mermaid export
    from src.knowledge.graph import KnowledgeGraph as SimpleKG
    
    simple_kg = SimpleKG()
    for eid, entity in kg.entities.items():
        simple_kg.add_node(eid, entity.name, entity.entity_type.value, entity.attributes)
    
    for rel in kg.relationships:
        simple_kg.add_edge(rel.id, rel.source_entity_id, rel.target_entity_id, rel.relation_type)
    
    results["knowledge_graph"] = {
        "entities": [
            {"id": eid, "name": e.name, "type": e.entity_type.value, "properties": e.attributes}
            for eid, e in kg.entities.items()
        ],
        "relationships": [
            {"from": r.source_entity_id, "to": r.target_entity_id, "type": r.relation_type}
            for r in kg.relationships
        ],
        "mermaid": simple_kg.to_mermaid() if kg.entities else "graph TD\n    Empty[No entities extracted]"
    }
    
    if verbose:
        print(f"   Mermaid diagram generated ({len(simple_kg.to_mermaid())} chars)\n")
    
    # ========== PHASE 4: ARCHITECTURE DIAGRAMS ==========
    if include_diagrams and verbose:
        print("📊 PHASE 4: ARCHITECTURE DIAGRAMS")
        print("-" * 40)
    
    diagrams = {}
    
    if include_diagrams:
        viz = ArchitectureVisualizer()
        
        # analysis_result.diagrams is a list of ArchitectureDiagram objects
        for diagram in analysis_result.diagrams:
            if diagram.diagram_type == "mermaid":
                diagrams[diagram.title.replace(" ", "_").lower()] = diagram.content
        
        # If no diagrams from analysis, create one from knowledge graph
        if not diagrams and kg.entities:
            diagrams["knowledge_graph"] = simple_kg.to_mermaid()
    
    results["diagrams"] = diagrams
    
    if verbose and diagrams:
        for dtype in diagrams.keys():
            print(f"   ✓ {dtype.capitalize()} diagram generated")
        print()
    
    # ========== PHASE 5: IMPLEMENTATION BLUEPRINT ==========
    if verbose:
        print("📐 PHASE 5: IMPLEMENTATION BLUEPRINT")
        print("-" * 40)
    
    blueprint_gen = BlueprintGenerator()
    
    # Auto-generate components from knowledge graph entities
    for eid, entity in list(kg.entities.items())[:10]:  # Limit to 10 components
        if entity.entity_type in ["service", "module", "component", "system", "database"]:
            component = Component(
                name=entity.name,
                description=entity.properties.get("description", f"Component derived from {entity.name}"),
                component_type=entity.entity_type,
                responsibilities=[f"Handle {entity.name.lower()} operations"],
                technology_stack=["Python", "asyncio"]  # Default stack
            )
            blueprint_gen.add_component(component)
    
    # Add default component if none were created
    if len(blueprint_gen.components) == 0:
        default_component = Component(
            name=f"{topic.split()[0].title()}System",
            description=f"Main system component for: {topic}",
            component_type="system",
            responsibilities=["Core functionality", "API endpoints", "Data management"],
            technology_stack=["Python", "FastAPI", "PostgreSQL", "Redis"]
        )
        blueprint_gen.add_component(default_component)
    
    # Generate blueprint outputs
    test_plans = blueprint_gen.generate_test_plan()
    risks = blueprint_gen.identify_risks()
    
    if include_code:
        code_stubs = []
        for comp in blueprint_gen.components:
            stubs = blueprint_gen.generate_python_scaffold(comp)
            code_stubs.extend(stubs)
        results["blueprint"]["code_stubs"] = [
            {"filename": s.filename, "content": s.content}
            for s in code_stubs
        ]
    
    results["blueprint"]["components"] = [
        {
            "name": c.name,
            "type": c.component_type,
            "description": c.description,
            "responsibilities": c.responsibilities,
            "tech_stack": c.technology_stack
        }
        for c in blueprint_gen.components
    ]
    
    results["blueprint"]["test_plans"] = [
        {"type": t.test_type, "description": t.description, "steps": t.steps}
        for t in test_plans
    ]
    
    results["blueprint"]["risks"] = [
        {"category": r.category, "risk": r.description, "mitigation": r.mitigation}
        for r in risks
    ]
    
    results["blueprint"]["markdown"] = blueprint_gen.to_markdown()
    
    if verbose:
        print(f"   Components: {len(blueprint_gen.components)}")
        print(f"   Test plans: {len(test_plans)}")
        print(f"   Risks identified: {len(risks)}")
        if include_code:
            print(f"   Code stubs generated: {len(code_stubs)}")
        print()
    
    # ========== PHASE 6: GAPS & SUMMARY ==========
    if verbose:
        print("⚠️  PHASE 6: KNOWLEDGE GAPS")
        print("-" * 40)
    
    gaps = analysis_result.gaps
    # Handle both string gaps and Gap objects
    results["gaps"] = []
    for g in gaps:
        if isinstance(g, str):
            results["gaps"].append({"area": "General", "description": g, "priority": "medium"})
        else:
            results["gaps"].append({"area": g.area, "description": g.description, "priority": g.priority.value})
    
    if verbose:
        if gaps:
            for gap in gaps[:5]:
                desc = gap.description if hasattr(gap, 'description') else gap
                print(f"   • [{hasattr(gap, 'priority') and gap.priority.value or 'medium'}] {hasattr(gap, 'area') and gap.area or 'General'}: {str(desc)[:50]}...")
        else:
            print("   No critical gaps identified")
        print()
    
    # Generate summary
    summary = f"""
# Technical Intelligence Report: {topic}

## Overview
Analyzed topic with {len(claims)} evidence-backed claims, 
{len(kg.entities)} knowledge entities, and {len(blueprint_gen.components)} blueprint components.

## Key Findings
"""
    for i, claim in enumerate(claims[:3], 1):
        summary += f"\n{i}. {claim.statement}"
    
    summary += f"\n\n## Next Steps\n"
    if gaps:
        summary += f"Address {len(gaps)} identified knowledge gaps before implementation.\n"
    summary += f"Review {len(test_plans)} test plans and {len(risks)} risk assessments in the blueprint."
    
    results["summary"] = summary
    
    # ========== SAVE OUTPUTS ==========
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            print(f"💾 SAVING OUTPUTS to {output_path}")
            print("-" * 40)
        
        # Save JSON report
        json_path = output_path / "report.json"
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)
        if verbose:
            print(f"   ✓ report.json")
        
        # Save Markdown report
        md_path = output_path / "report.md"
        with open(md_path, "w") as f:
            f.write(results["blueprint"]["markdown"])
        if verbose:
            print(f"   ✓ report.md")
        
        # Save individual diagrams
        for dtype, diagram_content in diagrams.items():
            diag_path = output_path / f"diagram_{dtype}.mmd"
            with open(diag_path, "w") as f:
                f.write(diagram_content)
            if verbose:
                print(f"   ✓ diagram_{dtype}.mmd")
        
        # Save code stubs
        if include_code and "code_stubs" in results["blueprint"]:
            code_dir = output_path / "code"
            code_dir.mkdir(exist_ok=True)
            for stub in results["blueprint"]["code_stubs"]:
                stub_path = code_dir / stub["filename"]
                stub_path.parent.mkdir(parents=True, exist_ok=True)
                with open(stub_path, "w") as f:
                    f.write(stub["content"])
            if verbose:
                print(f"   ✓ code/ ({len(results['blueprint']['code_stubs'])} files)")
        
        print()
    
    if verbose:
        print("=" * 70)
        print("✅ PIPELINE COMPLETE")
        print("=" * 70)
        print(summary)
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="TechIntel Platform - Technical Intelligence Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.cli "How does Raft consensus work?"
  python -m src.cli "Design a distributed cache system" --output ./raft-analysis
  python -m src.cli "Build a real-time chat application" --verbose --no-code
  python -m src.cli "Microservices architecture patterns" --output ./output --diagrams-only
        """
    )
    
    parser.add_argument(
        "topic",
        nargs="?",
        help="Technical question, concept, or project idea to analyze"
    )
    
    parser.add_argument(
        "-o", "--output",
        dest="output_dir",
        help="Output directory for reports and artifacts (default: ./output)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed progress information"
    )
    
    parser.add_argument(
        "--no-code",
        action="store_true",
        help="Skip code scaffold generation"
    )
    
    parser.add_argument(
        "--no-diagrams",
        action="store_true",
        help="Skip diagram generation"
    )
    
    parser.add_argument(
        "--no-research",
        action="store_true",
        help="Skip research phase (use only built-in knowledge)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output only JSON (suppress verbose output)"
    )
    
    args = parser.parse_args()
    
    # If no topic provided, show help
    if not args.topic:
        parser.print_help()
        print("\n❌ Error: Please provide a topic to analyze")
        print("   Example: python -m src.cli \"How does Kubernetes scheduling work?\"")
        sys.exit(1)
    
    # Set default output directory
    output_dir = args.output_dir or "./output"
    
    # Run pipeline
    try:
        results = run_full_pipeline(
            topic=args.topic,
            output_dir=None if args.json else output_dir,
            verbose=not args.json and args.verbose,
            include_code=not args.no_code,
            include_diagrams=not args.no_diagrams,
            include_research=not args.no_research
        )
        
        # If JSON-only mode, print results
        if args.json:
            print(json.dumps(results, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
