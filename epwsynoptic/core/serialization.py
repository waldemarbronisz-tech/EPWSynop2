import json
from typing import Dict, Any
from epwsynoptic.core.models import Project, Page, EngineeringObject, Connection, Port, LabelSettings

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        import dataclasses
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def save_project(project: Project, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(project, f, cls=EnhancedJSONEncoder, indent=2)

def load_project(filepath: str) -> Project:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    project = Project(
        project_id=data.get('project_id', ''),
        format_version=data.get('format_version', 1),
        created_with=data.get('created_with', ''),
        modified_at=data.get('modified_at', ''),
        metadata=data.get('metadata', {})
    )

    for page_data in data.get('pages', []):
        page = Page(
            id=page_data.get('id', ''),
            name=page_data.get('name', 'Page'),
            description=page_data.get('description', ''),
            background=page_data.get('background', '#ffffff'),
            width=page_data.get('width', 1920.0),
            height=page_data.get('height', 1080.0),
            grid_enabled=page_data.get('grid_enabled', True),
            grid_size=page_data.get('grid_size', 10.0),
            startup_page=page_data.get('startup_page', False),
            visibility=page_data.get('visibility', True)
        )

        for obj_data in page_data.get('objects', []):
            ls_data = obj_data.get('label_settings', {})
            label_settings = LabelSettings(**ls_data)

            ports_data = obj_data.get('ports', [])
            ports = [Port(**p) for p in ports_data]

            # Need to filter out any unexpected keys for EngineeringObject
            obj_kwargs = {k: v for k, v in obj_data.items() if k not in ['label_settings', 'ports']}
            obj = EngineeringObject(label_settings=label_settings, ports=ports, **obj_kwargs)
            page.objects.append(obj)

        for conn_data in page_data.get('connections', []):
            conn = Connection(**conn_data)
            page.connections.append(conn)

        project.pages.append(page)

    return project
