from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Optional
from .models import Port, EngineeringObject

@dataclass
class SymbolDefinition:
    type_id: str
    category: str
    display_name: str
    default_width: float
    default_height: float
    allowed_states: List[str]
    engineering_properties: Dict[str, Any]
    ports: List[Port]
    supported_bindings: List[str]
    supported_commands: List[str]
    default_label_settings: Dict[str, Any]

    # Optional rendering hooks or classes could go here
    # renderer: Callable = None
    # preview_renderer: Callable = None

class SymbolRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SymbolRegistry, cls).__new__(cls)
            cls._instance.symbols = {}
        return cls._instance

    def register(self, symbol_def: SymbolDefinition):
        self.symbols[symbol_def.type_id] = symbol_def

    def get(self, type_id: str) -> Optional[SymbolDefinition]:
        return self.symbols.get(type_id)

    def get_all(self) -> List[SymbolDefinition]:
        return list(self.symbols.values())

    def get_by_category(self, category: str) -> List[SymbolDefinition]:
        return [s for s in self.symbols.values() if s.category == category]

    def create_instance(self, type_id: str) -> EngineeringObject:
        definition = self.get(type_id)
        if not definition:
            raise ValueError(f"Symbol {type_id} not found in registry.")

        import copy
        return EngineeringObject(
            type_id=type_id,
            width=definition.default_width,
            height=definition.default_height,
            ports=copy.deepcopy(definition.ports),
            states=copy.deepcopy(definition.allowed_states),
            properties=copy.deepcopy(definition.engineering_properties),
            bindings={},
            commands=copy.deepcopy(definition.supported_commands)
        )

# Global singleton accessor
def get_registry() -> SymbolRegistry:
    return SymbolRegistry()
