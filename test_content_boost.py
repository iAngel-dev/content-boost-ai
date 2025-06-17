import unittest
from content_boost import app

class ContentBoostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"G\xc3\xa9n\xc3\xa9rateur d'id\xc3\xa9es de contenu TikTok", response.data)

    def test_index_post_empty(self):
        response = self.app.post('/', data={'topic': ''})
        self.assertIn(b"Veuillez entrer un sujet valide.", response.data)

    def test_index_post_long(self):
        long_topic = 'a' * 101
        response = self.app.post('/', data={'topic': long_topic})
        self.assertIn(b"Le sujet est trop long", response.data)

if __name__ == '__main__':
    unittest.main()
