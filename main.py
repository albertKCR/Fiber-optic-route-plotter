import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyautogui
import PIL.ImageGrab

img = cv.imread(r'C:\Users\kirch\OneDrive\Documentos\img3.png')
cv.imshow("x",img)

##
cor_para_amarelo = (255, 0, 0)

im = Image.open(r'C:\Users\kirch\OneDrive\Documentos\img3.png').convert('RGB')

# Pega a imagem como um numpy.array com formato altura x largura x num_canais
data = np.array(im)

vermelho, verde, azul = data.T

# Defino a condição (ser branco)
condicao = (vermelho >= 200) & (verde >= 150) & (azul <= 50)
# Substitui a cor branca pela cor desejada
data[condicao.T] = cor_para_amarelo

# Volto o array para uma imagem do PIL
im2 = Image.fromarray(data)
im2.save("aaa.png")
##

img = cv.imread("aaa.png")
cv.imshow("y",img)

grey = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
plt.imshow(grey,cmap="gray")
plt.show()


kernel = np.ones((2,2),np.uint8)
# Blurring and erasing little details
grey = cv.GaussianBlur(grey,(9,9),0)
grey = cv.morphologyEx(grey, cv.MORPH_OPEN, kernel)
grey = cv.morphologyEx(grey, cv.MORPH_CLOSE, kernel)
plt.imshow(grey,cmap="gray")
plt.show()

canny = cv.Canny(grey,170,200)
plt.imshow(canny,cmap="gray")
plt.show()


circles = circles = cv.HoughCircles(canny,
                          cv.HOUGH_GRADIENT,
                          dp=1.1,
                          minDist=5,
                          param1=27,
                          param2=7,
                          minRadius=0,
                          maxRadius=10)

print(len(circles[0]))

# Changing the dtype  to int
circles = np.uint16(np.around(circles))
cimg = canny.copy()
for i in circles[0,:]:
    # draw the center of the circle
    cv.circle(cimg,(i[0],i[1]),2,(255,0,0),10)

for i in circles[0,:]:
  print(i)


img1 = cv.imread("img3.png")


print("###")




#print(grey[57,213])


plt.imshow(cimg)


for i in circles[0,:]:


red_image = PIL.Image.open(r'C:\Users\kirch\OneDrive\Documentos\img3.png')
red_image_rgb = red_image.convert("RGB")
rgb_pixel_value = red_image_rgb.getpixel((57,213))
print(rgb_pixel_value)