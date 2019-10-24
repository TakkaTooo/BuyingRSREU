import requests

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

def getRecord(search, page, params):
    url = "https://obd-memorial.ru/html/search.htm"
    r = getAnswer(url, search)
    count = findCount(r)
    print(page, ' - ', count)
    if (count > 0):    #Найден хоть кто - то (в теории проходим по каждому и сравниваем с нашим человеком)
        #-- Действия:                                                                           --#
        #-- Выполняем запрос по id человека на сайте                                            --#
        #-- Выполняем сравнивание данных из params c данными, которые получаем в ответе сервера --#
        #-- Возвращаем значение, если совпало все как надо, не вызывая функцию еще раз          --#
        if (False):
            return 1
        if (count == 100):  #Возможно, что найдено более одной страницы (мало вероятно)
            search['p'] = str(page + 1)
            getRecord(search, page + 1, params)
    return 0