from epwsynoptic.core.registry import SymbolDefinition
from epwsynoptic.core.models import Port

def register_hvac_symbols(registry):
    registry.register(SymbolDefinition(
        type_id="hvac.fan",
        category="HVAC",
        display_name="Fan",
        default_width=60,
        default_height=60,
        allowed_states=["STOPPED", "RUNNING", "FAULT", "UNKNOWN"],
        engineering_properties={},
        ports=[
            Port(id="IN", x=0.0, y=0.5, domain="hvac", medium="air", direction="in"),
            Port(id="OUT", x=1.0, y=0.5, domain="hvac", medium="air", direction="out")
        ],
        supported_bindings=["running", "fault"],
        supported_commands=["START", "STOP"],
        default_label_settings={"position": "BOTTOM"}
    ))

    registry.register(SymbolDefinition(
        type_id="hvac.damper",
        category="HVAC",
        display_name="Damper",
        default_width=40,
        default_height=40,
        allowed_states=["OPEN", "CLOSED", "FAULT", "UNKNOWN"],
        engineering_properties={},
        ports=[
            Port(id="IN", x=0.0, y=0.5, domain="hvac", medium="air", direction="bidirectional"),
            Port(id="OUT", x=1.0, y=0.5, domain="hvac", medium="air", direction="bidirectional")
        ],
        supported_bindings=["position"],
        supported_commands=["OPEN", "CLOSE"],
        default_label_settings={"position": "TOP"}
    ))
