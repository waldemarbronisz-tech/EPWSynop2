from epwsynoptic.core.registry import SymbolDefinition, get_registry
from epwsynoptic.core.models import Port

def register_all_symbols():
    registry = get_registry()

    # We will import and call registration functions from domain modules here
    from .electrical import register_electrical_symbols
    from .water import register_water_symbols
    from .hvac import register_hvac_symbols
    from .automation import register_automation_symbols
    from .graphics import register_graphics_symbols

    register_electrical_symbols(registry)
    register_water_symbols(registry)
    register_hvac_symbols(registry)
    register_automation_symbols(registry)
    register_graphics_symbols(registry)
