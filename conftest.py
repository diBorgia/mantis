import pytest
import json
import os.path
from fixture.application import Application

#grobal variable
fixture = None
target = None

@pytest.fixture
def app(request):
    global fixture
    # через реквест получаем доступ к параметру
    browser = request.config.getoption("--browser")
    web_config =load_config(request.config.getoption("--target"))["web"]
    #ситуация перед вызовом первой тестовой функции
    # если фикстура уже создана, н.проверить, не испортилась ли она
    if fixture is None or not fixture.is_valid():
    #тогда надо фикстуру проинициализировать
        fixture = Application(browser=browser, url=web_config['baseUrl'])
    #проверка нужно выполнять логин или не нужно
    return fixture

@pytest.fixture(scope="session", autouse=True) #благодаря autouse фикстура сработает автоматически
def configure_server(request):
    pass

#ф-цияб занимающ загрузкой из target.json
def load_config(file):
    global target
    if target is None:
        # преобразуем путь к файлу в абсолютный, определяем директорию, присоединяем таргет
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture(scope="session", autouse=True) #благодаря autouse фикстура сработает автоматически
def stop(request):
#благодаря этой функции при финалайзере будет и логаут, и дестрой
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    #параметр, действие кот нужно выполнить - сохранить пар-р, значение
    parser.addoption("--browser",action="store",default="Firefox")
    #при запуске тестов в параметре таргет должна быть указана ссылка на конфиг-й файл
    parser.addoption("--target",action="store",default="target.json")
