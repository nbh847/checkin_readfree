# a checkin script for readfree
import requests
from config.setting import *
from bs4 import BeautifulSoup

class RunReadfree(object):

    def __init__(self):

        self.headers = {'User-Agent': USERAGENT, 'Cookie': COOKIES, 'Host': HOST,
                        'Connection': 'keep-alive'}
        self.url = 'http://readfree.me/'

    def get_contemt(self):
        result = requests.get(self.url, headers=self.headers).text
        soup = BeautifulSoup(result, 'lxml')
        print (soup)


    def run(self):
        self.get_contemt()

if __name__ == "__main__":
    rr = RunReadfree()
    rr.run()