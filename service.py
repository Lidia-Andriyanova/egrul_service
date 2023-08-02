import requests
from requests.exceptions import Timeout, ConnectionError
import datetime


class BearerAuth(requests.auth.AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class ServiceRequest:

    def __init__(self, use_request, token):
        self.use_request = use_request
        self.token = token
        self.response = ''

    def request_string(self):
        return self.use_request

    def request_format(self):
        self.response = requests.post(self.request_string())
        return self.response

    def request_ok_result(self):
        return self.response.json()

    def request_fail_result(self):
        return self.response.json()

    def exec_request(self):
        try:
            response = self.request_format()
            if response.status_code != 200:
                return self.request_fail_result(), True
            return self.request_ok_result(), False
        except Timeout:
            return 'Ошибка таймаута ' + self.request_string(), True
        except ConnectionError:
             return 'Ошибка соединения ' + self.request_string(), True
        except:
             return 'Ошибка получения ответа ' + self.request_string(), True


class AccessTokenRequest(ServiceRequest):

    def request_format(self):
        self.response = requests.post(self.request_string(), json={'masterToken': self.token})
        return self.response


class DateRequest(ServiceRequest):

    def __init__(self, use_request, token, date):
        super().__init__(use_request, token)
        self.date = date

    def request_string(self):
        return self.use_request + self.date

    def request_format(self):
        self.response = requests.get(self.request_string(), auth=BearerAuth(self.token))
        return self.response

    def set_date(self, date):
        self.date = date


class OgrnRequest(ServiceRequest):

    def __init__(self, use_request, token, ogrn):
        super().__init__(use_request, token)
        self.ogrn = ogrn

    def request_string(self):
        return self.use_request + self.ogrn

    def request_format(self):
        self.response = requests.get(self.request_string(), auth=BearerAuth(self.token))
        return self.response

    def request_ok_result(self):
        return self.response.content

    def set_ogrn(self, ogrn):
        self.ogrn = ogrn


# def access_token_request(use_request, token):
#     response = requests.post(use_request, json={'masterToken': token})
#     return response.json()
#
#
# def date_request(use_request, token, date):
#     try:
#         response = requests.get(use_request + date, auth=BearerAuth(token))
#         if response.status_code != 200:
#             return response.json(), True
#         return response.json(), False
#     except Timeout:
#         return 'Ошибка таймаута ' + use_request  + date, True
#     except ConnectionError:
#         return 'Ошибка соединения ' + use_request + date, True
#     except:
#         return 'Ошибка получения ответа ' + use_request + date, True
#
#
# def ul_request(token, ogrn):
#     response = requests.get('https://openapi.tax.gov.ru/egrul-api/v1/vyp-xml/' + ogrn, auth=BearerAuth(token))
#     return response.content
#
