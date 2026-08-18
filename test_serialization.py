from epwsynoptic.core.models import Project, Page, EngineeringObject, LabelSettings
from epwsynoptic.core.serialization import save_project, load_project

def test():
    proj = Project(project_id="test-123")
    page = Page(name="TestPage")
    obj = EngineeringObject(type_id="test.type", name="TestObj", label_settings=LabelSettings(showName=False))
    page.objects.append(obj)
    proj.pages.append(page)

    save_project(proj, "test.epwsyn")

    loaded = load_project("test.epwsyn")
    assert loaded.project_id == "test-123"
    assert loaded.pages[0].name == "TestPage"
    assert loaded.pages[0].objects[0].name == "TestObj"
    assert loaded.pages[0].objects[0].label_settings.showName == False
    print("Serialization test passed!")

if __name__ == "__main__":
    test()
