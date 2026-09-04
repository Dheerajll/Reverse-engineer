"""
TechIntel Platform - Test Suite

Tests for core functionality across all modules.
"""

import pytest
from src.core.models import (
    Source, Evidence, Claim, Entity, Relationship,
    KnowledgeGraph, ArchitectureDiagram, Blueprint, 
    EntityType, EvidenceConfidence
)
from src.knowledge.graph import KnowledgeGraph as GraphKnowledge, GraphNode, GraphEdge
from src.visualization.diagrams import (
    ArchitectureVisualizer, DiagramNode, DiagramEdge,
    generate_sequence_diagram, generate_flowchart
)
from src.blueprint.generator import (
    BlueprintGenerator, Component, CodeStub, TestCase,
    MigrationStep, Risk
)


class TestCoreModels:
    """Test core data models."""
    
    def test_source_creation(self):
        """Test creating a Source object."""
        source = Source(
            url="https://example.com/paper.pdf",
            title="Example Paper",
            source_type="paper"
        )
        assert source.url == "https://example.com/paper.pdf"
        assert source.title == "Example Paper"
        assert source.source_type == "paper"
        assert source.id is not None
    
    def test_evidence_creation(self):
        """Test creating an Evidence object."""
        source = Source(url="https://example.com", title="Test")
        evidence = Evidence(
            content="This is a claim",
            source=source,
            confidence=EvidenceConfidence.HIGH,
            quote="Direct quote from source"
        )
        assert evidence.content == "This is a claim"
        assert evidence.confidence == EvidenceConfidence.HIGH
        assert evidence.quote == "Direct quote from source"
    
    def test_claim_with_evidence(self):
        """Test creating a Claim with evidence."""
        claim = Claim(statement="Technical statement")
        evidence = Evidence(content="Supporting evidence")
        claim.add_evidence(evidence)
        
        assert len(claim.evidences) == 1
        assert claim.get_confidence() == EvidenceConfidence.MEDIUM
        
        # Add high confidence evidence
        high_evidence = Evidence(content="Strong evidence", confidence=EvidenceConfidence.HIGH)
        claim.add_evidence(high_evidence)
        assert claim.get_confidence() == EvidenceConfidence.HIGH
    
    def test_entity_creation(self):
        """Test creating entities."""
        entity = Entity(
            name="Raft Consensus",
            entity_type=EntityType.ALGORITHM,
            description="A consensus algorithm for managing a replicated log"
        )
        assert entity.name == "Raft Consensus"
        assert entity.entity_type == EntityType.ALGORITHM
        assert entity.to_dict()["type"] == "algorithm"
    
    def test_knowledge_graph_operations(self):
        """Test knowledge graph operations."""
        kg = KnowledgeGraph()
        
        # Add entities
        entity1 = Entity(name="System A", entity_type=EntityType.SYSTEM)
        entity2 = Entity(name="System B", entity_type=EntityType.SYSTEM)
        kg.add_entity(entity1)
        kg.add_entity(entity2)
        
        # Add relationship
        rel = Relationship(
            source_entity_id=entity1.id,
            target_entity_id=entity2.id,
            relation_type="communicates-with"
        )
        kg.add_relationship(rel)
        
        assert len(kg.entities) == 2
        assert len(kg.relationships) == 1
        
        # Query neighbors
        neighbors = kg.get_neighbors(entity1.id)
        assert len(neighbors) == 1
        assert neighbors[0].name == "System B"


class TestKnowledgeGraph:
    """Test knowledge graph module."""
    
    def test_graph_node_creation(self):
        """Test creating graph nodes."""
        node = GraphNode(
            id="node1",
            label="Consensus Algorithm",
            node_type="algorithm",
            properties={"complexity": "O(n)"}
        )
        assert node.label == "Consensus Algorithm"
        assert node.to_dict()["properties"]["complexity"] == "O(n)"
    
    def test_graph_edge_creation(self):
        """Test creating graph edges."""
        edge = GraphEdge(
            id="edge1",
            source_id="node1",
            target_id="node2",
            relation_type="implements"
        )
        assert edge.relation_type == "implements"
    
    def test_graph_path_finding(self):
        """Test finding paths in the graph."""
        graph = GraphKnowledge()
        
        # Create a chain: A -> B -> C
        graph.add_node("A", "Node A", "concept")
        graph.add_node("B", "Node B", "concept")
        graph.add_node("C", "Node C", "concept")
        graph.add_edge("e1", "A", "B", "relates-to")
        graph.add_edge("e2", "B", "C", "relates-to")
        
        paths = graph.find_path("A", "C")
        assert len(paths) > 0
        assert paths[0] == ["A", "B", "C"]
    
    def test_graph_mermaid_export(self):
        """Test exporting graph to Mermaid format."""
        graph = GraphKnowledge()
        graph.add_node("n1", "Component A", "service")
        graph.add_node("n2", "Component B", "database")
        graph.add_edge("e1", "n1", "n2", "depends-on")
        
        mermaid = graph.to_mermaid()
        assert "graph TD" in mermaid
        assert "Component_A" in mermaid  # Spaces are replaced with underscores
        assert "depends-on" in mermaid


