from model.project import Project
import pytest
from operator import attrgetter
from data.projects import testdata

@pytest.mark.parametrize("project",testdata, ids=[repr(x) for x in testdata])
def test_add_project(app,project): #параметр груп может указывать на тестовые данные. Загруж тестовые данные из модуля групс в пакете дата
    old_projects = app.project.get_project_list()
    app.project.create(project)
    #проверка, что новый список на единицу длиннее чем старый
   # assert len(old_projects)+1 == app.project.count()
    new_projects = app.project.get_project_list()
    #старый список, в который мы сами добавили группу
    #новый, который загружен из приложения, когда в приложение добавлена та же группа
    old_projects.append(project)
    #assert sorted(old_projects, key=project.id_or_max) == sorted(new_projects, key=project.id_or_max)
    #getName = attrgetter('name')
    assert sorted(old_projects, key=attrgetter('name')) == sorted(new_projects, key=attrgetter('name'))
