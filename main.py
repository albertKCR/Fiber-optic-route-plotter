import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyautogui
import PIL.ImageGrab
import math

dic = r'img2.png'
img = cv.imread(dic)

im = Image.open(dic).convert('RGB')

#take the image as a numpy.array with the format: height x width x channel_number
data = np.array(im)

#the yellow don't work so well to the image treatment, so replace by red
red, green, blue = data.T

yellowToRed = (255, 0, 0)
condition = (red >= 200) & (green >= 150) & (blue <= 50)
#replace the yellow from the image to red
data[condition.T] = yellowToRed

#return the array to a PIL image
im2 = Image.fromarray(data)
im2.save("yellowToRed.png")
img = cv.imread("yellowToRed.png")


#treatment of the image to recognize the circles
#------------------------------------------------
#swap the RGB for gray
grey = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)

kernel = np.ones((2,2),np.uint8)
#blurring and erasing little details
grey = cv.GaussianBlur(grey,(9,9),0)
grey = cv.morphologyEx(grey, cv.MORPH_OPEN, kernel)
grey = cv.morphologyEx(grey, cv.MORPH_CLOSE, kernel)

#finally the image is just white circles with black background
canny = cv.Canny(grey,170,200)

#recognize the circles e store the coordinates in the "circles" variable
circles = cv.HoughCircles(canny,
                          cv.HOUGH_GRADIENT,
                          dp=1.1,
                          minDist=5,
                          param1=27,
                          param2=7,
                          minRadius=0,
                          maxRadius=10)

#number of found circles
print(len(circles[0]))

#changing the dtype  to int
circles = np.uint16(np.around(circles))
cimg = canny.copy()
for i in circles[0,:]:
    #draw the center of the circle
    cv.circle(cimg,(i[0],i[1]),2,(255,0,0),10)
#------------------------------------------------


#from the coordinates of the circles will happen the color recognize
image = PIL.Image.open(dic)
image_rgb = image.convert("RGB")

postsCounter = 0
greenPostsCounter = 0
redPostsCounter = 0
yellowPostsCounter = 0

coordinates = [] #store the coordinates of each circle
colorInfo = [] #store de color of each circle (as long as it is green, yellow or red)
freePostCounter = 0

for i in circles[0,:]:
  #Reconhece a cor em RGB da coordenada e armazena em "rgb_pixel_value"
  rgb_pixel_value = image_rgb.getpixel((i[0],i[1]))
  #print(rgb_pixel_value)
  if rgb_pixel_value == (38, 115, 0): #count the number of green posts
    greenPostsCounter = greenPostsCounter+1
  elif rgb_pixel_value == (255, 0, 0): #count the number of red posts
    redPostsCounter = redPostsCounter+1
  elif rgb_pixel_value == (255, 170, 0): #count the number of yellow posts
    yellowPostsCounter = yellowPostsCounter+1
  if (rgb_pixel_value == (255, 170, 0)) or (rgb_pixel_value == (38, 115, 0)):
    #if the color of the post is yellow or green, the coordinate and color is appended in the correspondent array
    coordinates.append(i)
    colorInfo.append(rgb_pixel_value)
    freePostCounter = freePostCounter+1
  postsCounter = 1+postsCounter

freePosts = yellowPostsCounter+greenPostsCounter


print("Number of posts:", postsCounter)
print("Number of green posts:", greenPostsCounter)
print("Number of red posts:", redPostsCounter)
print("Number of yellow posts:", yellowPostsCounter)
print("Number of free posts (yellow and green):", freePostCounter)

plt.axis("off")

#each circle will iterate with all the others and check the circle that have the shorter distance (as long as it is shorter then 80)
for i in coordinates[:]:
  shorterDistance = 999999
  shorterDistance2 = 999999
  for j in coordinates[:]:
    if (math.dist([i[0],i[1]],[j[0],j[1]])<shorterDistance) and [i[0],i[1]]!=[j[0],j[1]] and math.dist([i[0],i[1]],[j[0],j[1]])<80:
      shorterDistance=math.dist([i[0],i[1]],[j[0],j[1]])
      x_1=i[0]
      x_2=j[0]
      y_1=i[1]
      y_2=j[1]
    if (math.dist([i[0],i[1]],[j[0],j[1]])<shorterDistance2) and [i[0],i[1]]!=[j[0],j[1]] and math.dist([i[0],i[1]],[j[0],j[1]])<80 and (math.dist([i[0],i[1]],[j[0],j[1]])>shorterDistance):
      shorterDistance2=math.dist([i[0],i[1]],[j[0],j[1]])
      x1_1=i[0]
      x1_2=j[0]
      y1_1=i[1]
      y1_2=j[1]
  #draw a line between the 2 points
  plt.plot([x_1,x_2],[y_1,y_2], 'b')
  plt.plot([x1_1,x1_2],[y1_1,y1_2], 'r')

plt.imshow(im)
plt.savefig("FinalImage.png", transparent = True) 
plt.show()