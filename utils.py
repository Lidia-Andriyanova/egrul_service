import datetime


def xmltimestamp_2date(xml_str):
    return datetime.datetime(int(xml_str[:4]), int(xml_str[5:7]), int(xml_str[8:10]),
                             int(xml_str[11:13]), int(xml_str[14:16]), int(xml_str[17:19]))