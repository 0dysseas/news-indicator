import requests
from get_news_helpers import print_json_object

# TODO-me:Refactor below in a class

# TODO-me: Add an attribution link that reads "Powered by NewsAPI"

latest_news = {}
API_KEY = 'XXX-XXX-XXX'

# TODO-me: Put the list of links in another module and import it from there
guardian = 'https://newsapi.org/v1/articles?source=the-guardian-uk&sortBy=latest&apiKey=' + API_KEY
al_jaz = 'https://newsapi.org/v1/articles?source=al-jazeera-english&sortBy=latest&apiKey=' + API_KEY
hacker_news_top = 'https://newsapi.org/v1/articles?source=hacker-news&sortBy=top&apiKey=' + API_KEY
nation_geog_top = 'https://newsapi.org/v1/articles?source=national-geographic&sortBy=top&apiKey=' + API_KEY
tech_radar_top = 'https://newsapi.org/v1/articles?source=techradar&sortBy=top&apiKey=' + API_KEY
next_web = 'https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=' + API_KEY
ny_times = 'https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey=' + API_KEY

news_sources = [guardian, al_jaz, hacker_news_top, nation_geog_top, tech_radar_top, next_web, ny_times]

# for key, value in enumerate(news_sources):
#     print key, value

# Latest Guardian headlines
response = requests.get(
    guardian).json()

print_json_object(response)

# Extract {source:{title:url}}, except for National_geo where extract {source:{title:urlToImage}}
# print {response['source']: {response['title']: response['url']}}
for k, v in enumerate(response['articles']):
    print {response['source']: {v['title']: v['url']}}








