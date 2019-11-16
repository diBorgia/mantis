import poplib #получение почты
import time
import email #для парсенья сообщения

class MailHelper:

    def __init__(self, app):
        self.app = app


    def get_mail(self,username,password,subject):
        #почта м. прийти не сразу, потому делаем несколько попыток
        for i in range(5):
            pop = poplib.POP3(self.app.config['james']['host'])
            pop.user(username)
            pop.pass_(password)
            #возвращает стат инф, что имеется в ящике. Первый эл-т возвращ кортежа = кол-во писем
            num=pop.stat()[0]
            if num>0:
                #то смотрим тему письма, сравн-м с заданной
                for n in range(num):
                    msglines = pop.retr(n+1)#текст письма во втором элементе кортежа
                    msgtext="\n".join(map(lambda x:x.decode('utf-8'),msglines))
                    msg = email.message_from_string(msgtext)
                    if msg.get("subject")==subject:
                        pop.dele(n+1)
                        pop.quit() #закр с сохр удвленного close - без сохр
                        return msg.get_payload()
            pop.close()
            time.sleep(3)
        return None




