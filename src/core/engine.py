"""
TechIntel Platform - Core Engine

The core engine orchestrates the full pipeline from idea to blueprint.
"""

from typing import List, Optional, Dict, Any
from .models import (
    AnalysisResult, Claim, Evidence, Source, Entity, 
    Relationship, KnowledgeGraph, ArchitectureDiagram, 
    Blueprint, EntityType, EvidenceConfidence
)


class TechIntel:
    """
    Main platform class that coordinates all components.
    
    Transforms: IDEA → RESEARCH → EVIDENCE → UNDERSTANDING → ARCHITECTURE → BLUEPRINT
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.knowledge_graph = KnowledgeGraph()
        
    def analyze(self, query: str) -> AnalysisResult:
        """
        Analyze a technical question or idea.
        
        Args:
            query: The technical question or idea to analyze
            
        Returns:
            AnalysisResult with claims, evidence, diagrams, and blueprint
        """
        result = AnalysisResult(query=query)
        
        # Phase 1: Research - gather information from multiple sources
        research_phase = self._research(query)
        result.reasoning_chain.append(f"Research completed: {len(research_phase)} sources analyzed")
        
        # Phase 2: Extract evidence and create claims
        for source_data in research_phase:
            claim = self._extract_claim(source_data, query)
            if claim:
                result.claims.append(claim)
                
        result.reasoning_chain.append(f"Evidence extracted: {len(result.claims)} claims created")
        
        # Phase 3: Build knowledge graph from claims
        self._build_knowledge_graph(result, query)
        result.reasoning_chain.append(
            f"Knowledge graph built: {len(self.knowledge_graph.entities)} entities, "
            f"{len(self.knowledge_graph.relationships)} relationships"
        )
        
        # Phase 4: Detect gaps in understanding
        result.gaps = self._detect_gaps(result, query)
        result.reasoning_chain.append(f"Gaps identified: {len(result.gaps)} areas need more research")
        
        # Phase 5: Generate architecture visualization
        result.diagrams = self._generate_architecture(result, query)
        result.reasoning_chain.append(f"Architecture diagrams generated: {len(result.diagrams)} views")
        
        # Phase 6: Create implementation blueprint
        result.blueprint = self._generate_blueprint(result, query)
        result.reasoning_chain.append("Implementation blueprint created")
        
        return result
    
    def _research(self, query: str) -> List[Dict[str, Any]]:
        """
        Research phase: gather information from multiple sources.
        
        In a full implementation, this would:
        - Search academic papers
        - Clone and analyze GitHub repositories
        - Extract API documentation
        - Parse RFCs and specifications
        - Query knowledge bases
        
        For now, returns placeholder structure.
        """
        # TODO: Integrate with research engines
        # - src/research/paper_parser.py
        # - src/research/repo_analyzer.py
        # - src/research/api_docs_extractor.py
        # - src/research/spec_parser.py
        
        return []
    
    def _extract_claim(self, source_data: Dict[str, Any], query: str) -> Optional[Claim]:
        """
        Extract a claim with evidence from source data.
        """
        # TODO: Implement claim extraction with evidence attribution
        return None
    
    def _build_knowledge_graph(self, result: AnalysisResult, query: str) -> None:
        """
        Build knowledge graph from extracted claims.
        
        Extracts entities and relationships from claims.
        """
        # Auto-extract entities from the query if no claims exist
        if not result.claims:
            # Parse query to identify potential entities
            words = query.replace("?", "").replace(",", "").split()
            
            # Identify key technical terms (simplified heuristic)
            tech_terms = []
            skip_words = {"how", "does", "what", "is", "are", "the", "a", "an", "in", "on", "for", 
                         "to", "of", "and", "or", "build", "design", "create", "make", "work"}
            
            i = 0
            while i < len(words):
                word = words[i].lower()
                if word not in skip_words:
                    # Check for multi-word terms
                    if i + 1 < len(words) and words[i+1].lower() not in skip_words:
                        term = f"{words[i]} {words[i+1]}"
                        tech_terms.append(term)
                        i += 2
                    else:
                        tech_terms.append(words[i])
                        i += 1
                else:
                    i += 1
            
            # Create entities from identified terms
            entity_types = {
                "kubernetes": EntityType.SYSTEM,
                "pod": EntityType.CONCEPT,
                "scheduling": EntityType.ALGORITHM,
                "rate limiter": EntityType.SYSTEM,
                "distributed": EntityType.CONCEPT,
                "cache": EntityType.SYSTEM,
                "consensus": EntityType.ALGORITHM,
                "websocket": EntityType.PROTOCOL,
                "chat": EntityType.SYSTEM,
                "real-time": EntityType.CONCEPT,
                "api": EntityType.API,
                "database": EntityType.SYSTEM,
                "service": EntityType.SYSTEM,
                "module": EntityType.CONCEPT,
                "component": EntityType.CONCEPT,
                "system": EntityType.SYSTEM,
                "protocol": EntityType.PROTOCOL,
                "algorithm": EntityType.ALGORITHM,
            }
            
            for term in tech_terms[:10]:  # Limit to 10 entities
                term_lower = term.lower()
                entity_type = EntityType.CONCEPT
                
                # Match against known types
                for keyword, etype in entity_types.items():
                    if keyword in term_lower:
                        entity_type = etype
                        break
                
                # Also check query context for type hints
                if "design" in query.lower() or "build" in query.lower():
                    if entity_type == EntityType.CONCEPT:
                        entity_type = EntityType.SYSTEM
                
                entity = Entity(
                    name=term.title(),
                    entity_type=entity_type,
                    description=f"Key concept extracted from: {query}",
                    attributes={"source": "query_analysis"}
                )
                self.knowledge_graph.add_entity(entity)
                result.knowledge_graph.add_entity(entity)
        
        # Add relationships between consecutive entities
        entities_list = list(result.knowledge_graph.entities.values())
        for i in range(len(entities_list) - 1):
            rel = Relationship(
                source_entity_id=entities_list[i].id,
                target_entity_id=entities_list[i+1].id,
                relation_type="related_to",
                description=f"Relationship derived from query context"
            )
            self.knowledge_graph.add_relationship(rel)
            result.knowledge_graph.add_relationship(rel)
    
    def _detect_gaps(self, result: AnalysisResult, query: str) -> List[str]:
        """
        Detect gaps in current understanding.
        
        Identifies areas where more research is needed.
        """
        gaps = []
        
        # Check if we have enough entities
        if len(result.knowledge_graph.entities) < 3:
            gaps.append("Limited entity extraction - consider providing more context or specific technical terms")
        
        # Check for missing evidence
        if not result.claims:
            gaps.append("No evidence-backed claims generated - connect to research sources for verification")
        
        # Query-specific gap detection
        query_lower = query.lower()
        if "distributed" in query_lower and "consensus" not in query_lower and "coordination" not in query_lower:
            gaps.append("Distributed systems topic may need consensus/coordination mechanism details")
        
        if "security" not in query_lower and ("api" in query_lower or "service" in query_lower):
            gaps.append("Security considerations not explicitly addressed")
        
        if "performance" not in query_lower and "scalability" not in query_lower:
            if "system" in query_lower or "architecture" in query_lower:
                gaps.append("Performance and scalability aspects may need exploration")
        
        return gaps
    
    def _generate_architecture(self, result: AnalysisResult, query: str) -> List[ArchitectureDiagram]:
        """
        Generate architecture diagrams from understanding.
        """
        diagrams = []
        
        # Generate a system context diagram based on entities
        entities = list(result.knowledge_graph.entities.values())
        
        if entities:
            # Create Mermaid graph from entities
            mermaid_lines = ["graph TD"]
            
            for entity in entities:
                node_id = entity.id.replace("-", "_")
                label = entity.name.replace(" ", "_")
                
                # Style based on entity type
                if entity.entity_type == EntityType.SYSTEM:
                    mermaid_lines.append(f"    {node_id}[{label}]:::system")
                elif entity.entity_type == EntityType.PROTOCOL:
                    mermaid_lines.append(f"    {node_id}({label}):::protocol")
                elif entity.entity_type == EntityType.ALGORITHM:
                    mermaid_lines.append(f"    {node_id}{{{label}}}:::algorithm")
                else:
                    mermaid_lines.append(f"    {node_id}[{label}]")
            
            # Add relationships
            for rel in result.knowledge_graph.relationships:
                src_id = rel.source_entity_id.replace("-", "_")
                tgt_id = rel.target_entity_id.replace("-", "_")
                mermaid_lines.append(f"    {src_id} -- {rel.relation_type} --> {tgt_id}")
            
            # Add styles
            mermaid_lines.extend([
                "    classDef system fill:#e1f5fe,stroke:#01579b",
                "    classDef protocol fill:#fff3e0,stroke:#e65100",
                "    classDef algorithm fill:#f3e5f5,stroke:#4a148c",
            ])
            
            diagrams.append(ArchitectureDiagram(
                title="System Context",
                diagram_type="mermaid",
                content="\n".join(mermaid_lines),
                description="High-level system architecture showing key components and relationships"
            ))
        
        return diagrams
    
    def _generate_blueprint(self, result: AnalysisResult, query: str) -> Optional[Blueprint]:
        """
        Generate implementation blueprint.
        """
        from src.blueprint.generator import BlueprintGenerator, Component as BPComponent
        
        gen = BlueprintGenerator()
        
        # Create components from entities
        for entity in result.knowledge_graph.entities.values():
            if entity.entity_type in [EntityType.SYSTEM, EntityType.API]:
                comp = BPComponent(
                    name=entity.name,
                    description=entity.description,
                    component_type=entity.entity_type.value,
                    responsibilities=[f"Handle {entity.name.lower()} operations"],
                    technology_stack=["Python", "asyncio"]
                )
                gen.add_component(comp)
        
        # If no components created, add a default one
        if not gen.components:
            default_name = query.split()[0].title() + "System"
            comp = BPComponent(
                name=default_name,
                description=f"Main system for: {query}",
                component_type="system",
                responsibilities=["Core functionality", "API endpoints", "Data management"],
                technology_stack=["Python", "FastAPI", "PostgreSQL", "Redis"]
            )
            gen.add_component(comp)
        
        # Generate test plans and risks
        test_plans = gen.generate_test_plan()
        risks = gen.identify_risks()
        
        # Create Blueprint object
        blueprint = Blueprint(
            title=f"Implementation Blueprint: {query}",
            overview=f"Blueprint generated for: {query}",
            components=[c.to_dict() for c in gen.components],
            test_plan=[t.to_dict() for t in test_plans],
            risks=[r.to_dict() for r in risks],
        )
        
        return blueprint
    
    def add_source(self, source_type: str, **kwargs) -> Source:
        """Add a new information source to the platform."""
        source = Source(
            source_type=source_type,
            metadata=kwargs
        )
        return source
    
    def query_knowledge_graph(self, entity_name: str) -> List[Entity]:
        """Query the knowledge graph for entities."""
        return self.knowledge_graph.find_entities_by_name(entity_name)
    
    def get_related_entities(self, entity_id: str) -> List[Entity]:
        """Get entities related to a given entity."""
        return self.knowledge_graph.get_neighbors(entity_id)
