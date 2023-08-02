import os
import yaml
from yaml.loader import SafeLoader
import datetime


class Counter:
    def __init__(self, limit_count):
        self.limit_count = limit_count
        self.moment = datetime.datetime.now()
        self.current_date = self.moment.strftime("%Y-%m-%d")
        self.current_count = 0
        self.load()

    def inc(self):
        actual_moment = datetime.datetime.now()
        actual_date = actual_moment.strftime("%Y-%m-%d")
        result = True
        if self.current_date != actual_date:
            self.moment = actual_moment
            self.current_date = actual_date
            self.current_count = 0
            self.save()
        else:
            if self.next():
                self.current_count += 1
                self.save()
            else:
                result = False
        return result

    def next(self):
        return self.current_count < self.limit_count

    def load(self):
        if os.path.exists('config/request_count.yaml'):
            with open('config/request_count.yaml') as f:
                request_count_yaml = yaml.load(f, Loader=SafeLoader)
                if self.current_date == request_count_yaml['current_date']:
                    self.current_count = int(request_count_yaml['current_count'])

    def save(self):
        with open('config/request_count.yaml', 'w') as f:
            request_count_dict = [{'current_date': self.current_date, 'current_count': self.current_count}]
            yaml.dump(request_count_dict, f)

