"""
TechIntel Platform - Code Intelligence Engine

Provides deep code analysis capabilities:
- AST parsing for multiple languages
- Call graph construction
- Data flow analysis
- Type inference
- Cross-repository linking
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
import ast


@dataclass
class CodeSymbol:
    """Represents a code symbol (function, class, variable, etc.)."""
    id: str
    name: str
    symbol_type: str  # function, class, method, variable, interface, etc.
    file_path: str
    line_start: int
    line_end: int
    signature: Optional[str] = None
    docstring: Optional[str] = None
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    return_type: Optional[str] = None
    imports: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.symbol_type,
            "file": self.file_path,
            "lines": (self.line_start, self.line_end),
            "signature": self.signature,
            "docstring": self.docstring,
        }


@dataclass
class CallEdge:
    """Represents a call relationship between symbols."""
    caller_id: str
    callee_id: str
    call_site_line: int
    call_site_file: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "caller": self.caller_id,
            "callee": self.callee_id,
            "location": f"{self.call_site_file}:{self.call_site_line}",
        }


@dataclass
class DataFlowEdge:
    """Represents a data flow relationship."""
    source_id: str
    target_id: str
    variable_name: str
    flow_type: str  # assignment, parameter, return, field_access
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source_id,
            "target": self.target_id,
            "variable": self.variable_name,
            "type": self.flow_type,
        }


class LanguageParser(ABC):
    """Abstract base class for language-specific parsers."""
    
    @abstractmethod
    def parse_file(self, file_path: str, content: str) -> List[CodeSymbol]:
        """Parse a file and extract symbols."""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions."""
        pass


class PythonParser(LanguageParser):
    """
    Parser for Python code using AST.
    
    Extracts:
    - Functions and methods
    - Classes
    - Imports
    - Variable assignments
    - Type annotations
    """
    
    def parse_file(self, file_path: str, content: str) -> List[CodeSymbol]:
        """Parse Python file and extract symbols."""
        symbols = []
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return symbols
        
        # Extract classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                symbol = self._parse_class(node, file_path, content)
                symbols.append(symbol)
            
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                symbol = self._parse_function(node, file_path, content)
                symbols.append(symbol)
        
        return symbols
    
    def _parse_class(self, node: ast.ClassDef, file_path: str, content: str) -> CodeSymbol:
        """Parse a class definition."""
        bases = [self._get_name(base) for base in node.bases]
        
        return CodeSymbol(
            id=f"{file_path}:{node.name}:class",
            name=node.name,
            symbol_type="class",
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            signature=f"class {node.name}({', '.join(bases)})",
            docstring=ast.get_docstring(node),
        )
    
    def _parse_function(self, node: ast.FunctionDef, file_path: str, content: str) -> CodeSymbol:
        """Parse a function definition."""
        params = []
        for arg in node.args.args:
            param = {
                "name": arg.arg,
                "annotation": self._get_annotation(arg.annotation) if arg.annotation else None,
            }
            params.append(param)
        
        return_type = self._get_annotation(node.returns) if node.returns else None
        
        # Determine if it's a method (inside a class)
        symbol_type = "method" if self._is_method(node) else "function"
        
        return CodeSymbol(
            id=f"{file_path}:{node.name}:{symbol_type}",
            name=node.name,
            symbol_type=symbol_type,
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            signature=self._build_signature(node, params, return_type),
            docstring=ast.get_docstring(node),
            parameters=params,
            return_type=return_type,
        )
    
    def _get_name(self, node) -> str:
        """Get the name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return ""
    
    def _get_annotation(self, node) -> Optional[str]:
        """Get type annotation as string."""
        if node is None:
            return None
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_annotation(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_annotation(node.value)}[{self._get_annotation(node.slice)}]"
        return None
    
    def _build_signature(self, node, params: List[Dict], return_type: Optional[str]) -> str:
        """Build function signature string."""
        param_strs = [p["name"] + (f": {p['annotation']}" if p.get("annotation") else "") 
                      for p in params]
        ret_str = f" -> {return_type}" if return_type else ""
        return f"def {node.name}({', '.join(param_strs)}){ret_str}"
    
    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method (has self parameter)."""
        if node.args.args:
            first_arg = node.args.args[0].arg
            return first_arg in ("self", "cls")
        return False
    
    def get_supported_extensions(self) -> List[str]:
        return [".py", ".pyi"]


