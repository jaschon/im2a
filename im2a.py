#!/usr/bin/env python

from PIL import Image
from os import path

__author__ = "Jason Rebuck"
__copyright__ = "2011/2012"
__version__ = "v.1"

##########
# USAGE ##
##########
#
# im2a = Image2Ascii(<image name>, <block size>, <character map list>) <!--inits and sets values
# im2a.setCharMap(<character map list>) <!-- (OPTIONAL) replaces character map is new list
#
# im2a.convert() <!--converts image to ascii. saves all data to a list. (self.outputList)
# im2a.write() <!-- writes list to file


class Image2Ascii:
    """Translate Image To ASCII Characters"""

    def __init__(self, image, blockSize=4, charMap = ('#',"$","*","!","'"," ")):
        self.imageName = image #save name of image
        self.blockSize = blockSize #size of squares
        self.charMap = charMap #your color mapping. [dark -> light]
        self.outputList = [] #create empty output list
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
        self.outputList = [] #clear output list
        for y in range(0, self.y+self.blockSize, self.blockSize): #loop through height
            yMax = y + self.blockSize
            xBreak = False
            self.outputList.append([]) #new row in output
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
                # get average color in block, map char and add char to outputList
                self.outputList[-1].append( self._mapChar( self._getAverage(list(region.getdata())) ))
                if xBreak: #break when you reach the max width
                    break
            if yBreak: #break when you reach the max height
                break

    def write(self, fileName=""):
        """Writes Output to Text File"""
        if not fileName: #if not file name given, use the image name as a base
            root, ext = path.splitext(self.imageName) #take off extention
            fileName = root + ".txt" #add '.txt' extention
        try:
            if self.outputList: #make sure there is data in the list
                f = open(fileName, 'w') #create new file
                for i in self.outputList: #loop through output array
                    f.write(''.join(i)) #join array to solid string
                    f.write('\n') #add an extra line break
                f.close() #close file when done
            else:
                print "Ooops! You Need to Run Process First."
        except:
            print "Unable to Write File!"

if __name__ == "__main__":

    #test if not using in another script
    im = Image2Ascii('test.jpg')
    im.convert()
    im.write()


