from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Tag:
    name: str
    value: Any = None
    data_type: str = "float"
    quality: str = "GOOD" # GOOD, BAD, UNKNOWN, OFFLINE
    timestamp: float = 0.0
    source: str = ""
    unit: str = ""

class TagModel:
    def __init__(self):
        self.tags: Dict[str, Tag] = {}

    def add_tag(self, tag: Tag):
        self.tags[tag.name] = tag

    def get_tag(self, name: str) -> Tag:
        return self.tags.get(name)

    def update_value(self, name: str, value: Any, quality: str = "GOOD"):
        if name in self.tags:
            self.tags[name].value = value
            self.tags[name].quality = quality
