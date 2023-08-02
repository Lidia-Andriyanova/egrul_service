import os
import yaml
from yaml.loader import SafeLoader
import datetime
import base64
import json
from dicttoxml import dicttoxml
import service
import utils
import logger
import counter


logger = logger.Logger()

# Настройки ФНС
if os.path.exists('config/fns_service.yaml'):
    with open('config/fns_service.yaml') as f:
        fns_service = yaml.load(f, Loader=SafeLoader)
else:
    logger.add_event('config', "Файл config/fns_service.yaml не существует", True, True)
    exit()

# Тест
print(fns_service)
fns_service['day_request_count'] = 1

# Определение количества выполненных http-запросов за текущий день
counter = counter.Counter(fns_service['day_request_count'])

# Определение лимита http-запросов в день
if not counter.next():
    logger.add_event('request_limit', 'Достигнут лимит на ' +
                     str(fns_service['day_request_count']) + ' http-запросов к сервису в день ', True, True)
    exit()

# Получение временного сохраненного токена доступа (если есть)
access_token = None
if os.path.exists('config/access_token.yaml'):
    with open('config/access_token.yaml') as f:
        access_token_yaml = yaml.load(f, Loader=SafeLoader)
        access_token = access_token_yaml['accessToken']
        access_end = utils.xmltimestamp_2date(access_token_yaml['accessTokenEndDate'])

while counter.next():

    # Получение нового временого токена доступа от сервиса (если его нет или устарел) и запись в файл
    if access_token is None or (access_end - datetime.datetime.now()).total_seconds() < fns_service['last_request_seconds']:
        access_token_response = service.AccessTokenRequest(fns_service['requests']['access_token'],
                                                           fns_service['master_token'])
        access_token_json, access_token_error = access_token_response.exec_request()
        logger.add_event('http', access_token_json, access_token_error)
        counter.inc()

        if not access_token_error:
            access_token = access_token_json['accessToken']
            access_end = utils.xmltimestamp_2date(access_token_json['accessTokenEndDate'])
            with open('config/access_token.yaml', 'w') as f:
                documents = yaml.dump(access_token_json, f)
        else:
            logger.last_event()
            exit()

    # Тест
    print(access_token, access_end)

    if not counter.next():
        break

    # Перевод временного токена в формат base64
    byte_token = base64.b64encode(bytes(access_token, 'utf-8'))
    exec_token = byte_token.decode('utf-8')

    # Получение списка ЮЛ и ИП на дату
    date_request_response = service.DateRequest(fns_service['requests']['date_events'],
                                                exec_token, '2023-01-19')
    date_json, date_error = date_request_response.exec_request()
    counter.inc()

    if not date_error:
        logger.add_event('http', 'Запрос по ЮЛ и ИП на дату ' + '2023-01-19' + ' получен', date_error)
    else:
        logger.add_event('http', date_json, date_error, True)
        exit()

    # Тест
    print(date_json)

    if not counter.next():
        break




# json_ul, error_ul = service.date_request(requests['date_events'], exec_token, '2023-01-19')

# date_request_response = service.DateRequest(requests['date_events'], exec_token, '2023-01-19')
# json_ul, error_ul = date_request_response.exec_request()

#
# with open('ul_date.json', 'w', encoding='utf-8') as f:
#     json.dump(json_ul, f, ensure_ascii=False, indent=4)
#
#
# # xml_ul = dicttoxml(json_ul, return_bytes=False)
# # print(xml_ul)
#
# # with open('ul_date.xml', 'w', encoding='utf-8') as file_info:
# #     file_info.write(xml_ul)
#
#
# country_ul = json_ul['registrations']
#
# fns_region = 56
#
# region_ul = [elem for elem in country_ul if elem.get('ifts', '')[:2] == str(fns_region)]
#
# for i in range(0, len(region_ul)):
#     print(str(i + 1).ljust(4), region_ul[i].get('ifts', '').ljust(6), str(region_ul[i].get('taxpayerType', 2)).ljust(3), region_ul[i].get('ogrn', '').ljust(17), region_ul[i].get('taxpayerName', ''))
#
#
# with open('ul_region.txt', 'w', encoding='utf-8') as file_info:
#     for i in range(0, len(region_ul)):
#         line = str(i + 1).ljust(4) + region_ul[i].get('ifts', '').ljust(6) + str(region_ul[i].get('taxpayerType', 2)).ljust(3) + region_ul[i].get('ogrn', '').ljust(17) + region_ul[i].get('taxpayerName', '') + '\n'
#         file_info.write(line)
#
#
# for elem in region_ul:
#     ogrn = elem.get('ogrn', '');
#     if ogrn != '':
#         tax_type = elem.get('taxpayerType', 2)
#         ul_type = 'ul' if tax_type == 0 else 'ip'
#
#         ogrn_content = service.ul_request(exec_token, ogrn)
#         ogrn_xml_ul = ogrn_content.decode()
#         # print(ogrn_xml_ul)
#         file_name = ul_type + '_' + ogrn + '.xml'
#         with open(file_name, 'w', encoding='utf-8') as file_info:
#             file_info.write(ogrn_xml_ul)
#             print(file_name)
#
#
logger.last_event()