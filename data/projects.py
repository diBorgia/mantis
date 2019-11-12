from model.project import Project
import random
    # содержит константы, хранящие списки символов
import string

def random_string(prefix, maxlen):
    symbols_str = string.ascii_letters + string.punctuation + string.digits + " " * 2  # 10 пробелов на строку
    return prefix + "".join([random.choice(symbols_str) for i in
                             range(random.randrange(maxlen))])  # будет сген случ длина не превыш макс

def random_view_status():
    status = ['public','private']
    return random.choice(status)

def random_status():
    status = ['development','release','stable','obsolete']
    return random.choice(status)

# выйдет 1 пустая и 5шт со случ
testdata = [Project(name=random_string("name", 15), desc=random_string("desc", 25),
                       status=random_status(), public=random_view_status())
               for i in range(5)
]