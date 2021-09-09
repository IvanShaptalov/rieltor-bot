import unittest


class ConfigTest(unittest.TestCase):
    def test_config_valid(self):
        try:
            import config_interpreter
        except KeyError as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()
