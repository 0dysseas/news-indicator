import json
import os


def print_json_object(obj):
    print 'PRINTING JSON OBJECT'
    print (json.dumps(obj, indent=4))


def get_news_sources_from_file():
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    source_file = os.path.join(absolute_path, 'assets/news_sources.txt')

    with open(source_file, 'r') as f:
        news_sources = dict()
        for line in f:
            if not line.startswith('#') and line.split():
                split_line = line.split(' = ')
                news_sources[split_line[0]] = split_line[1].rstrip('\n')

    return news_sources


def delete_redundant_items(json_news, keys_to_del):
    for item in keys_to_del:
        del json_news[item]

        return json_news
