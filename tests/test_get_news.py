import queue
import pytest

from newsindicator.get_news import DownloadWorker


class TestDownloadWorker:
    def setup_method(self):
        self.out_q = queue.Queue()
        self.dw = DownloadWorker(queue.Queue(), self.out_q)

    def _drain_queue(self):
        items = []
        try:
            while True:
                items.append(self.out_q.get_nowait())
        except Exception:
            pass
        return items

    def test_non_dict_input_returns_empty_and_does_not_put_to_queue(self):
        result = self.dw._form_news_structure(None)
        assert result == []
        assert self._drain_queue() == []

    def test_articles_not_list_returns_empty_and_no_queue_put(self):
        result = self.dw._form_news_structure({'articles': 'not-a-list'})
        assert result == []
        assert self._drain_queue() == []

    def test_valid_articles_processed_and_limited_to_first_four(self):
        json_news = {
            'articles': [
                {'title': 'A', 'url': 'http://a', 'source': {'name': 'S1'}, 'urlToImage': 'imgA'},
                {'title': 'B', 'url': 'http://b', 'source': 'S2'},
                {'title': '', 'url': 'http://c', 'source': {'name': 'S3'}},       # missing title -> skip
                {'title': 'D', 'url': '', 'source': {'name': 'S4'}},             # missing url -> skip
                {'title': 'E', 'url': 'http://e', 'source': {'name': 'S5'}}      # 5th -> should be ignored (max 4)
            ]
        }

        processed = self.dw._form_news_structure(json_news)

        # Only first two articles have both title and url and are within first 4
        assert len(processed) == 2
        titles = [p['title'] for p in processed]
        urls = [p['url'] for p in processed]
        sources = [p.get('source', '') for p in processed]

        assert titles == ['A', 'B']
        assert urls == ['http://a', 'http://b']
        assert sources == ['S1', 'S2']

        queued = self._drain_queue()
        assert queued == processed