class CallGraphBuilder:
    """
    Build call graphs from parsed code symbols.
    """
    
    def __init__(self):
        self.symbols: Dict[str, CodeSymbol] = {}
        self.calls: List[CallEdge] = []
    
    def add_symbol(self, symbol: CodeSymbol) -> "CallGraphBuilder":
        """Add a symbol to the graph."""
        self.symbols[symbol.id] = symbol
        return self
    
    def add_symbols(self, symbols: List[CodeSymbol]) -> "CallGraphBuilder":
        """Add multiple symbols."""
        for symbol in symbols:
            self.add_symbol(symbol)
        return self
    
    def build_calls(self, file_path: str, content: str) -> List[CallEdge]:
        """
        Analyze code to find function calls.
        
        TODO: Implement proper call site analysis.
        """
        # Placeholder - would need full AST analysis
        return []
    
    def get_callers(self, symbol_id: str) -> List[CodeSymbol]:
        """Get all symbols that call this symbol."""
        caller_ids = {edge.caller_id for edge in self.calls if edge.callee_id == symbol_id}
        return [self.symbols[cid] for cid in caller_ids if cid in self.symbols]
    
    def get_callees(self, symbol_id: str) -> List[CodeSymbol]:
        """Get all symbols called by this symbol."""
        callee_ids = {edge.callee_id for edge in self.calls if edge.caller_id == symbol_id}
        return [self.symbols[cid] for cid in callee_ids if cid in self.symbols]
    
    def to_dict(self) -> Dict[str, Any]:
        """Export call graph as dictionary."""
        return {
            "symbols": {sid: s.to_dict() for sid, s in self.symbols.items()},
            "calls": [c.to_dict() for c in self.calls],
        }


class DataFlowAnalyzer:
    """
    Analyze data flow through code.
    
    Tracks:
    - Variable assignments
    - Parameter passing
    - Return values
    - Field accesses
    """
    
    def analyze(self, symbols: List[CodeSymbol], file_content: str) -> List[DataFlowEdge]:
        """Analyze data flow in code."""
        # TODO: Implement data flow analysis
        # Would use techniques like:
        # - Def-use chains
        # - SSA form conversion
        # - Points-to analysis
        return []


class CodeIntelligenceEngine:
    """
    Main code intelligence engine coordinating all analysis.
    """
    
    def __init__(self):
        self.parsers: Dict[str, LanguageParser] = {}
        self.call_graph = CallGraphBuilder()
        self.data_flow = DataFlowAnalyzer()
        
        # Register default parsers
        self.register_parser(PythonParser())
    
    def register_parser(self, parser: LanguageParser) -> "CodeIntelligenceEngine":
        """Register a language parser."""
        for ext in parser.get_supported_extensions():
            self.parsers[ext] = parser
        return self
    
    def analyze_file(self, file_path: str, content: str) -> List[CodeSymbol]:
        """Analyze a single file."""
        # Find appropriate parser
        ext = "." + file_path.split(".")[-1] if "." in file_path else ""
        parser = self.parsers.get(ext)
        
        if parser:
            symbols = parser.parse_file(file_path, content)
            self.call_graph.add_symbols(symbols)
            return symbols
        
        return []
    
    def analyze_repository(self, repo_path: str, file_patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze an entire repository.
        
        Returns comprehensive analysis including:
        - All symbols
        - Call graph
        - Data flow
        - Dependencies
        """
        # TODO: Implement repository-wide analysis
        # Would:
        # - Walk directory tree
        # - Parse all supported files
        # - Build cross-file call graph
        # - Detect module dependencies
        return {
            "symbols": [],
            "call_graph": {},
            "dependencies": [],
        }
    
    def find_symbol(self, name: str, file_pattern: Optional[str] = None) -> List[CodeSymbol]:
        """Find symbols by name."""
        results = []
        for symbol in self.call_graph.symbols.values():
            if name.lower() in symbol.name.lower():
                if file_pattern is None or file_pattern in symbol.file_path:
                    results.append(symbol)
        return results
    
    def get_symbol_usage(self, symbol_id: str) -> Dict[str, Any]:
        """Get complete usage information for a symbol."""
        symbol = self.call_graph.symbols.get(symbol_id)
        if not symbol:
            return {}
        
        callers = self.call_graph.get_callers(symbol_id)
        callees = self.call_graph.get_callees(symbol_id)
        
        return {
            "symbol": symbol.to_dict(),
            "called_by": [c.to_dict() for c in callers],
            "calls": [c.to_dict() for c in callees],
        }
    
    def generate_dependency_graph(self) -> Dict[str, Set[str]]:
        """Generate module/file dependency graph."""
        # TODO: Implement dependency extraction
        return {}
