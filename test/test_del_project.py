from model.project import Project

def test_login(app):
    app.session.login("administrator","root")
    assert app.session.is_logged_in_as("administrator")

def test_delete_some_group(app):
    #if app.group.count()==0:
    if len(app.project.get_project_list())==0:
        app.project.create(Project(name="test"))
    old_projects = app.project.get_project_list()
    #old_groups = app.group.get_group_list()
    #определяем индекс удаляемой группы
    #randrange генер случ число от 0 до указ знач-я длина олд_групп
    #group = random.choice(old_projects)
    #index = randrange(len(old_groups))
    #правила сортировки для польз.интерфейса и БД - разные 7.4
    app.project.delete_first_proj(3)
    new_groups = app.project.get_project_list()
    #new_groups = app.group.get_group_list()
    #проверка, что новый список на единицу короче чем старый

    #assert len(old_projects)-1 == len(new_groups)
    #берем старый список и удал все эл с индексом
    #old_projects.remove(group)
    #assert old_projects == new_groups #список из бд
    #assert (sorted(new_groups, key=Project.id_or_max) == sorted(app.group.get_group_list(),key=Project.id_or_max))