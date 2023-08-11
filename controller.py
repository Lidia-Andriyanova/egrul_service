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
import configurator
import perioder
import counter


class Controller:
    def __init__(self):
        self.logger = logger.Logger()
        self.configurator = None

    def run(self):
        # Получить настройки ФНС
        self.get_configurator()

        self.logger.last_event()

    # Настройки ФНС
    def get_configurator(self):
        self.configurator = configurator.Configurator()
        event = self.configurator.load()
        if not (event is None) and event['error']:
            self.logger.add_event(event)
            exit()


