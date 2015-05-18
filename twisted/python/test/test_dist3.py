# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for L{twisted.python.dist3}.
"""

from __future__ import absolute_import, division

import os
import twisted

from twisted.trial.unittest import TestCase
from twisted.python.dist3 import modulesToInstall
from twisted.python.dist3 import testDataFiles, _processDataFileList


class ModulesToInstallTests(TestCase):
    """
    Tests for L{modulesToInstall}.
    """
    def test_sanityCheck(self):
        """
        L{modulesToInstall} includes some obvious module names.
        """
        self.assertIn("twisted.internet.reactor", modulesToInstall)
        self.assertIn("twisted.python.test.test_dist3", modulesToInstall)


    def test_exist(self):
        """
        All modules listed in L{modulesToInstall} exist.
        """
        root = os.path.dirname(os.path.dirname(twisted.__file__))
        for module in modulesToInstall:
            segments = module.split(".")
            segments[-1] += ".py"
            path = os.path.join(root, *segments)
            alternateSegments = module.split(".") + ["__init__.py"]
            packagePath = os.path.join(root, *alternateSegments)
            self.assertTrue(os.path.exists(path) or
                            os.path.exists(packagePath),
                            "Module {0} does not exist".format(module))


    def test_dataFileExist(self):
        """
        All data files in L{testDataFiles} exist.
        """
        root = os.path.dirname(os.path.dirname(twisted.__file__))
        for file in testDataFiles:
            self.assertTrue(os.path.exists(os.path.join(root, file)))


    def test_processDataFileList(self):
        """
        L{_processDataFileList} translates a list of files into a distutils
        friendly format.
        """
        result = _processDataFileList(["foo/bar.py", "foo/baz/bar.py",
                                       "foo/z.out", "baz/spam.py"])
        self.assertIn(("foo", ["foo/bar.py", "foo/z.out"]),
                      result)
        self.assertIn(("foo/baz", ["foo/baz/bar.py"]),
                      result)
        self.assertIn(("baz", ["baz/spam.py"]),
                      result)
