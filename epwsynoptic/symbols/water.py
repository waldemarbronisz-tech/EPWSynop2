from epwsynoptic.core.registry import SymbolDefinition
from epwsynoptic.core.models import Port

def register_water_symbols(registry):
    registry.register(SymbolDefinition(
        type_id="water.pump",
        category="Water",
        display_name="Pump",
        default_width=60,
        default_height=60,
        allowed_states=["STOPPED", "RUNNING", "FAULT", "UNKNOWN"],
        engineering_properties={},
        ports=[
            Port(id="IN", x=0.0, y=0.5, domain="water", medium="water", direction="in"),
            Port(id="OUT", x=1.0, y=0.5, domain="water", medium="water", direction="out")
        ],
        supported_bindings=["running", "fault"],
        supported_commands=["START", "STOP"],
        default_label_settings={"position": "BOTTOM"}
    ))

    registry.register(SymbolDefinition(
        type_id="water.valve",
        category="Water",
        display_name="Valve",
        default_width=40,
        default_height=40,
        allowed_states=["OPEN", "CLOSED", "FAULT", "UNKNOWN"],
        engineering_properties={},
        ports=[
            Port(id="IN", x=0.0, y=0.5, domain="water", medium="water", direction="bidirectional"),
            Port(id="OUT", x=1.0, y=0.5, domain="water", medium="water", direction="bidirectional")
        ],
        supported_bindings=["position"],
        supported_commands=["OPEN", "CLOSE"],
        default_label_settings={"position": "TOP"}
    ))

    registry.register(SymbolDefinition(
        type_id="water.source",
        category="Water",
        display_name="Water Source",
        default_width=50,
        default_height=50,
        allowed_states=["OK", "UNKNOWN"],
        engineering_properties={},
        ports=[
            Port(id="OUT", x=1.0, y=0.5, domain="water", medium="water", direction="out")
        ],
        supported_bindings=[],
        supported_commands=[],
        default_label_settings={"position": "TOP"}
    ))
