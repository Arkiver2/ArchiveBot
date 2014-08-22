import unittest

from .wpull import WpullArgs
from seesaw.item import Item

def joined(args):
    return str.join(' ', args)

class TestWpullArgs(unittest.TestCase):
    def setUp(self):
        self.item = {
                'cookie_jar': '/foobar/cookies.txt',
                'ident': 'abc123',
                'item_dir': '/foobar',
                'url': 'http://www.example.com',
                'warc_file_base': '/foobar/warc'
        }

        self.args = WpullArgs(default_user_agent='Default/1',
                wpull_exe='/bin/wpull')

    def test_user_agent_can_be_set(self):
        self.item['user_agent'] = 'Frobinator/20.1'

        self.assertIn('-U Frobinator/20.1', joined(self.args.realize(self.item)))

    def test_uses_default_user_agent(self):
        self.assertIn('-U Default/1', joined(self.args.realize(self.item)))

    def test_recursive_fetch_settings(self):
        self.item['recursive'] = True
        self.item['depth'] = 'inf'

        cmdline = joined(self.args.realize(self.item))

        self.assertIn('--recursive', cmdline)
        self.assertIn('--level inf', cmdline)

    def test_nonrecursive_fetch_settings(self):
        self.item['recursive'] = False

        cmdline = joined(self.args.realize(self.item))

        self.assertNotIn('--recursive', cmdline)
        self.assertNotIn('--level inf', cmdline)

    def test_recursive_fetch_enables_linked_pages_and_requisites(self):
        self.item['recursive'] = True
        self.item['depth'] = 'inf'

        cmdline = joined(self.args.realize(self.item))

        self.assertIn('--span-hosts-allow page-requisites,linked-pages',
                cmdline)

    def test_recursive_fetch_with_no_linked_pages_enables_requisites(self):
        self.item['recursive'] = True
        self.item['depth'] = 'inf'
        self.item['no_linked_pages'] = True

        cmdline = joined(self.args.realize(self.item))

        self.assertIn('--span-hosts-allow page-requisites', cmdline)
        self.assertNotIn('linked-pages', cmdline)
        
    def test_nonrecursive_fetch_enables_requisites(self):
        self.item['recursive'] = False

        cmdline = joined(self.args.realize(self.item))

        self.assertIn('--span-hosts-allow page-requisites', cmdline)
        self.assertNotIn('linked-pages', cmdline)

# vim:ts=4:sw=4:et:tw=78
