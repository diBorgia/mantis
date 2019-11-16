import pytest
import json
import os.path
import ftputil
from fixture.application import Application

#grobal variable
fixture = None
target = None

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))

@pytest.fixture
def app(request,config):
    global fixture
    # через реквест получаем доступ к параметру
    browser = request.config.getoption("--browser")
    #config =load_config(request.config.getoption("--target"))["web"]
    #ситуация перед вызовом первой тестовой функции
    # если фикстура уже создана, н.проверить, не испортилась ли она
    if fixture is None or not fixture.is_valid():
    #тогда надо фикстуру проинициализировать
        fixture = Application(browser=browser, config=config)#url=config["web"]['baseUrl'])
    #проверка нужно выполнять логин или не нужно
    fixture.session.ensure_login(username=config["webAdmin"]["username"], password=config['webAdmin']["password"])
    return fixture

@pytest.fixture(scope="session", autouse=True) #благодаря autouse фикстура сработает автоматически
def configure_server(request,config):
    #задача - подложить нужные конфиг данные на сервер
    install_server_configuration(config['ftp']['host'],config['ftp']['username'],config['ftp']['password'])
    #восстановление исходного
    def fin():
        restore_server_configuration(config['ftp']['host'],config['ftp']['username'],config['ftp']['password'])
    request.addfinalizer(fin)

#ф-цияб занимающ загрузкой из target.json
def load_config(file):
    global target
    if target is None:
        # преобразуем путь к файлу в абсолютный, определяем директорию, присоединяем таргет
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

def install_server_configuration(host,username,password):
    with ftputil.FTPHost(host,username,password) as remote:
        #проверяем, что не будет еще одного конфликта, если будет - удаляем
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        #если есть такой файл, то он будет переименован
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php","config_inc.php.bak")
        #после переименования можно загрузить локальный файл на сервер
        remote.upload(os.path.join(os.path.dirname(__file__),"resources/config_inc.php"),"config_inc.php")

def restore_server_configuration(host,username,password):
    #обратные действия относительно install configuration
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")

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
