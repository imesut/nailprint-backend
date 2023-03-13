#import libraries
import PIL
from PIL import Image
 
img=Image.open('kare.JPEG') 
#binarization function
def binarize(img):
  #convert image to greyscale
  img=img.convert('L') 
  
  # img.show()
  width,height=img.size
  print(img.getpixel((width/2, height/2)))
  print(img.getpixel((1051, 371)))

  #initialize threshold
  thresh=140


  #traverse through pixels 
  for x in range(width):
    for y in range(height):

      #if intensity less than threshold, assign white
      if img.getpixel((x,y)) < thresh:
        img.putpixel((x,y),0)

      #if intensity greater than threshold, assign black 
      else:
        img.putpixel((x,y),255)

  return img

bin_image=binarize(img)
bin_image.show()
