# -*- coding: utf-8 -*-

from .context import exporter
from exporter.osclient import OSClient

import unittest


class OSClientTestSuite(unittest.TestCase):

    def test_uninitialized_token_is_invalid(self):
       osclient = OSClient(None, None, None, None, None, None, None, None)
       self.assertFalse(osclient.is_valid_token())


if __name__ == '__main__':
    unittest.main()
