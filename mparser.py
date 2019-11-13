import json

# род. 1895 г., Рязанская обл., Шацкий рн, 
# с. Кулики, рядовой, 172 сд, погиб 10. 12. 42 г., 
# место захоронения Ворошиловоградская обл.

# род. Рязанская обл., Шацкий рн, рядовой, 
# 907 сп, 244 сд, пропал без вести 24. 02. 43 г.

reason = ['пропал без вести', 'погиб в плену',
          'умер от ран', 'неизвестно', 'пропапала без вести', 'погибла в плену',
          'умерла от ран', 'умерла', 'умер', 'увековечен', 'увековечена', 
          'пропала', 'пропал', 'погибла','погиб']

season = {'январ' : '01', 'феврал' : '02', 'март' : '03', 'апрел' : '04', 'ма' : '05', 'июн' : '06', 
          'июл' : '07', 'август' : '08', 'сентябр' : '09', 'октябр' : '10', 'ноябр' : '11', 'декабре' : '12'}
rank = ['рядовой', 'гвардии ефрейтор', 'старший сержант', 'ефрейтор', 'младший сержант',
        'лейтенант', 'капитан', 'майор', 'старшина', 'гвардии лейтенант', 'гвардии рядовой', 'гвардии младший лейтенант',
        'младший политрук']
spec = []

type_area = ['обл.', 'рн', 'г.', 'с.', 'д.']

def parse(info, person):
    _person = person
    _list = splitShit(info)
    bornyear = False
    checkby = False

    bornplace = False
    rank = False
    spec = False
    dutyplace = False
    deathday = False
    burialplace = False

    j = 0
    while (j < len(_list)):
        #Обработка года рождения / место рождения (область)
        if ((j < len(_list)) and _list[j].find('род.') >= 0):
            args = _list[j][5:len(_list[j])]
            if (args.find('г.') > 0):
                cleanargs = args[0:args.find('г.')]
                bornyear = True
                checkby = True
                cleanargs = getOnlyNumbers(cleanargs)
                _person['birthyear'] = cleanargs
                j += 1
            elif (j < len(_list) and isItFuckingPlace(args)):
                cleanargs = args
                bornplace = True
                j += 1
                if (j < len(_list) and isItFuckingPlace(args) and (_list[j].find('место захоронения') < 0) and isThisBadSituation(_list[j]) == False):
                    cleanargs += ', ' + _list[j]
                    j += 1
                    if (j < len(_list) and isItFuckingPlace(args) and (_list[j].find('место захоронения') < 0)  and isThisBadSituation(_list[j]) == False):
                        cleanargs += ', ' + _list[j]
                        j += 1

                _person['born_place'] = cleanargs
            else:
                j += 1
            continue
        #Обработка места рождения (область)
        elif (j < len(_list) and isItFuckingPlace(_list[j]) and (_list[j].find('место захоронения') < 0)):
            bornplace = True
            cleanargs = _list[j]
            j += 1
            if (j < len(_list) and isItFuckingPlace(_list[j]) and (_list[j].find('место захоронения') < 0)  and isThisBadSituation(_list[j]) == False):
                cleanargs += ', ' + _list[j]
                j += 1
                if (j < len(_list) and isItFuckingPlace(_list[j]) and (_list[j].find('место захоронения') < 0)  and isThisBadSituation(_list[j]) == False):
                    cleanargs += ', ' + _list[j]
                    j += 1
            _person['born_place'] = cleanargs
            continue
        #Обработка звания
        #elif ((j < len(_list)) and isFuckingRank(_list[j])):
        #    rank = True
        #    _person['rank'] = _list[j]
        #    j += 1
        #    continue
        #Получение даты смерти
        elif ((j < len(_list)) and isThisBadSituation(_list[j])):
            firstin = 0
            secondin = 0
            for i in reason:
                if (_list[j].find(i) >= 0):
                    firstin = _list[j].find(i)
                    secondin = len(i)
                    break
            if ((j < len(_list)) and isThisBadDate(_list[j])):
                smth = 'в '
                month = ''
                kk = list(season.keys())
                for i in kk:
                    if (_list[j].find(i) >= 0):
                        month = season[i]
                        smth += i
                        break
                args = '00.' + month + '.'
                a = _list[j].find('г.')
                word = getOnlyNumbers(_list[j][_list[j].find(smth)+len(smth):a])
                print(word)
                args += word
                _person['deathday'] = args
            elif((j < len(_list))):
                if (_list[j].find('в ') >= 0):
                    secondin += 2
                lastin = _list[j].find('г.')
                arg = _list[j][firstin+secondin:lastin]
                cleanargs = ''
                for i in range(len(arg)):
                    if (arg[i] != ' '):
                        cleanargs += arg[i]
                p = 0
                for i in range(len(cleanargs)):
                    if (cleanargs[i] == '.'):
                        p += 1
                    if (p == 2):
                        a = cleanargs[i+1:len(cleanargs)]
                        a = '.19' + a
                        cleanargs = cleanargs[0:i] + a
                        break
                word = ''
                for i in range(len(cleanargs)):
                    if (cleanargs[i] == '.'):
                        break
                    else:
                        word += cleanargs[i]
                if (len(word) == 1):
                    cleanargs = '0' + cleanargs
                if (p == 0):
                    cleanargs = "00.00." + cleanargs
                _person['deathday'] = cleanargs
            j += 1
            continue
        #Получение места захоронения
        #elif ((j < len(_list)) and _list[j].find('место захоронения') >= 0):
        #    l = len('место захоронения')
        #    f = _list[j].find('место захоронения')
        #    num = f+l
        #    word = _list[j][num:len(_list[j])]
        #    more = False
        #    j += 1
        #    if (j < len(_list)):
        #        word += ', '
        #        more = True
        #    else:
        #        if (_list[j-1].find('обл.') < 0):
        #            word = word[0:len(word)-1]
        #    while (j < len(_list)):
        #        word += _list[j]
        #        j += 1
        #   if (more):
        #        _person['burial_place'] = word[0:len(word)-1]
        #    else:
        #        _person['burial_place'] = word
        #    continue
        #Обработка специальности
        elif ((j < len(_list) and containsInSpec(_list[j]))):
            spec = True
            _person['spec'] = _list[j]
            j += 1
            continue
        else:
            #Получение места службы
            if (j < len(_list)):
                args4duty = ''
                if (containsInPart(_list[j], _person['vol'])):
                    while ((j < len(_list)) and containsInPart(_list[j], _person['vol'])):
                        word = ''
                        dic = getDict(_person['vol'])
                        mylist = _list[j].split(' ')
                        red = list(dic.keys())
                        for a in mylist:
                            if (isNumber(a) == False):
                                if (a[len(a)-1] == '.'):
                                    a = a[0:len(a)-2]
                                for i in red:
                                    if (a == i):
                                        word = _list[j].replace(i, dic[i])
                                        print(word, ' ', _list[j], ' ', dic[i])
                                        break
                        args4duty = args4duty + word + ' '
                        j += 1
                    _person['duty_place'] = args4duty
                else:
                    j += 1
       

            
    return _person

