#import web
#import json
import person
import shutil
import mparser
import time
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl import load_workbook

def getDict(t):
    with open("ReductionsJson/t" + str(t) + ".json", "r") as read_file:
        return json.load(read_file)

def main():
    #shutil.copyfile(r"ts.xlsx", r"ts1.xlsx")
    time.sleep(1)
    #Кароч метод LoadFile не хочет возвращать wb, вывод питон - х##ня
    wb = load_workbook("test.xlsx", data_only=True)
    sheet = wb.active

    p = person.MakePersonList(sheet)
    for perid in range(len(p)):
        info = p[perid]['info']
        p[perid] = mparser.parse(info, p[perid])
    size = person.GetSize(sheet)
    for i in range(2, size - 1):
        j = 6
        while (j < 22):
            if (p[i-2][person.field_name[j-1]] != None):
                sheet[get_column_letter(j) + str(i)].value = p[i-2][person.field_name[j-1]]
            else:
                sheet[get_column_letter(j) + str(i)].value = ""
            j += 1
    wb.save("tx.xlsx")
    #search = {'f':'Пылькин', 'ps': '100'}
    #params = 0
    #web.getRecords(search, page = 1, params = params)

if __name__ == "__main__":
    main()