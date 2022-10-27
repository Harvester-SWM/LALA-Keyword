from os import walk
from xml.dom.minidom import Document
import json

PATH_1 = './모욕'
PATH_2 = './통매음'

result_1 = {
    'document' : [

    ]
}

result_2 = {
    'document' : [

    ]
}

document_format = {
    'case_name':'',
    'sentence' : []
}

f1 = open('test_1.json', 'w')
f2 = open('test_2.json', 'w')

path_1 = []
for (dirpath, dirnames, filenames) in walk(PATH_1):
    filenames.sort()
    path_1.extend(filenames)
    break

path_2 = []
for (dirpath, dirnames, filenames) in walk(PATH_2):
    filenames.sort()
    path_2.extend(filenames)
    break

for i in path_1:
    temp = document_format.copy()
    temp['case_name'] = i
    result_1['document'].append(temp)
    

for i in path_2:
    temp = document_format.copy()
    temp['case_name'] = i
    result_2['document'].append(temp)


# json dump하기

json.dump(result_1, f1, ensure_ascii=False)
json.dump(result_2, f2, ensure_ascii=False)

f1.close()
f2.close()
