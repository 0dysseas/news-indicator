import unittest

class TestAssert(unittest.TestCase):

    def test_first(self):
        self.assertEqual('foo', 'foo')

    def test_second(self):
        self.assertEqual('bar', 'bar')

    def test_third(self):
        self.assertEqual('foobar', 'foobar')

if __name__ == '__main__':
    unittest.main()