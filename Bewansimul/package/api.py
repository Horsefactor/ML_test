import requests
from config import config


class API:
    statusCode = None

    def __init__(self):
        self.url = config['api']['url']
        self.attribute = config['api']['response']
        self.header = {'content-type': 'application/json'}

    def get(self, city_name, country_code, start_time, end_time):
        request = self.url.format(city_name=city_name, country_code=country_code,
                                  start=start_time, end=end_time)
        response = requests.get(request, headers=self.header)
        self.statusCode = response.status_code
        response = response.json()
        self.attribute = self.attribute.split('.')

        for i in range(len(self.attribute)):
            response = response[self.attribute[i]]

        print(response)
        return response




