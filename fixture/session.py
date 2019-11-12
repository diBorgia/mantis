class SessionHelper:

    def __init__(self, app):
        self.app = app


    def login(self, username, password):
        wd = self.app.wd
        #тк метода остался в фикстуре, обращаемся к нему через нее
        self.app.open_home_page()
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_css_selector("input[type='submit']").click()

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()
        #ждем полного разлогина, чтобы верно отработали последующие сценарии
        #проверяем, что логин произошел по нахождению элемента на странице
        wd.find_element_by_name("user")

    def ensure_logout(self):
        wd = self.app.wd
        #find elements вернет все элементы, удовлетворяющие заданному условию
        #len нам важно знать, что их количество >0
        if self.is_logged_in(wd):
            self.logout()

    def is_logged_in(self, wd):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, username):
        wd = self.app.wd
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        #читаем текс и делаем вырезку от 1 до предпосл символа
        return wd.find_element_css_selector("td.login-info-left span").text

    def ensure_login(self,username,password):
        wd = self.app.wd
        #если мы вошли в систему, проверяем, что вошли как пользователь именно с таким именем
        if self.is_logged_in(wd):
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        #до этой строки доберемся если пользователь не залогинен, если залогинен, но имя не совпадает
        self.login(username,password)