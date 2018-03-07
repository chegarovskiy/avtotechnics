import re
import json
from collections import namedtuple

import requests
import requests.cookies
from http.cookies import SimpleCookie
from urllib.parse import urlencode
#response = requests.post('http://b2b.ad.ua/Account/Login?ReturnUrl=%2F', data={'ComId': '15', 'UserName': '10115', 'Password': 'e89f1a11', 'RememberMe': False, '__RequestVerificationToken': '<TOKEN>'})
cookies = requests.cookies.RequestsCookieJar()
headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}
token = None
response = requests.get(
    'http://b2b.ad.ua/',
    headers=headers
)

if response.status_code == 200:
    for history_response in response.history:
        cookies.update(history_response.cookies)
    cookies.update(response.cookies)
    content = response.text
    print(response.text)
    match = re.search(
        r'<input\s+name="__RequestVerificationToken"\s+type="hidden"\s+value="(?P<value>[a-zA-Z0-9_-]+)"\s*/>',
        content,
    )
    if match:
        token = match.groupdict().get('value')
        pass
    pass

response = requests.post(
    'http://b2b.ad.ua/Account/Login?ReturnUrl=%2F',
    data={
        'ComId': '15',
        'UserName': '10115',
        'Password': 'e89f1a11',
        'RememberMe': False,
        '__RequestVerificationToken': token,
    },
    cookies=cookies,
    headers=headers,
)
if 200 <= response.status_code < 400:
    for history_response in response.history:
        cookies.update(history_response.cookies)
    cookies.update(response.cookies)
    content = response.text
    print(response.text)
else:
    print('Login failed with', response.status_code, response.reason)
    exit(1)

response = requests.get('http://b2b.ad.ua/art/335810', cookies=cookies, headers=headers,)
if 200 <= response.status_code < 400:
    for history_response in response.history:
        cookies.update(history_response.cookies)
    cookies.update(response.cookies)
    content = response.text
    print(response.text)
for cookie in cookies.items():
    print('cookie', cookie)


"""
query = dict(code='3')
response = requests.get('http://b2b.ad.ua/api/catalog/groups?{query}'.format(query=urlencode(query)), cookies=cookies, headers=headers)
print('             ',response.text)
"""

mark_dict = dict() # {id_mark : name_mark}
mod_dict = dict() # {id_model : id_mark}
type_dict = dict() #{type_id : id_model}
type_name_dict = dict() #{type_id : name_type}

grup_dict = dict() # {type_id : [ ]}
total_grups_list = list() # []

ACURA_mark_dict = dict() # тестовый словарь на одну марку
ZAZ_mark_dict = dict() # тестовый словарь на одну марку
ACURA_mark_dict[1505] = 'ACURA'
ZAZ_mark_dict[1139] = 'ZAZ'


"""
response = requests.get('http://b2b.ad.ua/api/catalog/marks', cookies=cookies, headers=headers)
print(response.json())

# парисм все марки
if 200 <= response.status_code < 400:
    all_marks_list = list(response.json())
    for current_mark in all_marks_list:
        mark_dict[current_mark['MARK_ID']] = current_mark['Name']
        print(current_mark['MARK_ID'], current_mark['Name'])
print(mark_dict.__len__())


# парсим все модели
for mark_id in mark_dict.keys():
    query = dict(code=1139)
    response = requests.get('http://b2b.ad.ua/api/catalog/models?{query}'.format(query=urlencode(query)), cookies=cookies, headers=headers)
    if 200 <= response.status_code < 400:
        all_models_list = list(response.json())
        for current_mod in all_models_list:
            mod_dict[current_mod['MOD_ID']] = current_mod['MARK_ID']
            print(current_mod['MARK_ID'], current_mod['MOD_ID'])
print(mod_dict.__len__())

"""

