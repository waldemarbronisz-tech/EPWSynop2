import os
from epwsynoptic.core.models import Project, Page, Connection, Port
from epwsynoptic.core.registry import get_registry
from epwsynoptic.core.serialization import save_project
from epwsynoptic.symbols.base import register_all_symbols

def generate_demo():
    register_all_symbols()
    registry = get_registry()

    project = Project(project_id="ENTRY_GATE_DEMO", metadata={"description": "Demonstration Project"})

    # Page 1: MAIN
    p_main = Page(name="MAIN")

    # Page 2: POWER
    p_power = Page(name="POWER")
    grid = registry.create_instance("electrical.grid")
    grid.designation = "GRID"
    grid.x, grid.y = 100, 50
    p_power.objects.append(grid)

    q1 = registry.create_instance("electrical.circuit_breaker")
    q1.designation = "Q1"
    q1.x, grid.y = 100, 150
    q1.bindings["position"] = "EG.Q1.POSITION"
    p_power.objects.append(q1)

    busbar = registry.create_instance("electrical.busbar")
    busbar.designation = "BB1"
    busbar.name = "400 V"
    busbar.x, busbar.y = 50, 300
    p_power.objects.append(busbar)

    q2 = registry.create_instance("electrical.circuit_breaker")
    q2.designation = "Q2"
    q2.x, q2.y = 100, 400
    p_power.objects.append(q2)

    q3 = registry.create_instance("electrical.circuit_breaker")
    q3.designation = "Q3"
    q3.x, q3.y = 200, 400
    p_power.objects.append(q3)

    q4 = registry.create_instance("electrical.circuit_breaker")
    q4.designation = "Q4"
    q4.x, q4.y = 300, 400
    p_power.objects.append(q4)

    # Simple connections for POWER
    c1 = Connection(id="c1", fromObjectId=grid.id, fromPort="OUT", toObjectId=q1.id, toPort="LINE", domain="electrical", medium="ac")
    c2 = Connection(id="c2", fromObjectId=q1.id, fromPort="LOAD", toObjectId=busbar.id, toPort="MAIN", domain="electrical", medium="ac")
    p_power.connections.extend([c1, c2])

    # Page 3: WATER
    p_water = Page(name="WATER")
    w_source = registry.create_instance("water.source")
    w_source.x, w_source.y = 100, 100
    p_water.objects.append(w_source)

    valve = registry.create_instance("water.valve")
    valve.designation = "V1"
    valve.x, valve.y = 200, 100
    p_water.objects.append(valve)

    pump = registry.create_instance("water.pump")
    pump.designation = "P1"
    pump.x, pump.y = 300, 100
    p_water.objects.append(pump)

    # Page 4: HVAC
    p_hvac = Page(name="HVAC")
    fan = registry.create_instance("hvac.fan")
    fan.designation = "FAN1"
    fan.x, fan.y = 100, 100
    p_hvac.objects.append(fan)

    damper = registry.create_instance("hvac.damper")
    damper.designation = "DAMP1"
    damper.x, damper.y = 200, 100
    p_hvac.objects.append(damper)

    # Page 5: AUTOMATION
    p_automation = Page(name="AUTOMATION")
    ind = registry.create_instance("automation.indicator")
    ind.designation = "SYS_OK"
    ind.x, ind.y = 100, 100
    p_automation.objects.append(ind)

    # Page 6: ENERGY
    p_energy = Page(name="ENERGY")
    meas_u = registry.create_instance("automation.measurement")
    meas_u.designation = "UL1"
    meas_u.bindings["value"] = "EPM01.UL1"
    meas_u.x, meas_u.y = 100, 100
    p_energy.objects.append(meas_u)

    meas_i = registry.create_instance("automation.measurement")
    meas_i.designation = "IL1"
    meas_i.bindings["value"] = "EPM01.IL1"
    meas_i.properties["unit"] = "A"
    meas_i.x, meas_i.y = 100, 150
    p_energy.objects.append(meas_i)

    project.pages.extend([p_main, p_power, p_water, p_hvac, p_automation, p_energy])

    os.makedirs("examples", exist_ok=True)
    save_project(project, "examples/ENTRY_GATE_DEMO.epwsyn")
    print("Created examples/ENTRY_GATE_DEMO.epwsyn")

if __name__ == "__main__":
    generate_demo()
