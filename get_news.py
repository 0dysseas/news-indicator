import requests
import logging
from get_news_helpers import print_json_object

# TODO-me: Add an attribution link that reads "Powered by NewsAPI"

# TODO-me: Put the list of links in another module(base_API_endpoints) and import it from there using Queues to operate
# on it

# TODO-me: Split news and sports sources?


logging.basicConfig(level=logging.INFO)

API_KEY = 'XXX-XXX-XXX'


# Base API endpoints
guardian = 'https://newsapi.org/v1/articles?source=the-guardian-uk&sortBy=latest&apiKey=' + API_KEY
al_jaz = 'https://newsapi.org/v1/articles?source=al-jazeera-english&sortBy=latest&apiKey=' + API_KEY
hacker_news_top = 'https://newsapi.org/v1/articles?source=hacker-news&sortBy=top&apiKey=' + API_KEY
nation_geog_top = 'https://newsapi.org/v1/articles?source=national-geographic&sortBy=top&apiKey=' + API_KEY
tech_radar_top = 'https://newsapi.org/v1/articles?source=techradar&sortBy=top&apiKey=' + API_KEY
next_web = 'https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=' + API_KEY
ny_times = 'https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey=' + API_KEY

news_sources = [guardian, al_jaz, hacker_news_top, nation_geog_top, tech_radar_top, next_web, ny_times]

latest_news = dict()


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

    def retrieve_news(self):
        for key, value in enumerate(self.sources):
            response = requests.get(value).json()
            # print_json_object(response)
            self.form_news_structure(response)
            print_json_object(response)


def main():
    news = News(news_sources)
    logging.info('Retrieving news...')
    news.retrieve_news()


if __name__ == '__main__':

    main()









