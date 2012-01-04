#!/usr/bin/env python

from PIL import Image, ImageDraw
from os import path

__author__ = "Jason Rebuck"
__copyright__ = "2011/2012"
__version__ = "v.12"

##########
# USAGE ##
##########
#
# im2a = Image2Ascii(<image name>, <block size>, <character map list>) <!--inits and sets values
# im2a.setCharMap(<character map list>) <!-- (OPTIONAL) replaces character map is new list
#
# im2a.convert() <!--converts image to ascii. saves all data to a list. (self.outputText)
# im2a.output2text() <!-- writes list to file
# im2a.output2image() <!-- writes list of colored blocks back to image 


class Image2Ascii:
    """Translate Image To ASCII Characters"""

    def __init__(self, image, blockSize=10, charMap = ('#',"$","*","!","'"," ")):
        self.imageName = image #save name of image
        self.blockSize = blockSize #size of squares
        self.charMap = charMap #your color mapping. [dark -> light]
        self.outputText = [] #create empty output list
        self.outputColor = [] #create empty output list
        try:
            self.image = Image.open(self.imageName).convert("L") #open image and convert to b&w
            self.x, self.y = self.image.size #get image size
        except:
            print "Ooops, I can't Open the Image!"

    def setCharMap(self, newMap):
        if type(newMap) in (list, tuple):
            self.charMap = newMap

    def _mapChar(self, num):
        """Map Color Value to List Value""" 
        for c in range(1, len(self.charMap)+1):
            if num <= round(c*(256.0/len(self.charMap))):
                return str(self.charMap[c-1]) #return char (make sure it is a string!)
        return str(self.charMap[0]) #if nothing found, give the first value

    def _getAverage(self, pixels):
        """Get Average Color in Pixel Block"""
        try:
            return round(float(sum(pixels))/len(pixels))
        except:
            return 255 #if out of range or no pixel values, return white

    def convert(self):
        """Loop Through Each Block in Image and Translate Each Value to a List Value"""
        yBreak = False
        self.outputText = [] #clear output list
        self.outputColor = [] #clear output list
        for y in range(0, self.y+self.blockSize, self.blockSize): #loop through height
            yMax = y + self.blockSize
            xBreak = False
            self.outputText.append([]) #new row in output
            self.outputColor.append([]) #new row in output
            if yMax > self.y: #if value is more than height, give height and flag for loop break
                yMax = self.y
                yBreak = True
            for x in range(0, self.x, self.blockSize): #loop through width
                xMax = x + self.blockSize
                if xMax > self.x: #if value is more than width, give width and flag for loop break
                    xMax = self.x
                    xBreak = True
                # remember: cropbox is (left, upper, right, bottom)
                region = self.image.crop( (x, y, xMax, yMax) ) #crop region box
                # get average color in block, map char and add char to outputText
                colorAvg = self._getAverage(list(region.getdata()))
                self.outputText[-1].append( self._mapChar( colorAvg ))
                self.outputColor[-1].append( colorAvg )
                if xBreak: #break when you reach the max width
                    break
            if yBreak: #break when you reach the max height
                break

    def output2text(self):
        """Writes Output to Text File"""
        root, ext = path.splitext(self.imageName) #take off extention
        fileName = root + ".txt" #add '.txt' extention
        try:
            if self.outputText: #make sure there is data in the list
                f = open(fileName, 'w') #create new file
                for i in self.outputText: #loop through output array
                    f.write(''.join(i)) #join array to solid string
                    f.write('\n') #add an extra line break
                f.close() #close file when done
            else:
                print "Ooops! You Need to Run Process First."
        except:
            print "Unable to Write File!"

    def output2blocks(self, blockSize=0):
        """Writes Output to Image File"""
        if not blockSize:
            blockSize = self.blockSize #lets you scale output size
	root, ext = path.splitext(self.imageName) #get root name
	fileName = root + ".png" # make file name
	try:
          height = len(self.outputColor) * blockSize #get output image size
          width = len(self.outputColor[0]) * blockSize
	  outImage = Image.new("L", (width, height), 255) #make new image object
          draw = ImageDraw.Draw(outImage) #make draw object
	except:
	   print "Unable to Write Image File"
	   raise
        row = 0 #var to change row in outputColor array
	for y in range(0, height, blockSize): #loop through height
            x = 0 #x val
	    for color in self.outputColor[row]: #loop through width
                draw.rectangle((x, y, x+blockSize, y+blockSize), color )
                x += blockSize
            row += 1
        outImage.save(fileName) #write to output image


if __name__ == "__main__":

    #test if not using in another script
    im = Image2Ascii('test.jpg')
    im.convert()
    im.output2blocks(50)
    im.output2text()


