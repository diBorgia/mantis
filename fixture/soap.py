from suds.client import Client
from suds import WebFault #исключение, выбрасывается, если что-то пошло не так

class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self,username,password):
        #client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        client = Client(self.app.soapUrl)
        try:
            client.service.mc_login(username,password)
            return True
        except WebFault:
            return False

    def count(self,username,password):
        #client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        client = Client(self.app.soapUrl)
        count=client.service.mc_projects_get_user_accessible(username,password)
        return count
