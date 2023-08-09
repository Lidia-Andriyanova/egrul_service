import os
import yaml
from yaml.loader import SafeLoader
import datetime


class Perioder:
    def __init__(self):
        self.periods = []
        self.load()

    def load(self):
        if os.path.exists('config/period.yaml'):
            with open('config/period.yaml') as f:
                period_yaml = yaml.load(f, Loader=SafeLoader)
                print(period_yaml)
                for element in period_yaml['periods']:
                    # period = Period(element['period'])
                    # self.periods.append(period)
                    period = element['period']
                    start_date = period['start_date']
                    now_date = datetime.datetime.now().date()
                    end_date = period['end_date'] if 'end_date' in period and period['end_date'] < now_date else now_date
                    print(start_date, end_date)

                    delta_date = datetime.timedelta(days=1)
                    exclude_days = period['exclude_days'] if 'exclude_days' in period else []
                    while start_date <= end_date:
                        print(start_date)

                        if start_date not in self.periods and start_date.weekday() not in exclude_days:
                            self.periods.append(start_date)

                        start_date += delta_date

                print(self.periods)
                start_date -= delta_date
                print(start_date, start_date in self.periods)



