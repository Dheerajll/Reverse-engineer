# TechIntel Platform

A genuine technical intelligence platform for deep engineering understanding.

## Vision

Transform: **IDEA → RESEARCH → EVIDENCE → UNDERSTANDING → ARCHITECTURE → IMPLEMENTATION BLUEPRINT**

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      TECHINTEL PLATFORM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   RESEARCH   │  │  KNOWLEDGE   │  │    CODE INTELLIGENCE │   │
│  │    ENGINE    │  │    GRAPH     │  │       ENGINE         │   │
│  │              │  │              │  │                      │   │
│  │ • Paper Parse│  │ • Entities   │  │ • AST Analysis       │   │
│  │ • Repo Clone │  │ • Relations  │  │ • Call Graphs        │   │
│  │ • API Docs   │  │ • Citations  │  │ • Data Flow          │   │
│  │ • Spec Extract│ │ • Evidence   │  │ • Type Inference     │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘   │
│         │                 │                      │               │
│         └─────────────────┼──────────────────────┘               │
│                           │                                      │
│                  ┌────────▼────────┐                             │
│                  │  EVIDENCE CORE  │                             │
│                  │                 │                             │
│                  │ • Source Links  │                             │
│                  │ • Code Snippets │                             │
│                  │ • Confidence    │                             │
│                  │ • Provenance    │                             │
│                  └────────┬────────┘                             │
│                           │                                      │
│         ┌─────────────────┼──────────────────┐                   │
│         │                 │                  │                   │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐           │
│  │ UNDERSTANDING│  │ ARCHITECTURE │  │   BLUEPRINT  │           │
│  │    LAYER     │  │   VISUALIZER │  │   GENERATOR  │           │
│  │              │  │              │  │              │           │
│  │ • Synthesis  │  │ • Diagrams   │  │ • Code Stubs │           │
│  │ • Gap Detect │  │ • Mermaid    │  │ • Test Plans │           │
│  │ • Q&A        │  │ • Excalidraw │  │ • Migration  │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Core Modules

### 1. Research Engine (`src/research/`)
- Academic paper parsing and summarization
- GitHub repository cloning and analysis
- API documentation extraction
- RFC/protocol specification parsing
- Multi-source evidence gathering

### 2. Knowledge Graph (`src/knowledge/`)
- Entity extraction (concepts, systems, APIs, algorithms)
- Relationship mapping (depends-on, implements, extends, contradicts)
- Citation tracking and provenance
- Temporal evolution of ideas

### 3. Code Intelligence Engine (`src/code_intel/`)
- AST parsing for multiple languages
- Call graph construction
- Data flow analysis
- Type inference and interface discovery
- Cross-repository linking

### 4. Evidence Core (`src/evidence/`)
- Source attribution for every claim
- Confidence scoring
- Contradiction detection
- Quote and snippet management

### 5. Understanding Layer (`src/core/`)
- Query comprehension
- Gap detection in knowledge
- Synthesis engine
- Explainable reasoning chains

### 6. Architecture Visualizer (`src/visualization/`)
- Mermaid diagram generation
- Excalidraw scene export
- Interactive architecture exploration
- Layered views (logical, physical, data)

### 7. Blueprint Generator (`src/blueprint/`)
- Implementation scaffolding
- Test plan generation
- Migration strategies
- Risk assessment

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the platform
python -m src.main
```

## Example Workflow

```python
from techintel import TechIntel

platform = TechIntel()

# Start with an idea
idea = "How does Raft consensus work compared to Paxos?"

# Get research-backed understanding
result = platform.analyze(idea)

# Access structured outputs
print(result.evidence)      # Source-backed claims
print(result.architecture)  # System diagrams
print(result.blueprint)     # Implementation guide
```

## Design Principles

1. **Evidence-Backed**: Every claim links to sources
2. **Explainable**: Reasoning chains are transparent
3. **Modular**: Components are independently testable
4. **Extensible**: New analyzers plug in easily
5. **Reproducible**: Analyses can be re-run and verified

## License

MIT