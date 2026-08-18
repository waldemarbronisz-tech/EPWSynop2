from epwsynoptic.core.registry import SymbolDefinition
from epwsynoptic.core.models import Port

def register_graphics_symbols(registry):
    registry.register(SymbolDefinition(
        type_id="graphics.text",
        category="Graphics",
        display_name="Text Note",
        default_width=100,
        default_height=30,
        allowed_states=["NORMAL"],
        engineering_properties={
            "content": "Note",
            "font_size": 12
        },
        ports=[],
        supported_bindings=[],
        supported_commands=[],
        default_label_settings={"showDesignation": False, "showName": False}
    ))
