#!/usr/bin/env python
import sys
import os.path
import unittest

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import configgen.utils.videoMode as videoMode

class VideoModeUtilTest(unittest.TestCase):
    pass
    #def test_createSimpleFillValues(self):
    #   self.assertEquals(videoMode.createVideoModeLine("10"), "tvservice -e 10 CEA HDMI")

    #def test_createAddHDMI(self):
    #    self.assertEquals(videoMode.createVideoModeLine("10 CEA"), "tvservice -e 10 CEA HDMI")
    #def test_createDontAddWhenLineCompelete(self):
    #    self.assertEquals(videoMode.createVideoModeLine("10 CEA HDMI"), "tvservice -e 10 CEA HDMI")

if __name__ == '__main__':
    unittest.main()
