import unittest
from spampost import (
    is_eng_post,
    is_rus_post,
    get_post_toks_len,
    get_html_tags_len,
    is_spam_post,
    remove_urls,
)


class Test(unittest.TestCase):
    def eq_is_eng_post(self, s, b, max_words=5):
        self.assertEqual(is_eng_post(s, max_words=max_words), b)

    def test_is_eng_post(self):
        self.eq_is_eng_post('これは日本語です。this is, a big heaven world.', True)
        self.eq_is_eng_post('これは日本語です', False)
        self.eq_is_eng_post('これは日本語です\nこれは日本語です\nこれは日本語です', False)
        self.eq_is_eng_post('これは this 日本語 is です heaven.', False)
        self.eq_is_eng_post('this is a heaven world.', True)
        self.eq_is_eng_post('<a href="#">mp3</a>', True, max_words=1)
        self.eq_is_eng_post('<a href="#">click me!</a> this is a heaven.', True)
        self.eq_is_eng_post('<a href="#">mp3</a>', False)
        self.eq_is_eng_post('<a href="#">hello</a>', True, max_words=1)

        # russia
        self.eq_is_eng_post('<a href="#">Вы не могли бы мне помочь, пожалуйста?</a>', False)

    def eq_is_rus_post(self, s, b, max_words=5):
        self.assertEqual(is_rus_post(s, max_words=max_words), b)

    def test_is_rus_post(self):
        self.eq_is_rus_post('<a href="#">Вы</a>', False)
        self.eq_is_rus_post('<a href="#">Вы</a>', True, max_words=1)
        self.eq_is_rus_post('<a href="#">Вы, не. могли! Вы? не!</a>', True)
        self.eq_is_rus_post('<a href="#">Вы не могли бы мне помочь, пожалуйста?</a>', True)

    def eq_get_post_toks_len(self, s, n):
        self.assertEqual(get_post_toks_len(s), n)

    def test_get_post_toks_len(self):
        self.eq_get_post_toks_len('これは日本語です', 4)
        self.eq_get_post_toks_len('これは日本語です\nこれは日本語です\nこれは日本語です', 12)
        self.eq_get_post_toks_len('<a href="#">mp3</a>', 2)
        self.eq_get_post_toks_len('<a href="#">mp3 mp3</a>', 4)
        self.eq_get_post_toks_len('<a href="#">mp3 mp3 mp3 mp3</a>', 8)

    def eq_get_html_tags_len(self, s, n):
        self.assertEqual(get_html_tags_len(s), n)

    def test_get_html_tags_len(self):
        self.eq_get_html_tags_len('<a href="#">a</a>', 1)
        self.eq_get_html_tags_len('<a href="#">a</a><a href="#">a</a>', 2)
        self.eq_get_html_tags_len('<a href="#">a</a><a href="#">a</a><a href="#">a</a>', 3)

    def eq_is_spam_post(self, s, b):
        self.assertEqual(is_spam_post(s), b)

    def test_is_spam_post(self):
        self.eq_is_spam_post('こんにちは', True)
        self.eq_is_spam_post('こんにちは。いいお天気ですね。', False)
        self.eq_is_spam_post('''こんにちは。今日はあなた様のWebサイトを拝見しまして、ご連絡いたしました。
ぜひ私どものサイトにリンクを張らせていただきたいと思いまして、事後報告になりますが↓のURLからリンクをご確認ください。
httpx://xxxx.xxx/aaa-bbb.html?ccc=ddd
''', False)
        self.eq_is_spam_post('This', True)
        self.eq_is_spam_post('This is!', True)
        self.eq_is_spam_post('This is hello world!', True)
        self.eq_is_spam_post('Hi admin. My name is Bob. Are you fine?', True)
        self.eq_is_spam_post('<a href="#">mp3</a>', True)
        self.eq_is_spam_post('<a href="#">mp3 mp3</a>', True)
        self.eq_is_spam_post('<a href="#">mp3 mp3 mp3</a>', True)
        self.eq_is_spam_post('<a href="#">mp3 mp3 mp3 mp3</a>', True)
        self.eq_is_spam_post('<a href="#">This is hello world!</a>', True)
        self.eq_is_spam_post('<a href="#">Вы, не. могли!</a>', True)
        self.eq_is_spam_post('<a href="#">Вы не могли бы мне помочь, пожалуйста?</a>', True)

    def eq_remove_urls(self, a, b):
        self.assertEqual(remove_urls(a), b)

    def test_remove_urls(self):
        self.eq_remove_urls('', '')
        self.eq_remove_urls('http', 'http')
        self.eq_remove_urls('http://', '')
        self.eq_remove_urls('ttp://', 'ttp://')
        self.eq_remove_urls('http://xxx.com', '')
        self.eq_remove_urls(' http://xxx.com', ' ')
        self.eq_remove_urls('  http://xxx.com', '  ')
        self.eq_remove_urls(' http://xxx.com ', '  ')
        self.eq_remove_urls('  http://xxx.com  ', '    ')
        self.eq_remove_urls('this is http://xxx.com not url', 'this is  not url')
        self.eq_remove_urls('http://xxx.com ', ' ')
        self.eq_remove_urls('http://xxx.com  ', '  ')
        self.eq_remove_urls('http://xxx.com http://xxx.com', ' ')
        self.eq_remove_urls('this http://xxx.com is http://xxx.com url', 'this  is  url')
        self.eq_remove_urls('http://xxx.com  http://xxx.com', '  ')
        self.eq_remove_urls('http://xxx.com\nhttp://xxx.com', '\n')
        self.eq_remove_urls('http://xxx.com\n\nhttp://xxx.com', '\n\n')
        self.eq_remove_urls('http://xxx.com\thttp://xxx.com', '\t')
        self.eq_remove_urls('http://xxx.com\t\thttp://xxx.com', '\t\t')
