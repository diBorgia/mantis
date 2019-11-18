from sys import maxsize

class Project:
    #None - поле не проинициализировано, то есть указывать его не обязательно, но там хранится специальное значение None
    def __init__(self, name=None, status=None, public=None, id=None,desc=None):
        self.name = name
        self.status = status
        self.desc = desc
        self.id = id
        self.public = public

#ф-ция, что определяет, как будет выглядеть объект при выводе на консоль, какого его строковое представление representation
    def __repr__(self):
        #вывод идентификатора и имени
        return "%s:%s" % (self.name, self.desc)

    #станд ф-ция сравнения объектов не по расположению в памяти, а по значению
    def __eq__(self, other):
         return (self.id is None or other.id is None or self.id == other.id) and \
               (self.name is None or other.name is None or self.name == other.name) and \
               (self.status is None or other.status is None or self.status == other.status) and \
               (self.public is None or other.public is None or self.public == other.public)

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            #eсли возвращается None, то ему будет присвоено макс число, кот м испся в списке в качестве индекса
            return maxsize