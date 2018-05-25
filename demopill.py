#Import libraries
from PIL import Image
from PIL import ImageDraw
 
#Image Size
EPD_WIDTH       = 176
EPD_HEIGHT      = 264
# Create a white mask 
mask = Image.new('1', (EPD_HEIGHT,EPD_WIDTH), 255)   
#Create a Draw object than allows to add elements (line, text, circle...) 
draw = ImageDraw.Draw(mask)
#Some Text
draw.text((EPD_HEIGHT/4,EPD_WIDTH/2), 'Demo Python PILL', fill = 0)
#Horizontal line
draw.line((0,EPD_WIDTH/2 + 12, EPD_HEIGHT, EPD_WIDTH/2 + 12), fill = 0)
#Save the picture on disk
mask.save('demopill.bmp',"bmp")