def isItFuckingPlace(place):
    li = place.split()
    for j in li:
        for i in reason:
            if (j == i):
                return False
    for i in li:
        for j in type_area:
            if (i == j):
                return True
    return False

def splitShit(info):
    li = info.split(',')
    for i in li:
        if (i.startswith(' ')):
            i = i[1:len(i)]
    return li

def getDict(t):
    with open("ReductionsJson/t" + str(t) + ".json", "r") as read_file:
        return json.load(read_file)            

def isNumber(st):
    for i in range(len(st)):
        if(st[i].isdigit() == False):
            return False
    return True

def containsInPart(st, vol):
    mylist = st.split(' ')
    red = list((getDict(vol)).keys())
    for a in mylist:
        if (isNumber(a) == False):
            if (a[len(a)-1] == '.'):
                a = a[0:len(a)-2]
            for i in red:
                if (a == i):
                    print(a)
                    return True    
    return False

def isThisBadDate(st):
    kk = list(season.keys())
    for i in kk:
        if (st.find(i) >= 0):
            return True
    return False

def isThisBadSituation(st):
    for i in reason:
        if (st.find(i) >= 0):
            return True
    return False

def isFuckingRank(st):
    for i in rank:
        if (st.find(i) >= 0):
            return True
    return False

def getOnlyNumbers(year):
    word = ''
    for i in range(len(year)):
        if (str(year[i]).isdigit() or year[i] == '.'):
            word += year[i]
    return word

def containsInSpec(st):
    for i in spec:
        if (st.find(i) >= 0):
            return True
    return False