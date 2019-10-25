import web
import json
import person

def getDict(t):
    with open("ReductionsJson/t" + str(t) + ".json", "r") as read_file:
        return json.load(read_file)

def main():
    #sheet = person.LoadFile("test")
    search = {'f':'Пылькин', 'ps': '100'}
    params = 0
    web.getRecords(search, page = 1, params = params)

if __name__ == "__main__":
    main()