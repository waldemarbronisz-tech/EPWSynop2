from epwsynoptic.core.registry import SymbolDefinition
from epwsynoptic.core.models import Port

def register_electrical_symbols(registry):
    registry.register(SymbolDefinition(
        type_id="electrical.circuit_breaker",
        category="Electrical",
        display_name="Circuit Breaker",
        default_width=40,
        default_height=80,
        allowed_states=["OPEN", "CLOSED", "TRIPPED", "FAULT", "UNKNOWN"],
        engineering_properties={},
        ports=[
            Port(id="LINE", x=0.5, y=0.0, domain="electrical", medium="ac", direction="bidirectional"),
            Port(id="LOAD", x=0.5, y=1.0, domain="electrical", medium="ac", direction="bidirectional")
        ],
        supported_bindings=["position", "trip"],
        supported_commands=["OPEN", "CLOSE"],
        default_label_settings={"position": "LEFT"}
    ))

    registry.register(SymbolDefinition(
        type_id="electrical.disconnect_switch",
        category="Electrical",
        display_name="Disconnect Switch",
        default_width=40,
        default_height=80,
        allowed_states=["OPEN", "CLOSED", "FAULT", "UNKNOWN"],
        engineering_properties={},
        ports=[
            Port(id="LINE", x=0.5, y=0.0, domain="electrical", medium="ac", direction="bidirectional"),
            Port(id="LOAD", x=0.5, y=1.0, domain="electrical", medium="ac", direction="bidirectional")
        ],
        supported_bindings=["position"],
        supported_commands=["OPEN", "CLOSE"],
        default_label_settings={"position": "LEFT"}
    ))

    registry.register(SymbolDefinition(
        type_id="electrical.busbar",
        category="Electrical",
        display_name="Busbar",
        default_width=400,
        default_height=10,
        allowed_states=["DEENERGIZED", "ENERGIZED", "FAULT"],
        engineering_properties={"voltage": "400V", "orientation": "horizontal"},
        ports=[
            # Busbars allow dynamic attachment, but we give a default point for simplicity
            Port(id="MAIN", x=0.5, y=0.5, domain="electrical", medium="ac", direction="bidirectional")
        ],
        supported_bindings=["energized"],
        supported_commands=[],
        default_label_settings={"position": "TOP"}
    ))

    registry.register(SymbolDefinition(
        type_id="electrical.grid",
        category="Electrical",
        display_name="Grid Source",
        default_width=60,
        default_height=60,
        allowed_states=["OK", "FAULT", "UNKNOWN"],
        engineering_properties={},
        ports=[
            Port(id="OUT", x=0.5, y=1.0, domain="electrical", medium="ac", direction="out")
        ],
        supported_bindings=["status"],
        supported_commands=[],
        default_label_settings={"position": "TOP"}
    ))
