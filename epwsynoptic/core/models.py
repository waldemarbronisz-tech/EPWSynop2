import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass
class Port:
    id: str
    x: float
    y: float
    domain: str  # e.g., 'electrical', 'water', 'hvac', 'data', 'control'
    medium: str  # e.g., 'ac', 'dc', 'ethernet', 'rs485'
    direction: str  # e.g., 'in', 'out', 'bidirectional'
    label: str = ""
    connection_rules: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Connection:
    id: str
    fromObjectId: str
    fromPort: str
    toObjectId: str
    toPort: str
    domain: str
    medium: str
    route: str = "auto"
    waypoints: List[Dict[str, float]] = field(default_factory=list)
    style: Dict[str, Any] = field(default_factory=dict)
    state: str = "UNKNOWN"
    flowDirection: str = "none"
    bindings: Dict[str, str] = field(default_factory=dict)

@dataclass
class LabelSettings:
    showDesignation: bool = True
    showName: bool = True
    position: str = "BOTTOM"  # TOP, BOTTOM, LEFT, RIGHT
    offsetX: float = 0.0
    offsetY: float = 0.0
    fontSize: int = 10
    alignment: str = "center"
    wrapping: bool = True

@dataclass
class EngineeringObject:
    type_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    designation: str = ""
    name: str = ""
    description: str = ""
    x: float = 0.0
    y: float = 0.0
    width: float = 50.0
    height: float = 50.0
    rotation: float = 0.0
    z_order: int = 0
    visible: bool = True
    locked: bool = False
    label_settings: LabelSettings = field(default_factory=LabelSettings)
    properties: Dict[str, Any] = field(default_factory=dict)
    ports: List[Port] = field(default_factory=list)
    bindings: Dict[str, str] = field(default_factory=dict)
    states: List[str] = field(default_factory=lambda: ["UNKNOWN"])
    commands: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Page:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "New Page"
    description: str = ""
    background: str = "#ffffff"
    width: float = 1920.0
    height: float = 1080.0
    grid_enabled: bool = True
    grid_size: float = 10.0
    startup_page: bool = False
    visibility: bool = True
    objects: List[EngineeringObject] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)

@dataclass
class Project:
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    format_version: int = 1
    created_with: str = "EPW Synoptic Editor"
    modified_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    pages: List[Page] = field(default_factory=list)
