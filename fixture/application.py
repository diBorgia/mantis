from selenium import webdriver
from fixture.session import SessionHelper

class Application:

#FF- знач браузера по умолч
    def __init__(self, browser, url):
        if browser == "Firefox":
            self.wd = webdriver.Firefox()
        elif browser == "Chrome":
            self.wd = webdriver.Chrome()
        elif browser == "Ie":
            self.wd = webdriver.Ie()
        else:
            raise  ValueError("Unrecognized browser %s" % browser)
        #ожид элементов полезно, когда элементы подгружаются динамически и стоит дождаться, когда появятся все элементы
        self.wd.implicitly_wait(1)
        #подключение драйвера через фикстуру
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.contact = ContactHelper(self)
        self.url = url


    def open_home_page(self):
        wd = self.wd
        wd.get(self.url)

    def destroy(self):
        self.wd.quit()


    def is_valid(self):
        try:
            #просим браузер проверить адрес текущей страницы, если он сможет это сделать, все хорошо
            self.wd.current_url
            return True
        except:
            return False