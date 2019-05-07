import re
import socket
import subprocess
import requests
from collections import namedtuple
import json


class ASTracer:
    def __init__(self, target):
        self.target = target
        self.result_form = namedtuple('result_form', 'number ip as_number country provider')
        self.source_site = 'http://ip-api.com/json/'

    def get_tracert_results(self):
        tracert_result = subprocess.check_output(['tracert', self.target]).decode('utf-8', 'ignore')
        return re.findall(r'(?<=\s)\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', tracert_result)

    def get_site_info(self, site_addr):
        response = requests.get('http://ip-api.com/json/' + site_addr)
        return json.loads(response.text)
        
    def parse_json_data(self, number, data):
        ip = ''
        country = ''
        as_number = ''
        provider = ''
        for item in data:
            if item == 'query':
                ip = data[item]
            if item == 'country':
                country = data[item]
            if item == 'as':
                as_number = data[item].split(' ')[0]
            if item == 'org':
                provider = data[item]
        return self.result_form(number, ip, as_number, country, provider)

    def make_output(self, result):
        with open('output.txt', 'w') as f:
            for nt in result:
                f.write('number: ' + str(nt.number) + '   ' 
                + 'ip: ' + nt.ip + '   ' + 'as_number: ' + nt.as_number + '   ' 
                + 'country: ' + nt.country + '   ' + 'provider: ' + nt.provider + '\n')
    
    def run(self):
        result_list = []
        tracert_result = self.get_tracert_results()
        for number in range(len(tracert_result)):
            json = self.get_site_info(tracert_result[number])
            result_list.append(self.parse_json_data(number, json))
        self.make_output(result_list)

    



tr = ASTracer('24.48.0.1')
tr.run()
a = 1