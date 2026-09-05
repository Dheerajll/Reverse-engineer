# TechIntel Platform - Technical Intelligence Pipeline

A genuine technical intelligence platform that helps engineers deeply understand how software systems, programming languages, AI systems, distributed systems, and engineering concepts actually work.

## Quick Start

```bash
# Run the complete pipeline with a single command
python -m src.cli "Your technical question or project idea" --verbose

# Examples
python -m src.cli "How does Kubernetes pod scheduling work?" --verbose
python -m src.cli "Design a distributed rate limiter" --output ./analysis
python -m src.cli "Build a real-time chat application with WebSocket" --verbose --no-code
```

## What It Does

Transforms your technical questions through a 6-phase pipeline:

```
IDEA → RESEARCH → EVIDENCE → UNDERSTANDING → ARCHITECTURE → BLUEPRINT
```

### Phase 1: RESEARCH
- Analyzes your query for key technical concepts
- (Future) Integrates with academic papers, GitHub repos, API docs, RFCs

### Phase 2: EVIDENCE & CLAIMS  
- Extracts evidence-backed claims from sources
- Assigns confidence levels to each claim

### Phase 3: KNOWLEDGE GRAPH
- Identifies entities (systems, algorithms, protocols, concepts)
- Maps relationships between entities
- Exports to Mermaid diagram format

### Phase 4: ARCHITECTURE DIAGRAMS
- Generates system context diagrams
- Creates visual representations of component relationships
- Outputs Mermaid syntax for rendering

### Phase 5: IMPLEMENTATION BLUEPRINT
- Generates component specifications
- Creates code scaffolds (Python)
- Produces test plans
- Identifies risks and mitigations

### Phase 6: KNOWLEDGE GAPS
- Detects missing information
- Highlights areas needing more research
- Prioritizes gaps by importance

## Command-Line Interface

### Basic Usage

```bash
python -m src.cli "Your topic here"
```

### Options

| Option | Description |
|--------|-------------|
| `topic` | Technical question or project idea (required) |
| `-o, --output DIR` | Output directory (default: `./output`) |
| `-v, --verbose` | Print detailed progress |
| `--no-code` | Skip code scaffold generation |
| `--no-diagrams` | Skip diagram generation |
| `--no-research` | Skip research phase |
| `--json` | Output only JSON (machine-readable) |

### Examples

```bash
# Full analysis with verbose output
python -m src.cli "How does Raft consensus work?" --verbose

# Save to custom directory
python -m src.cli "Design a distributed cache with Redis" --output ./cache-analysis

# Generate report without code stubs
python -m src.cli "Microservices architecture patterns" --no-code

# Machine-readable JSON output
python -m src.cli "WebSocket protocol internals" --json > report.json

# Combine options
python -m src.cli "Build a real-time chat application" \
  --verbose \
  --output ./chat-app \
  --no-research
```

## Output Files

The platform generates several artifacts in the output directory:

```
output/
├── report.json              # Complete structured report
├── report.md                # Markdown implementation blueprint
├── diagram_system_context.mmd  # Mermaid architecture diagram
└── code/
    ├── component_name.py    # Python code scaffold
    └── test_component_name.py  # Test suite scaffold
```

### report.json Structure

```json
{
  "topic": "Your analyzed topic",
  "claims": [...],           # Evidence-backed claims
  "knowledge_graph": {
    "entities": [...],       # Identified entities
    "relationships": [...],  # Entity relationships
    "mermaid": "..."         # Mermaid diagram syntax
  },
  "diagrams": {...},         # Architecture diagrams
  "blueprint": {
    "components": [...],     # System components
    "code_stubs": [...],     # Generated code
    "test_plans": [...],     # Test specifications
    "risks": [...]           # Risk assessments
  },
  "gaps": [...],             # Knowledge gaps
  "summary": "..."           # Executive summary
}
```

## Use Cases

### 1. Understanding Complex Systems
```bash
python -m src.cli "How does Kubernetes scheduling work?" --verbose
```
Generates: Entity graph of K8s components, architecture diagrams, implementation blueprint

### 2. Designing New Systems
```bash
python -m src.cli "Design a distributed rate limiter with Redis"
```
Generates: Component specs, code scaffolds, test plans, risk assessment

### 3. Learning Protocols
```bash
python -m src.cli "How does the Raft consensus algorithm work?"
```
Generates: Algorithm entity graph, flow diagrams, implementation guide

### 4. Architecture Research
```bash
python -m src.cli "Microservices vs monolith for real-time analytics"
```
Generates: Comparative entity graphs, architecture patterns, migration considerations

## Integration Points

The platform is designed to be extended with real data sources:

- **Research Engine**: Connect to arXiv API, GitHub API, ReadTheDocs
- **Code Intelligence**: Integrate tree-sitter parsers for AST analysis
- **Visualization**: Export to Excalidraw, GraphViz, Neo4j
- **Knowledge Graph**: Persist to Neo4j or other graph databases

## Architecture

```
src/
├── cli.py                 # Unified command-line interface
├── core/
│   ├── engine.py          # Main orchestration engine
│   └── models.py          # Data models (Claim, Evidence, Entity, etc.)
├── research/
│   └── engine.py          # Multi-source research coordination
├── knowledge/
│   └── graph.py           # Knowledge graph with Mermaid export
├── code_intel/
│   └── engine.py          # Code analysis (AST, call graphs)
├── visualization/
│   └── diagrams.py        # Diagram generation (Mermaid, DOT)
└── blueprint/
    └── generator.py       # Implementation blueprint generation
```

## Future Enhancements

1. **Real Research Integration**
   - arXiv API for academic papers
   - GitHub API for repository analysis
   - RFC/IEEE spec parsers

2. **Advanced Code Intelligence**
   - tree-sitter integration for multi-language parsing
   - Call graph construction
   - Data flow analysis

3. **Enhanced Visualization**
   - Excalidraw scene export
   - Interactive D3.js diagrams
   - 3D architecture views

4. **Collaboration Features**
   - Shareable reports
   - Team knowledge graphs
   - Annotation and commenting

## License

MIT License - See LICENSE file for details

---

Built as an industrial-quality technical intelligence platform, not just another AI wrapper.
