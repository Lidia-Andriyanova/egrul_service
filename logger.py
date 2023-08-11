import datetime
from dicttoxml import dicttoxml


class Logger:
    def __init__(self):
        self.moment = datetime.datetime.now()
        self.filename = 'log/exec_' + self.moment.strftime("%Y%m%d%H%M%S") + '.xml'
        self.info = {'exec': {'start': self.moment.strftime("%Y-%m-%dT%H:%M:%S")}}
        self.write_log()

    # def add_event(self, event_type, detail, error=False, is_last=False):
    #     now = datetime.datetime.now()
    #     if 'events' not in self.info['exec'].keys():
    #         self.info['exec']['events'] = []
    #     self.info['exec']['events'].append({'datetime': now.strftime("%Y-%m-%dT%H:%M:%S"),
    #                                         'type': event_type, 'error': error, 'detail': detail})
    #     if is_last:
    #         self.last_event()
    #     self.write_log()

    def add_event(self, event):
        now = datetime.datetime.now()
        if 'events' not in self.info['exec'].keys():
            self.info['exec']['events'] = []
        self.info['exec']['events'].append({'datetime': now.strftime("%Y-%m-%dT%H:%M:%S"),
                                            'type': event['event_type'], 'error': event['error'], 'detail': event['detail']})
        if event['critical_error']:
            self.last_event()
        self.write_log()

    def last_event(self):
        now = datetime.datetime.now()
        self.info['exec']['finish'] = now.strftime("%Y-%m-%dT%H:%M:%S")
        self.write_log()

    def write_log(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(dicttoxml(self.info, return_bytes=False, attr_type=False, root=False))

