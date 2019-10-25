import web
import json
import person

def getDict(t):
    with open("ReductionsJson/t" + str(t) + ".json", "r") as read_file:
        return json.load(read_file)

def main():
    #sheet = person.LoadFile("test")
    #search = {'f':'Пылькин', 'ps': '100'}                  tests
    #params = 0
    #web.getRecord(search, page = 1, params = params)
    reductions = getDict(1)
    print(reductions)

if __name__ == "__main__":
    main()