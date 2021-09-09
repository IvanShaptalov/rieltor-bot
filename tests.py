import unittest


class ConfigTest(unittest.TestCase):
    def test_config_valid(self):
        try:
            import config_interpreter
        except KeyError as e:
            self.fail(e)


class ApiTest(unittest.TestCase):
    def test_internet_connection(self):
        import requests
        google = 'https://www.google.com/'
        try:
            requests.get(google)
        except Exception as e:
            print(e)
            self.fail('check internet connection')

    def test_main_data_from_api(self):
        from utils import api
        result = api.get_main_data_by_id(8)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
