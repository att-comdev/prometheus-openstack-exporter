# -*- coding: utf-8 -*-

from exporter.osclient import OSClient


def test_uninitialized_token_is_invalid():
    osclient = OSClient(None, None, None, None, None, None, None, None)
    assert osclient.is_valid_token() is False
