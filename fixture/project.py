from selenium.webdriver.support.ui import Select
from model.project import Project
import re

class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def redirect_to_manage_pr(self):
        wd = self.app.wd
        if wd.current_url.endswith("/manage_proj_page.php"):
            return
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_css_selector("input[type='submit']").click()
        wd.find_element_by_link_text("Manage Projects").click()

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.redirect_to_manage_pr()
            self.project_cache=[]
            for element in wd.find_elements_by_partial_link_text("name"):
            #for element in wd.find_elements_by_partial_link_text("manage_proj_edit_page.php?project_id="):
            #for element in wd.find_elements_by_xpath("//table[@class='width100']/tr//td[@width]"):
                cells = element.find_elements_by_tag_name("tr")
                name = cells[1].text
                #получаем текст элемента
                id = element.find_element_by_name("selected[]").get_attribute("value")
                status = cells[2].text
                #деление ячейки на строки. У нее берется текст и делится на кусочки
                #когда нарезка                all_phones = cells[5].text.splitlines()
                #когда склейка
                view_status = cells[4].text
                description = cells[5].text
                self.project_cache.append(Project(name=name,id=id,status=status,public=view_status, desc=description))
                                                    #когда нарезка по разным телефонам
                                                  #home=all_phones[0],mobile=all_phones[1],work=all_phones[2],phone2=all_phones[3]))
            # создется внешняя копия, сам кеш не будет тронут
        return list(self.project_cache)

    def create(self, new_data):
        wd = self.app.wd
        self.redirect_to_manage_pr()
        # init new contact creation
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        # fill contact form
        self.fill_project_form(new_data)
        # submit modification
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.redirect_to_manage_pr()
        self.project_cache = None


    def fill_project_form(self, project):
        self.change_field_value("name", project.name)
        self.change_field_value("status", project.status)
        self.change_field_value("description", project.desc)
        self.change_field_value("view_state", project.public)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            #wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def count(self):
        wd = self.app.wd
        self.redirect_to_manage_pr()
        #find all elements with name selected
        #взять длину получившегося списка and return it
        return len(wd.find_elements_by_partial_link_text("name"))
        #return len(wd.find_elements_by_xpath("//table[@class='width100']/tr//td[@width]"))

    def delete_first_proj(self,index):
        wd = self.app.wd
        self.redirect_to_manage_pr()
        wd.find_element_by_xpath("//tr[%s]/td/a"%index).click()
        wd.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Description'])[1]/following::input[4]").click()
        #submit deletion
        wd.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Logout'])[1]/following::input[6]").click()
        self.redirect_to_manage_pr()
        self.project_cache = None
