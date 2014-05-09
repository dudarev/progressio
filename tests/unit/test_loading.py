# -*- coding: utf-8 -*-

import sys

sys.path.insert(0, "../..")

from progressio.progressio import _parse_line
from .base import BaseUnitCase


class TestLoading(BaseUnitCase):
    def test_parse_line(self):
        """Tests function for parsing a line
        """
        line = 'title'
        item = _parse_line(line)
        self.assertEqual(item.title, line)