"""
query = dict(code=1139)
response = requests.get('http://b2b.ad.ua/api/catalog/models?{query}'.format(query=urlencode(query)), cookies=cookies, headers=headers)
if 200 <= response.status_code < 400:
    all_models_list = list(response.json())
    for current_mod in all_models_list:
        mod_dict[current_mod['MOD_ID']] = current_mod['MARK_ID']
        print(current_mod['MARK_ID'], current_mod['MOD_ID'])
        print(mod_dict.__len__())
#парсим все типы
for model_id in mod_dict.keys():
    query = dict(code=model_id)
    response = requests.get('http://b2b.ad.ua/api/catalog/types?{query}'.format(query=urlencode(query)),
                            cookies=cookies, headers=headers)
    if 200 <= response.status_code < 400:
        all_types_list = list(response.json())
        for current_type in all_types_list:
            type_dict[current_type['typ_id']] = current_type['MOD_ID']
            type_name_dict[current_type['typ_id']] = current_type['name_full']
            print('typ_id = ',current_type['typ_id'], 'name_full = ', current_type['name_full'])


# парсим групы

all_type_list_grp_subgrp = list() #[[ type_id, подгрупа, група], ...]

for type_id in type_dict.keys():
    query = dict(code=type_id)
    response = requests.get('http://b2b.ad.ua/api/catalog/groups?{query}'.format(query=urlencode(query)),
                            cookies=cookies, headers=headers)
    if 200 <= response.status_code < 400:
        type_list_grp_subgrp = list()
        all_grups = dict(response.json())
        for key, value in all_grups.items():
            grp_dict = dict()
            if (key == 'subgrp'):
                for cur_subgrp in list(value):
                    curType_subgrps_list = list()  # {name_group, name_sub_group}                  
                    curType_subgrps_list.append(type_id)
                    curType_subgrps_list.append(cur_subgrp['grp'])
                    curType_subgrps_list.append(cur_subgrp['code'])
                    all_type_list_grp_subgrp.append(curType_subgrps_list)
                    # print('id_type: ', type_id,  'подгрупа: ', cur_subgrp['code'], 'група: ', cur_subgrp['grp'])

for k in all_type_list_grp_subgrp:
    print(k[0], k[1], k[2])



# список запчастей (код, цена, ...)
curr_lisl_item_for_subgrup = list()
#all_cars_items__list = list()
#f = open('parts.txt', 'w')
for k in all_type_list_grp_subgrp:
    query = dict(code=k[0], group=k[2])
    response = requests.get('http://b2b.ad.ua/api/catalog/items?{query}'.format(query=urlencode(query)), cookies=cookies, headers=headers)
    if 200 <= response.status_code < 400:
        items_parts_dict = dict(response.json())
        for key, val in items_parts_dict.items():
            if(key == 'items'):
                for item in list(val):
                    curr_lisl_item_for_subgrup.append(k[0])
                    curr_lisl_item_for_subgrup.append(k[1])
                    curr_lisl_item_for_subgrup.append(k[2])
                    curr_lisl_item_for_subgrup.append(item['Item'])
                    #f.write(str(item['Item'])')
                    curr_lisl_item_for_subgrup.append(item['Price'])
                    curr_lisl_item_for_subgrup.append(item['Retail'])
                    print(k[0], k[1], k[2], item['Item'], item['Price'], item['Retail'])

"""
"""
list_items = list()
list_items_without_duplicate = list()
f = open('parts.txt', 'r')
f1 = open('list_items_without_duplicate.txt', 'w')
for line in f:
    list_items.append(line)

list_items_without_duplicate = list(set(list_items))
f.close()
print(list_items.__len__())
print(list_items_without_duplicate.__len__())
for i in list_items_without_duplicate:
    f1.write(str(i))
f1.close()
"""

# запчасти с привязанными аналогами
list_spare_parts = list()
f = open('list_items_without_duplicate.txt', 'r')
f1 = open('test.txt', 'w')
L = [item.replace('\n', '') for item in f]
for item in L:
    # print(item)
    query = dict(code=item)
    response = requests.get('http://b2b.ad.ua/api/catalog/replace?{query}'.format(query=urlencode(query)), cookies=cookies, headers=headers)
    print('    ', response.status_code, response.json())
    curr_spares = dict()
    curr_spares[item] = response.text
    list_spare_parts.append(curr_spares)
    # проверка на новые номера из аналогов
    for k, v in dict(response.json()).items():
        if (k == 'items'):
            for numb_spare in v:
                print(numb_spare['Item'])
                f1.write(str(numb_spare['Item']))

test_spare_count = list()
for line in f1:
    test_spare_count.append(line)
print(test_spare_count.__len__())


f.close()
f1.close()







f = open('list_items_without_duplicate.txt', 'r')
headers['Content-Type'] = 'text/html'
response = requests.post('http://b2b.ad.ua/api/catalog/stockitems', json={'items' : "''MH OC90OF ''"}, cookies=cookies, headers=headers)
print(response.status_code, response.reason, repr(response.text))


# for item in f:
#     enc_item = '\'\'' + item.strip() + '\'\''
#     response = requests.post('http://b2b.ad.ua/api/catalog/stockitems', json=dict(items=enc_item), cookies=cookies, headers=headers)
#     print(response.status_code, response.reason, repr(response.text))
#
# f_stocks = open('quontity_parts_in_stocks.txt', 'w')
# for quontity_item in response.json():
#     print(quontity_item['ItemNo'], quontity_item['LocationCode'], quontity_item['Qty'])
#     f_stocks.write(str(quontity_item))
#
#


























