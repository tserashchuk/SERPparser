# from datetime import time
import time
import requests, bs4, random
import settings


from bs4 import BeautifulSoup

class Google(object):

    def __init__(self):
        pro = random.choice(list(settings.proxyDesktopList.items()))
        self.session = requests.Session()
        # self.session.headers.update({'User-Agent': settings.userAgents[random.randint(0, 0)]})
        # self.session.proxies.update({pro[0]: pro[1]})
        # self.proxy = {pro[0]: pro[1]}
        # print(self.proxy)

    def send_request(self, region, item):
        time.sleep(15)
        pri = 'https://www.google.com/search?hl=ru&q='+str(item)
        response = self.session.get(pri)
        # print(response.text)
        if len(response.text) < 10000:
            time.sleep(10)
            # self.__init__()
            self.send_request(region, item)
        return response

    def parse_results(self, item):
        # region = Project.objects.get(id=item.ssystem_id)
        response = self.send_request(157, item)
        soup = BeautifulSoup(response.text, "html.parser")
        texts = soup.find_all('div', {'class': 'kCrYT'})
        # print('------------------------------------------------------------------------------------------')
        # print(texts)
        links = []
        i = 1
        for result in texts:
            link = result.find('a', href=True)
            if link:
                try:
                    print(link['href'].split('?q=')[1].split('&sa')[0])
                except:
                    print(link['href'])
                # links.append({"link": link['href'], "sentiment": "NONE",
                #               "jumps":'0', "result_id": i})
                i += 1
        return links

    def set_results(self, item):
        result = Keywords.objects.filter(id=item.id)
        links = self.parse_results(item)
        result.update(google_parsing_results=json.dumps(links))

    def update_results(self, item):
        links = self.parse_results(item)
        items = Keywords.objects.get(id=item.id)
        for link in links:
            for item_link in json.loads(item.google_parsing_results):
                if link['link'] == item_link['link']:
                    link['sentiment'] = item_link['sentiment']
        result = Keywords.objects.filter(id=item.id)
        result.update(google_parsing_results=json.dumps(links))

class Yandex(object):

    def __init__(self):
        pro = random.choice(list(settings.proxyDesktopList.items()))
        self.session = requests.Session()
        # self.session.headers.update({'User-Agent': settings.userAgents[random.randint(0, 0)]})
        # self.session.proxies.update({pro[0]: pro[1]})
        # self.proxy = {pro[0]: pro[1]}
        # print(self.proxy)

    def send_request(self, region, item):
        time.sleep(15)
        pri = 'https://yandex.ru/search/?lr='+region+'&text='+str(item)
        response = self.session.get(pri)
        if len(response.text) < 10000:
            time.sleep(10)
            # self.__init__()
            self.send_request(region, item)
        return response

    def parse_results(self, item):
        # region = Project.objects.get(id=item.ssystem_id)
        response = self.send_request('157', item)
        print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        texts = soup.find_all('div', {'class': 'path path_show-https organic__path'})
        links = []
        i = 1

        for result in texts:
            link = result.find('a', href=True)
            if link != '':
                links.append({"link": link['href'],
                              "sentiment": "NONE",
                              "jumps": 0,
                              "result_id": i})
                i += 1
        print(links)
        return links

    def set_results(self, item):
        result = Keywords.objects.filter(id=item.id)
        links = self.parse_results(item)
        result.update(yandex_parsing_results=json.dumps(links))

    def update_results(self, item):
        links = self.parse_results(item)
        items = Keywords.objects.get(id=item.id)
        for link in links:
            for item_link in json.loads(item.yandex_parsing_results):
                if link['link'] == item_link['link']:
                    link['sentiment'] = item_link['sentiment']
        result = Keywords.objects.filter(id=item.id)
        result.update(yandex_parsing_results=json.dumps(links))
