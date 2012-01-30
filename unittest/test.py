#!/usr/bin/env python

import sys
sys.path.append('../im2a')

from im2a import *
import unittest, os

__author__ = "Jason Rebuck"
__copyright__ = "2012"

class TestIm2A(unittest.TestCase):

    def setUp(self):
        """Set Up Test Image And Run im2a"""
        #setup test image
        self.testFile = "images/test.jpg"
        im = Image.new( 'L', (200,200), 0)
        im.save(self.testFile)

        #run im2a
        self.im = Image2Ascii(self.testFile) #run test file
        self.im.text() #make text image
        self.im.blocks() #make block image
        self.im.ellipse() #make ellipse image
        self.im.ascii()

        #set up output image names
        base, ext = os.path.splitext(os.path.basename(self.testFile))
        base = os.path.join(os.path.dirname(self.testFile), base)
        self.testTextImage = "{0}_text.png".format(base) 
        self.testBlockImage = "{0}_blocks.png".format(base)
        self.testEllipseImage = "{0}_ellipse.png".format(base)
        self.testAsciiFile = "{0}_ascii.txt".format(base)

    def test__OutputList(self):
        """Make Sure Data Has Been Collected"""
        self.assertTrue(self.im.outputText)
        self.assertTrue(self.im.outputColor)

    def test__OutputPaths(self):
        """Make Sure Output Images Were Created"""
        self.assertTrue(os.path.isfile(self.testFile))
        self.assertTrue(os.path.isfile(self.testTextImage))
        self.assertTrue(os.path.isfile(self.testBlockImage))
        self.assertTrue(os.path.isfile(self.testEllipseImage))
        self.assertTrue(os.path.isfile(self.testAsciiFile))

    def test__ColorList(self):
        """Make Sure Color List Is All Black"""
        #loop through data and make sure everything is black
        for row in self.im.outputColor:
            for col in row:
                self.assertTrue(col == 0 )

    def test__BlockImage(self):
        """Make Sure Generated Image Is All Black"""
        #loop through image pixels and make sure everything is black
        im = Image.open(self.testBlockImage)       
        pixels = list(im.getdata())
        for i in pixels:
            self.assertTrue(i == 0)

    def test_AsciiText(self):
        """Make Sure Generated Ascii Matches Output List"""
        lines = open(self.testAsciiFile, "r").readlines()
        for r in range(0, len(self.im.outputText)):
            self.assertTrue(len(lines[r]), len(self.im.outputText[r])) #make sure lines are same width
            for c in range(0, len(self.im.outputText[r])):
                self.assertTrue(self.im.outputText[r][c] == lines[r][c]) #make sure characters match

if __name__ == "__main__":
    unittest.main() #Run All Tests






 
