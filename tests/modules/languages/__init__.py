import json
import unittest

from mypass.core.languages import Language


class TestLanguage(unittest.TestCase):
    def test_lang(self):
        message = Language()
        json_str = message.data_not_valid()
        #print(message.data_not_valid())
        mew = json.dumps(json_str, ensure_ascii=False)
        print(mew)
    
test = TestLanguage()
if __name__ == '__main__':
    test.test_lang()