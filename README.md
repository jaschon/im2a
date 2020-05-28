

# im2a #


 *This started out as a simple image-to-ascii converter written in python...*



## REQUIREMENTS #

- Python 2.7.1+
- PIL 1.1.7+
 


## USAGE #

```
 im2a = Image2Ascii(<image name>, <block size>, <character map list>) # inits and sets values
 im2a.setMap(<character map list>) # (OPTIONAL) replaces character map

 im2a.ascii() # writes text to file
 im2a.text(<ttf font filename>, <font size>) # writes text and color list to file
 im2a.blocks(<blocksize>) # writes color list as blocks in an image file
 im2a.ellipse(<blocksize>) # writes color list as ellipses in an image file
 im2a.dot(<blocksize>) # writes color list as different sized dots in an image file
 
 ```



##  DEFAULT CHAR MAP #

 #### This is the default character map that I used for testing: 
 
 > #, $, *, !, ', <space>
 
 >[dark -----------> light]

 #### Use the 'setCharMap()' method to set your own.
 
 ```
 im2a.setCharMap(['a','b','c','d'])
 ```

