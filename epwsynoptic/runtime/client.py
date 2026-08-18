from typing import Callable, Dict, Any, List
from epwsynoptic.runtime.tags import Tag, TagModel

class RuntimeClient:
    def __init__(self, tag_model: TagModel):
        self.tag_model = tag_model
        self.connected = False
        self.subscribed_tags: set = set()
        self.on_tag_updated: Callable[[str, Any], None] = None

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def subscribe_tags(self, tag_names: List[str]):
        for name in tag_names:
            self.subscribed_tags.add(name)

    def unsubscribe_tags(self, tag_names: List[str]):
        for name in tag_names:
            if name in self.subscribed_tags:
                self.subscribed_tags.remove(name)

    def get_tag_value(self, name: str) -> Any:
        tag = self.tag_model.get_tag(name)
        return tag.value if tag else None

    def send_command_request(self, command: str, params: Dict[str, Any] = None):
        print(f"Command Request Sent: {command} with params {params}")
        return {"status": "ACCEPTED"}

    def get_device_status(self, device_id: str) -> str:
        return "ONLINE" if self.connected else "OFFLINE"
