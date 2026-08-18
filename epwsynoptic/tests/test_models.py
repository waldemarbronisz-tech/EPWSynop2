from epwsynoptic.core.models import EngineeringObject, Port, Project, Page
from epwsynoptic.core.registry import SymbolRegistry, SymbolDefinition, get_registry

def test_engineering_object_creation():
    obj = EngineeringObject(type_id="test.obj", name="Test")
    assert obj.id is not None
    assert obj.type_id == "test.obj"
    assert obj.name == "Test"
    assert obj.width == 50.0

def test_symbol_registry():
    registry = get_registry()
    assert isinstance(registry, SymbolRegistry)

    # Using electrical for testing
    from epwsynoptic.symbols.electrical import register_electrical_symbols
    register_electrical_symbols(registry)

    cb = registry.get("electrical.circuit_breaker")
    assert cb is not None
    assert cb.category == "Electrical"
    assert "OPEN" in cb.allowed_states

    inst = registry.create_instance("electrical.circuit_breaker")
    assert inst.type_id == "electrical.circuit_breaker"
    assert len(inst.ports) == 2

def test_project_model():
    p = Project()
    page = Page(name="TestPage")
    p.pages.append(page)

    assert len(p.pages) == 1
    assert p.pages[0].name == "TestPage"
