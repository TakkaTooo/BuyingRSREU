#import web
#import json
import person

def getDict(t):
    with open("ReductionsJson/t" + str(t) + ".json", "r") as read_file:
        return json.load(read_file)

def main():
    
    sheet = person.LoadFile("ts")
    p = person.MakePersonList(sheet)
    man = p[1]
    man_info = man['info'].split(',')
    for i in range(len(man_info)):
        man_info[i].strip() #Этот метод не работает
        if (man_info[i].startswith(' ')):
            man_info[i] = man_info[i][1:len(man_info[i]):1] #Fucking срез s[i, j, h], i - начало, j - кол-во, h - шаг
    print(man_info)
    i = 0
    #dic = getDict(man['vol'])

    #search = {'f':'Пылькин', 'ps': '100'}
    #params = 0
    #web.getRecords(search, page = 1, params = params)

if __name__ == "__main__":
    main()