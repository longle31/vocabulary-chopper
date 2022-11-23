import requests

class DictionaryRestClient:
    def __init__(self, url):
        self.url = url

    def get(self, word):
        try:
            return requests.get(self.url + word).json()
        except:
            return None