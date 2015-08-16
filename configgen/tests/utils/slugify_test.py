#!/usr/bin/env python
# coding=utf8
import os
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import utils.slugify as slugify

class SlugifyUtilTest(unittest.TestCase):

    def test_slugify_horrible_name(self):
        self.assertEquals(slugify.slugify(u'reallt BAD NAME ^ç--(23àçè-'), "reallt-bad-name-c-23ace")


if __name__ == '__main__':
    unittest.main()
