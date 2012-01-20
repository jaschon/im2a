#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from os import path

__author__ = "Jason Rebuck"
__copyright__ = "2011/2012"
__version__ = "v.16"

##########
# USAGE ##
##########
#
# im2a = Image2Ascii(<image name>, <block size>, <character map list>) <!--inits and sets values
# im2a.setCharMap(<character map list>) <!-- (OPTIONAL) replaces character map is new list
#
# im2a.run() <!--converts image to ascii. saves all data to a list. (self.outputText)
# im2a.output2text() <!-- writes list to file
# im2a.output2image(<blocksize>, <useText-True|False>) <!-- writes list to image file 


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
        except IOError, e:
            print "Ooops, I Can't Open the Image!"
            raise

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

    def run(self):
        """Loop Through Each Block in Image and Translate Each Value to a List Value"""
        yBreak = False
        self.outputText = [] #clear output list
        self.outputColor = [] #clear output list
        for y in range(0, self.y+self.blockSize, self.blockSize): #loop through height
            yMax = y + self.blockSize
            xBreak = False
            self.outputText.append([]) #new row in output
            self.outputColor.append([]) #new row in output
            if yMax >= self.y: #if value is more than height, give height and flag for loop break
                yMax = self.y
                yBreak = True
            for x in range(0, self.x, self.blockSize): #loop through width
                xMax = x + self.blockSize
                if xMax >= self.x: #if value is more than width, give width and flag for loop break
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

    def addTitle(self, text, spacer="*", color=0):
        if self.outputText and (len(text) <= len(self.outputText[-1])): #make sure text will fit
            halfLen = round(len(self.outputText[-1])/2.0) #get half of row length
            halfText = round(len(text)/2.0) #get half of text length
            text = str(text).replace(" ", spacer).upper() #format text
            textRow = self.outputText[-1][0:] #copy a text row
            colorRow = self.outputColor[-1][0:] #copy a color row
            counter = 0 # start with 0.
            for i in range(int(halfLen-halfText), int(halfLen-halfText) + len(text)):
                textRow[i] = text[counter] #replace text char of that spot in row
                colorRow[i] = color #replace color of that spot in row
                counter += 1 #inc counter
            self.outputText.append(textRow) #add text row
            self.outputText.append(self.outputText[-2][0:]) #copy extra row for spacing
            self.outputColor.append(colorRow) #add color row
            self.outputColor.append(self.outputColor[-2][0:]) #copy extra row for spacing
        else:
            print "Oops, Title is Too Long"
                
    def output2text(self):
        """Writes Output to Text File"""
        root, ext = path.splitext(self.imageName) #take off extention
        fileName = "{0}_text.txt".format(root) #add '.txt' extention
        try:
            if self.outputText: #make sure there is data in the list
                f = open(fileName, 'w') #create new file
                for i in self.outputText: #loop through output array
                    f.write(''.join(i)) #join array to solid string
                    f.write('\n') #add an extra line break
                f.close() #close file when done
            else:
                print "Ooops! You Need to Run Convert First."
        except:
            print "Unable to Write File!"
            raise

    #multi function to output as a text image or an image of tone blocks
    def _outputImage(self, blockSize, useText=True):
        """Writes Output to Image File"""
        if not blockSize:
            blockSize = self.blockSize #lets you scale output size
	root, ext = path.splitext(self.imageName) #get root name
        if useText:
	    fileName = "{0}_image.png".format(root) # make file name
        else:
	    fileName = "{0}_blocks.png".format(root) # make file name
	try:
          height = len(self.outputColor) * blockSize #get output image size
          width = (len(self.outputColor[0]) * blockSize)
	  outImage = Image.new("L", (width, height), 255) #make new image object
          draw = ImageDraw.Draw(outImage) #make draw object
          if useText:
              font = ImageFont.load_default() #load default font (for now)
	except:
	   print "Unable to Write Image File"
	   raise
        row = 0 #var to change row in outputColor array
	for y in range(0, height, blockSize): #loop through height
            x = 0 #x val
	    for col in range(0, len(self.outputColor[row])): #loop through width
                if useText:
                    draw.text((x, y), self.outputText[row][col], font=font, fill=self.outputColor[row][col] )
                    #draw text letter in correct color
                else:
                    draw.rectangle((x, y, x+blockSize, y+blockSize), self.outputColor[row][col] ) #else draw block
                x += blockSize
            row += 1
        outImage.save(fileName) #write to output image


    #easy to use wrapper for outputImage
    def output2blocks(self, blockSize=10):
        self._outputImage(blockSize, False)

    #easy to use wrapper for outputImage
    def output2image(self, blockSize=10):
        self._outputImage(blockSize)


if __name__ == "__main__":

    im = Image2Ascii('note.jpg', 5) #load image
    im.run() #collect and process image data
    im.addTitle("this is a super long title to show what this function can do!")
    im.output2text() #output to text file
    im.output2image() #output to text image
    im.output2blocks() #output to block image


