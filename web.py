import requests
import time
from bs4 import BeautifulSoup

def getAnswer(url, search):
    r = requests.get(url, params = search)
    while (len(r.text) < 19936):    #19936 - магическое число, длина страницы загрузки.
        r = requests.get(url, params = search)
    return r

def findCount(r):
    pos = r.text.find("row search-result")
    count = 0 
    while (pos != -1):
        count += 1
        pos = r.text.find("row search-result", pos + 1)
    return count


def analyzeRecord(id, params = 0):
    url = "https://obd-memorial.ru/html/info.htm"
    r = getAnswer(url, {"id":id})
    soup = BeautifulSoup(r.text, "html.parser")  
    titles = soup.findAll(class_="card_param-title")
    results = soup.findAll(class_="card_param-result")
    data = {}
    for i in range(0, len(results)):
        data[str(titles[i+1].text)] = str(results[i].text)
    return data

def birthYear(d):
    if (str(d).find('.') != -1):
        dt = str(d).split('.')
        return str(dt[2])
    else:
        d = str(d).strip()
        return str(d)

def deathDate(d):
    if (str(d).find('Между') != -1):
        d = d.split('и')
        dt = str(d[1]).strip()
    elif (str(d).find('-') != -1):
        d = d.split('-')
        dt = str(d[1]).strip()
    else:
        dt = d
        str(dt).strip()
    dt = str(dt).split('.')
    for i in range(0, len(dt)):
        dt[i] = str(dt[i]).replace('__', '00')
    return dt

def getRecords(page, params, per):    
    url = "https://obd-memorial.ru/html/search.htm"
    search = {'f': 'T~' + params['Фамилия'], 'n': 'T~' + params['Имя'], 's': 'T~' + params['Отчество'], 'ps': '100', 'entity':'000000011111111', 'entities': '24,28,27,23,34,22,20,21,19','p': page}
    print(search)
    params['Дата рождения/Возраст'] = birthYear(params['Дата рождения/Возраст'])
    if (page == 1):
        params['Дата выбытия'] = str(params['Дата выбытия']).split('.')
    persons = per
    r = getAnswer(url, search)
    count = findCount(r)
    print(page, ' - ', count)
    if (count > 0):
        soup = BeautifulSoup(r.text, "html.parser")
        ids = [tag['id'] for tag in soup.select('div[id]')] 
        for i in range(0, len(ids)):
            percent = 0
            if (str(ids[i]).isdigit()):
                person = analyzeRecord(ids[i])
                person['id'] = ids[i]
                try:
                    if (dict(person).keys().__contains__('Дата рождения/Возраст') and bool(str(params['Дата рождения/Возраст']))):
                        person['Дата рождения/Возраст'] = birthYear(person['Дата рождения/Возраст'])
                        print(person['Дата рождения/Возраст'], params['Дата рождения/Возраст'])
                        if (person['Дата рождения/Возраст'] == params['Дата рождения/Возраст']):
                            percent += 0.6
                    if (dict(person).keys().__contains__('Дата выбытия') and bool(str(params['Дата выбытия'][0]))):
                        person['Дата выбытия'] = deathDate(person['Дата выбытия'])
                        print(person['id'], ' ', person['Дата выбытия'], ' ', params['Дата выбытия'])
                        if (person['Дата выбытия'][2] == params['Дата выбытия'][2]):
                            percent += 0.3
                            if (person['Дата выбытия'][1] == params['Дата выбытия'][1]):
                                percent += 0.2
                                if (dict(person).keys().__contains__('Причина выбытия') and bool(str(params['Причина выбытия']))):
                                    if (person['Причина выбытия'] == params['Причина выбытия']):
                                        percent += 0.1
                                if (person['Дата выбытия'][0] == params['Дата выбытия'][0]):
                                    percent += 0.1
                except Exception:
                    print("Exception!")
                person['percent'] = percent
                #print(person)
            if percent >= 0.6:
                print("DADADADA")
                persons.append(person)
        if (count == 100):  #Возможно, что найдено более одной страницы (мало вероятно)
            search['p'] = str(page + 1)
            getRecords(page + 1, params, persons)
        else:
            print(persons)
    return list(persons)