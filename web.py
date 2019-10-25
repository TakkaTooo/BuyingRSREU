import requests
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
    print(data)

def getRecords(search, page, params):    
    url = "https://obd-memorial.ru/html/search.htm"
    r = getAnswer(url, search)
    count = findCount(r)
    print(page, ' - ', count)
    if (count > 0):    #Найден хоть кто - то (в теории проходим по каждому и сравниваем с нашим человеком)
        #-- Действия:                                                                           --#
        #-- Выполняем запрос по id человека на сайте                                            --#
        #-- Выполняем сравнивание данных из params c данными, которые получаем в ответе сервера --#
        #-- Возвращаем значение, если совпало все как надо, не вызывая функцию еще раз          --#
        soup = BeautifulSoup(r.text, "html.parser")     
        ids = [tag['id'] for tag in soup.select('div[id]')] 
        for i in range(0, len(ids)):
            if (str(ids[i]).isdigit()):
               analyzeRecord(ids[i]) 
        if (count == 100):  #Возможно, что найдено более одной страницы (мало вероятно)
            search['p'] = str(page + 1)
            getRecords(search, page + 1, params)
    return 0