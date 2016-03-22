#!/usr/bin/env python
# coding=utf8
import os
import sys
import os.path
import unittest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import configgen.utils.slugify as slugify

class SlugifyUtilTest(unittest.TestCase):

    def test_slugify_horrible_name(self):
        self.assertEquals(slugify.slugify(u'reallt BAD NAME ^ç--(23àçè-'), "reallt-bad-name-c-23ace")
    def test_slugify_name_with_int(self):
        self.assertEquals(slugify.slugify(u'Xbox Gamepad (userspace driver) #2'), "xbox-gamepad-userspace-driver-2")


if __name__ == '__main__':
    unittest.main()
