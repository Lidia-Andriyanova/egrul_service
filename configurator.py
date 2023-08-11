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
import perioder
import counter


class Configurator:
    def __init__(self):
        self.access_token = ''
        self.date_events = ''
        self.ogrn = ''
        self.day_request_count = 0
        self.last_request_seconds = 0
        self.master_token = ''
        self.regions = []

    def load(self):
        try:
            if os.path.exists('config/fns_service.yaml'):

                with open('config/fns_service.yaml') as f:
                    fns_service = yaml.load(f, Loader=SafeLoader)

                    self.access_token = fns_service['requests']['access_token']
                    self.date_events = fns_service['requests']['date_events']
                    self.ogrn = fns_service['requests']['ogrn']

                    self.day_request_count = fns_service['day_request_count']
                    self.last_request_seconds = fns_service['last_request_seconds']
                    self.master_token = fns_service['master_token']
                    self.regions = fns_service['regions']
            else:
                return {'event_type': 'config', 'error': True, 'critical_error': True, 'detail': 'Конфигурационный файл config/fns_service.yaml отсутствует'}
        except:
            return {'event_type': 'config', 'error': True, 'critical_error': True, 'detail': 'Ошибка загрузки конфигурационного файла config/fns_service.yaml'}
