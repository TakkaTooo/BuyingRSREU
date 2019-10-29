import json

# род. 1895 г., Рязанская обл., Шацкий рн, 
# с. Кулики, рядовой, 172 сд, погиб 10. 12. 42 г., 
# место захоронения Ворошиловоградская обл.

# род. Рязанская обл., Шацкий рн, рядовой, 
# 907 сп, 244 сд, пропал без вести 24. 02. 43 г.

reason = ['погиб', 'пропал без вести', 'погиб в плену',
          'умер от ран', 'неизвестно']

season = {'январ' : '01', 'феврал' : '02', 'март' : '03', 'апрел' : '04', 'ма' : '05', 'июн' : '06', 
          'июл' : '07', 'август' : '08', 'сентябр' : '09', 'октябр' : '10', 'ноябр' : '11', 'декабре' : '12'}
rank = ['рядовой', 'гвардии ефрейтор', 'старший сержант', 'ефрейтор', 'младший сержант',
        'лейтенант', 'капитан', 'майор', 'старшина', 'гвардии лейтенант', 'гвардии рядовой', 'гвардии младший лейтенант',
        'младший политрук']

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
        if ((j < len(_list)) and (_list[j].find('род.') and bornyear == False) == 0):
            args = _list[j][5:len(_list[j])]
            if (args.find('г.') > 0):
                cleanargs = args[0:args.find('г.')]
                bornyear = True
                checkby = True
                _person['birthyear'] = cleanargs
                j += 1
            elif ((j < len(_list)) and args.find('обл.') >= 0 or args.find('рн') >= 0 or args.find('с.') >= 0 or args.find('гор.') >= 0):
                cleanargs = args
                bornplace = True
                _person['born_place'] = cleanargs
                j += 1
                if ((j < len(_list)) and (_list[j].find('рн') >= 0 or _list[j].find('с.') >= 0 or _list[j].find('гор.') >= 0) and (_list[j].find('место захоронения') < 0)):
                    j += 1
                    if ((j < len(_list)) and (_list[j].find('с.') >= 0 or _list[j].find('гор.') >= 0) and (_list[j].find('место захоронения') < 0)):
                        j += 1
            continue
        #Обработка места рождения (область)
        elif ((j < len(_list)) and (_list[j].find('обл.') >= 0 or _list[j].find('рн') >= 0 or _list[j].find('с.') >= 0 or _list[j].find('гор.') >= 0) and (_list[j].find('место захоронения') < 0) and bornplace == False):
            bornplace = True
            _person['born_place'] = _list[j]
            j += 1
            if ((j < len(_list)) and (_list[j].find('рн') >= 0 or _list[j].find('с.') >= 0 or _list[j].find('гор.') >= 0) and (_list[j].find('место захоронения') < 0)):
                j += 1
                if ((j < len(_list)) and (_list[j].find('с.') >= 0 or _list[j].find('гор.') >= 0) and (_list[j].find('место захоронения') < 0)):
                    j += 1
            continue
        #Обработка звания
        elif ((j < len(_list)) and isFuckingRank(_list[j])):
            rank = True
            _person['rank'] = _list[j]
            j += 1
            continue
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
                word = _list[j][_list[j].find(smth)+len(smth):a]
                args += word
                _person['deathday'] = args
            elif((j < len(_list))):
                lastin = _list[j].find('г.')
                arg = _list[j][firstin+secondin+1:lastin]
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
                _person['deathday'] = cleanargs
            j += 1
            continue
        #Получение места захоронения
        elif ((j < len(_list)) and _list[j].find('место захоронения') >= 0):
            l = len('место захоронения')
            f = _list[j].find('место захоронения')
            num = f+l
            word = _list[j][num:len(_list[j])] + ', '
            j += 1
            while (j < len(_list)):
                word += _list[j]
                j += 1
            _person['burial_place'] = word
            continue
        #Обработка специальности
        elif ((j < len(_list)) and (bornyear == True or bornplace == True or rank == True) and (dutyplace == False and deathday == False and burialplace == False)):
            spec = True
            _person['spec'] = _list[j]
            j += 1
            continue
        else:
            j += 1
        #Получение места службы
        if (j < len(_list)):
            args4duty = ''
            while ((j < len(_list)) and (bornyear == True or bornplace == True or rank == True) and containsInPart(_list[j], _person['vol'])):
                word = ''
                dic = getDict(_person['vol'])
                red = list(dic.keys())
                for i in red:
                    if (_list[j].find(i) > 0):
                        word = _list[j].replace(i, dic[i])
                        break
                args4duty = args4duty + word + ' '
                j += 1
            _person['duty_place'] = args4duty
       

            
    return _person

def splitShit(info):
    li = info.split(',')
    for i in li:
        if (i.startswith(' ')):
            i = i[1:len(i)]
    return li

def getDict(t):
    with open("ReductionsJson/t" + str(t) + ".json", "r") as read_file:
        return json.load(read_file)            

def containsInPart(st, vol):
    red = list((getDict(vol)).keys())
    for i in red:
        if (st.find(i) >= 0):
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