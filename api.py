import requests

class DictionaryRestClient:
    def __init__(self, url):
        self.url = url

    def get(self, dictionary, word):
        try:
            response = requests.get(self.url + word, headers={"dictionary": dictionary})
            if response.status_code != 200:
                return None
            return response.json()
        except:
            return None