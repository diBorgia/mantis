from model.project import Project
from operator import attrgetter
import random
from random import randrange

def test_delete_some_project(app):
    #if app.group.count()==0:
    if len(app.project.get_project_list())==0:
        app.project.create(Project(name="test"))
    old_projects = app.project.get_project_list()
    #old_groups = app.group.get_group_list()
    #определяем индекс удаляемой группы
    #randrange генер случ число от 0 до указ знач-я длина олд_групп
    #project = random.choice(old_projects)
        #index = randrange(len(old_projects))
    #правила сортировки для польз.интерфейса и БД - разные 7.4
    app.project.delete_proj()
    new_projects = app.project.get_project_list()
    #new_groups = app.group.get_group_list()
    #проверка, что новый список на единицу короче чем старый
    #assert len(old_projects)-1 == len(new_groups)
    #берем старый список и удал все эл с индексом
    old_projects[0:1] = []
    assert old_projects==new_projects
    #assert sorted(old_projects, key=attrgetter('name')) == sorted(new_projects, key=attrgetter('name'))