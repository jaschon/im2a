#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
from os import path

__author__ = "Jason Rebuck"
__copyright__ = "2011/2012"
__version__ = "v.18"

##########
# USAGE ##
##########
#
# im2a = Image2Ascii(<image name>, <block size>, <character map list>) <!--inits and sets values
# im2a.setMap(<character map list>) <!-- (OPTIONAL) replaces character map
#
# im2a.addTitle("My Title Here") <!--add a text title to the bottom of the image [EXPERIMENTAL]
#
# im2a.ascii() <!-- writes text to file
# im2a.text(<text spacing>) <!-- writes text and color list to file
# im2a.blocks(<blocksize>) <!-- writes color list as blocks in an image file
# im2a.ellipse(<blocksize>) <!-- writes color list as ellipses in an image file

class Image2Ascii:
    """Translate Image To ASCII Characters"""
    def __init__(self, image, blockSize=10, charMap = ('#',"$","*","!","'"," ")):
        self.imageName = image #save name of image
        self.blockSize = blockSize #size of squares
        self.charMap = charMap #your color mapping. [dark -> light]
        self.outputText = [] #create empty output list
        self.outputColor = [] #create empty output list
        self.titleText = []
        self.titleColor = []
        self.hasRun = False #flag to tell if run function has been called
        try:
            self.image = Image.open(self.imageName).convert("L") #open image and convert to b&w
            self.x, self.y = self.image.size #get image size
        except IOError, e:
            print "Ooops, I Can't Open the Image!"
            raise

    def setMap(self, newMap):
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
        if self.outputText and self.outputColor: #mark flag as run
            self.hasRun = True

    def addTitle(self, text, spacer="*", color=0):
        self.checkRun()
        if self.outputText and (len(text) <= len(self.outputText[-1])): #make sure text will fit
            halfLen = round(len(self.outputText[-1])/2.0) #get half of row length
            halfText = round(len(text)/2.0) #get half of text length
            text = str(text).replace(" ", spacer).upper() #format text
            textRow = [ ' ' for i in self.outputText[0] ] #make blank text row
            extraRow = textRow[0:] #extra copy of text row
            colorRow = [ 255 for i in self.outputText[0] ] #make a white color row
            counter = 0 # start with 0.
            for i in range(int(halfLen-halfText), int(halfLen-halfText) + len(text)):
                textRow[i] = text[counter] #replace text char of that spot in row
                colorRow[i] = 0 #replace text char of that spot in row
                counter += 1 #inc counter
            self.titleText.append(textRow) #add text row
            self.titleText.append(extraRow) #add text row
            self.titleColor.append(colorRow) #add color row
            self.titleColor.append(colorRow) #add color row
        else:
            print "Oops, Title is Too Long"

    def checkRun(self):
        if not self.hasRun:
            self.run()

    def blocks(self, blockSize=10):
        """Output to Image of Colored Blocks"""
        self.checkRun()
        im = OutputImageGeneric(self, blockSize)
        im.loop()
        im.save()

    def text(self, space=10):
        """Output to Image of Colored Text"""
        self.checkRun()
        im = OutputImageText(self, space)
        im.loop()
        im.save()

    def ascii(self):
        """Output to Ascii Text File"""
        self.checkRun()
        im = OutputAsciiText(self)
        im.loop()
        im.save()

    def ellipse(self, blockSize=10):
        """Output to Image of Colored Ellipses"""
        self.checkRun()
        im = OutputImageEllipse(self, blockSize)
        im.loop()
        im.save()

class OutputImageGeneric:
    """Output To Blocks of Color"""
    def __init__(self, imObject, blockSize=''):
        self.setupLists(imObject) #save lists
        self.setFileName(imObject.imageName) #set filename
        self.blockSize = blockSize or imObject.blockSize #set blocksize
        self.setSize() #set height and width
        self.setupImage() #setup output file and other objects

    def setupLists(self, imObject):
        self.outputColor = imObject.outputColor #set object colorlist
        self.outputText = imObject.outputText #set object textlist

    def setupImage(self):
        self.outImage = Image.new("L", (self.width, self.height), 255) #make output image
        self.draw = ImageDraw.Draw(self.outImage) #make draw object
        self.font = ImageFont.load_default() #setup font object

    def setSize(self):
        self.height= len(self.outputColor) * self.blockSize #cal height
        self.width = len(self.outputColor[0]) * self.blockSize #cal width

    def setFileName(self,fileName):
	root, ext = path.splitext(fileName) #get root name
	self.fileName = "{0}_blocks.png".format(root) # make file name

    def loop(self):
        row = 0 #var to change row in outputColor array
	for y in range(0, self.height, self.blockSize): #loop through height
            x = 0 #x val
	    for col in range(0, len(self.outputColor[row])): #loop through width
                self.writeLn(x,y,row,col) #send loop var to write function
                x += self.blockSize #inc x val
            row += 1 #inc row

    def writeLn(self, x, y, row, col):
        try:
            self.draw.rectangle((x, y, x+self.blockSize, y+self.blockSize), self.outputColor[row][col] ) #draw rectangle
        except:
            print "Unable To Write Block Image Line! ({0},{1})".format(x,y)

    def save(self):
        self.outImage.save(self.fileName) #save to file

class OutputImageText(OutputImageGeneric):
    """Writes Output as Colored Text"""
    def setFileName(self,fileName):
	root, ext = path.splitext(fileName) #get root name
	self.fileName = "{0}_text.png".format(root) # make file name

    def setupLists(self, imObject):
        self.outputColor = imObject.outputColor + imObject.titleColor #set object colorlist
        self.outputText = imObject.outputText + imObject.titleText #set object textlist

    def writeLn(self, x, y, row, col):
        try:
            self.draw.text((x, y), self.outputText[row][col], font=self.font, fill=self.outputColor[row][col] ) #write colored text
        except OSError:
            print "Unable To Write Image Text Line! ({0},{1})".format(x,y)

class OutputImageEllipse(OutputImageGeneric):
    """Writes Output as Colored Ellipses"""
    def setFileName(self,fileName):
	root, ext = path.splitext(fileName) #get root name
	self.fileName = "{0}_ellipse.png".format(root) # make file name

    def writeLn(self, x, y, row, col):
        try:
            self.draw.ellipse((x, y, x+self.blockSize, y+self.blockSize), self.outputColor[row][col] ) #write ellipse
        except:
            print "Unable To Write Ellipse Line! ({0},{1})".format(x,y)

class OutputAsciiText(OutputImageGeneric):
    """Writes Output to Ascii Text File"""
    def setFileName(self, fileName):
        root, ext = path.splitext(fileName) #take off extention
        self.fileName = "{0}_ascii.txt".format(root) #add '.txt' extention

    def setupLists(self, imObject):
        self.outputColor = imObject.outputColor + imObject.titleColor #set object colorlist
        self.outputText = imObject.outputText + imObject.titleText #set object textlist

    def setupImage(self):
        pass #skip setup function [other objects not needed]

    def save(self):
        pass #skip save function [does this in loop()]

    def loop(self):
        try:
            f = open(self.fileName, 'w') #create new file
            for i in self.outputText: #loop through output array
                f.write(''.join(i)) #join array to solid string
                f.write('\n') #add an extra line break
            f.close() #close file when done
        except:
            print "Unable to Write File!"
            raise


if __name__ == "__main__":
    im = Image2Ascii('examples/note.jpg', 5) #load image
    #im.setMap(range(10)) #sets custom character map
    im.addTitle("Image Test") #adds title to ascii and text image
    im.ascii() #output to text file
    im.blocks() #output to block image
    im.text()
    im.ellipse()