class TestVisualization:
    """Test visualization module."""
    
    def test_architecture_visualizer_basic(self):
        """Test basic architecture visualization."""
        viz = ArchitectureVisualizer()
        viz.set_title("System Architecture")
        
        node = DiagramNode(
            id="api",
            label="API Gateway",
            node_type="rounded"
        )
        viz.add_node(node)
        
        mermaid = viz.to_mermaid()
        assert "System Architecture" in mermaid
        assert "API Gateway" in mermaid
    
    def test_system_diagram_generation(self):
        """Test generating system diagrams from components."""
        viz = ArchitectureVisualizer()
        
        components = [
            {"name": "Web App", "type": "service", "dependencies": ["Database"]},
            {"name": "Database", "type": "database", "dependencies": []},
        ]
        
        mermaid = viz.generate_system_diagram(components)
        assert "Web App" in mermaid
        assert "Database" in mermaid
        assert "comp_Web_App" in mermaid  # Check node reference exists
    
    def test_sequence_diagram(self):
        """Test sequence diagram generation."""
        actors = ["Client", "Server", "Database"]
        messages = [
            {"from": "Client", "to": "Server", "message": "HTTP Request"},
            {"from": "Server", "to": "Database", "message": "Query"},
            {"from": "Database", "to": "Server", "message": "Results"},
            {"from": "Server", "to": "Client", "message": "Response"},
        ]
        
        diagram = generate_sequence_diagram(actors, messages)
        assert "sequenceDiagram" in diagram
        assert "HTTP Request" in diagram
    
    def test_flowchart_generation(self):
        """Test flowchart generation."""
        steps = [
            {"id": "start", "label": "Start", "type": "start", "next": "process"},
            {"id": "process", "label": "Process Data", "type": "process", "next": "end"},
            {"id": "end", "label": "End", "type": "end", "next": []},
        ]
        
        flowchart = generate_flowchart(steps)
        assert "graph TD" in flowchart
        assert "Start" in flowchart


class TestBlueprintGenerator:
    """Test blueprint generator module."""
    
    def test_component_creation(self):
        """Test creating components."""
        component = Component(
            name="Auth Service",
            description="Handles user authentication",
            component_type="service",
            responsibilities=["Validate credentials", "Issue tokens"],
            technology_stack=["Python", "JWT", "Redis"]
        )
        
        assert component.name == "Auth Service"
        assert len(component.responsibilities) == 2
        assert "JWT" in component.technology_stack
    
    def test_python_scaffold_generation(self):
        """Test Python code scaffold generation."""
        generator = BlueprintGenerator()
        
        component = Component(
            name="Data Processor",
            description="Processes incoming data streams",
            component_type="module",
            responsibilities=["Parse input", "Transform data", "Store results"]
        )
        
        stubs = generator.generate_python_scaffold(component)
        
        assert len(stubs) >= 1
        assert any(".py" in s.filename for s in stubs)
        assert "class DataProcessor" in stubs[0].content
    
    def test_test_plan_generation(self):
        """Test test plan generation."""
        generator = BlueprintGenerator()
        
        component = Component(
            name="Payment Service",
            description="Handles payment processing",
            component_type="service",
            dependencies=["Stripe API"]
        )
        generator.add_component(component)
        
        tests = generator.generate_test_plan()
        
        assert len(tests) > 0
        assert any(t.test_type == "unit" for t in tests)
        assert any(t.test_type == "integration" for t in tests)
    
    def test_risk_assessment(self):
        """Test risk identification and severity calculation."""
        risk = Risk(
            id="RISK-001",
            category="technical",
            description="High complexity integration",
            likelihood="high",
            impact="high",
            mitigation="Thorough testing"
        )
        
        assert risk.severity == "critical"
        
        medium_risk = Risk(
            id="RISK-002",
            category="operational",
            description="Minor delay possible",
            likelihood="low",
            impact="medium"
        )
        assert medium_risk.severity == "medium"
    
    def test_blueprint_export(self):
        """Test blueprint export formats."""
        generator = BlueprintGenerator()
        
        component = Component(
            name="Test Component",
            description="A test component",
            component_type="library"
        )
        generator.add_component(component)
        
        # Test dict export
        blueprint_dict = generator.to_dict()
        assert "components" in blueprint_dict
        assert "generated_at" in blueprint_dict
        
        # Test markdown export
        md = generator.to_markdown()
        assert "# Implementation Blueprint" in md
        assert "Test Component" in md


class TestIntegration:
    """Integration tests for the platform."""
    
    def test_platform_initialization(self):
        """Test that the platform can be initialized."""
        from src.core.engine import TechIntel
        
        platform = TechIntel()
        assert platform is not None
        assert platform.config == {}
    
    def test_analysis_result_structure(self):
        """Test that analysis results have expected structure."""
        from src.core.engine import TechIntel
        from src.core.models import AnalysisResult
        
        platform = TechIntel()
        result = platform.analyze("Test query")
        
        assert isinstance(result, AnalysisResult)
        assert result.query == "Test query"
        assert hasattr(result, 'claims')
        assert hasattr(result, 'knowledge_graph')
        assert hasattr(result, 'diagrams')
        assert hasattr(result, 'blueprint')
        assert hasattr(result, 'gaps')
        assert hasattr(result, 'reasoning_chain')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
