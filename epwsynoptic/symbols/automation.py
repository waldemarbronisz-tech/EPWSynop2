from epwsynoptic.core.registry import SymbolDefinition
from epwsynoptic.core.models import Port

def register_automation_symbols(registry):
    registry.register(SymbolDefinition(
        type_id="automation.indicator",
        category="Automation",
        display_name="Status Indicator",
        default_width=30,
        default_height=30,
        allowed_states=["ON", "OFF", "FAULT", "UNKNOWN"],
        engineering_properties={},
        ports=[],
        supported_bindings=["status"],
        supported_commands=[],
        default_label_settings={"position": "BOTTOM"}
    ))

    registry.register(SymbolDefinition(
        type_id="automation.measurement",
        category="Measurements",
        display_name="Measurement Value",
        default_width=100,
        default_height=30,
        allowed_states=["NORMAL", "ALARM_LOW", "ALARM_HIGH", "UNKNOWN"],
        engineering_properties={
            "unit": "V",
            "decimals": 1,
            "alarm_low": 0.0,
            "alarm_high": 100.0
        },
        ports=[],
        supported_bindings=["value"],
        supported_commands=[],
        default_label_settings={"position": "TOP"}
    ))
