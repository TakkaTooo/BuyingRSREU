import web
import person

sheet = person.LoadFile("test")

search = {'f':'Пылькин', 'ps': '100'}
params = 0
web.getRecord(search, page = 1, params = params)


