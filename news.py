from news_helpers import print_json_object
import requests


class News(object):

    def __init__(self, sources):
        self.sources = sources

    def __repr__(self):
        return self.sources

    @staticmethod
    def delete_redundant_items(json_news, keys_to_del):
        for item in keys_to_del:
            del json_news[item]

        return json_news

    def form_news_structure(self, json_news):
        keys_to_remove = ['status', 'sortBy']
        sub_keys_to_remove = ['description', 'author', 'publishedAt']  # TODO-me: Handle the National Geographic case

        self.delete_redundant_items(json_news, keys_to_remove)

        for _, article in enumerate(json_news['articles']):
            self.delete_redundant_items(article, sub_keys_to_remove)

    # def retrieve_news(self):
    #     for key, value in enumerate(self.sources):
    #         response = requests.get(value).json()
    #         # print_json_object(response)
    #         self.form_news_structure(response)
    #         print_json_object(response)












