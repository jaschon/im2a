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
        self.testFile = "test.jpg"
        im = Image.new( 'L', (200,200), 0)
        im.save(self.testFile)

        #run im2a
        self.im = Image2Ascii(self.testFile) #run test file
        self.im.convert() #collect/convert data
        self.im.output2image() #make text image
        self.im.output2image(0, False) #make block image

        #set up output image names
        self.testTextImage = "{0}_image.png".format(self.testFile.replace(".jpg","")) 
        self.testBlockImage = "{0}_blocks.png".format(self.testFile.replace(".jpg",""))

    def test__OutputList(self):
        """Make Sure Data Has Been Collected"""
        self.assertTrue(self.im.outputText)
        self.assertTrue(self.im.outputColor)

    def test__OutputPaths(self):
        """Make Sure Output Images Were Created"""
        self.assertTrue(os.path.isfile(self.testFile))
        self.assertTrue(os.path.isfile(self.testTextImage))
        self.assertTrue(os.path.isfile(self.testBlockImage))

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

if __name__ == "__main__":
    unittest.main() #Run All Tests






 
