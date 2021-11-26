import requests, random
import settings
import re

from bs4 import BeautifulSoup

class Google(object):

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': settings.userAgents[random.randint(1, 1)]})
        self.session.proxies.update(settings.proxyDesktopList)
        self.session.verify = settings.CERTIFICATE

    def send_request(self, region, item):
        parse_url = 'https://www.google.com/search?hl=ru&q='+str(item)
        response = self.session.get(parse_url)
        if len(response.text) < 10000:
            self.send_request(region, item)
        return response

    def parse_results(self, item):
        # region = Project.objects.get(id=item.ssystem_id)
        response = self.send_request(157, item)
        soup = BeautifulSoup(response.text, "html.parser")
        texts = soup.find_all('div', {'class': 'yuRUbf'})
        links = []
        i = 1
        for result in texts:
            link = result.find('a', href=True)
            if link:
                links.append({"link": link['href'], "sentiment": "NONE",
                              "jumps":'0', "result_id": i})
                i += 1
        print(links)
        return links

    # def set_results(self, item):
    #     result = Keywords.objects.filter(id=item.id)
    #     links = self.parse_results(item)
    #     result.update(google_parsing_results=json.dumps(links))
    #
    # def update_results(self, item):
    #     links = self.parse_results(item)
    #     items = Keywords.objects.get(id=item.id)
    #     for link in links:
    #         for item_link in json.loads(item.google_parsing_results):
    #             if link['link'] == item_link['link']:
    #                 link['sentiment'] = item_link['sentiment']
    #     result = Keywords.objects.filter(id=item.id)
    #     result.update(google_parsing_results=json.dumps(links))


class Yandex(object):

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': settings.userAgents[random.randint(1, 1)]})
        self.session.proxies.update(settings.proxyDesktopList)
        self.session.verify = settings.CERTIFICATE

    def send_request(self, region, item):
        parse_url = 'https://yandex.ru/search/?lr='+region+'&text='+str(item)
        response = self.session.get(parse_url)
        if len(response.text) < 10000:
            self.send_request(region, item)
        return response

    def parse_results(self, item):
        # region = Project.objects.get(id=item.ssystem_id)
        response = self.send_request('213', item)
        soup = BeautifulSoup(response.text, "html.parser")
        texts = soup.find_all('a', {'class': 'organic__url','accesskey':re.compile(r"\d")} )
        links = []
        i = 1
        for result in texts:
            links.append({"link": result['href'],
                          "sentiment": "NONE",
                          "jumps": 0,
                          "result_id": i})
            i += 1
        print(links)
        return links

    # def set_results(self, item):
    #     result = Keywords.objects.filter(id=item.id)
    #     links = self.parse_results(item)
    #     result.update(yandex_parsing_results=json.dumps(links))
    #
    # def update_results(self, item):
    #     links = self.parse_results(item)
    #     items = Keywords.objects.get(id=item.id)
    #     for link in links:
    #         for item_link in json.loads(item.yandex_parsing_results):
    #             if link['link'] == item_link['link']:
    #                 link['sentiment'] = item_link['sentiment']
    #     result = Keywords.objects.filter(id=item.id)
    #     result.update(yandex_parsing_results=json.dumps(links))


a = Google()
a.parse_results('gfn')