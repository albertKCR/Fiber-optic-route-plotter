import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pyautogui
import PIL.ImageGrab
import math

dic = r'img2.png'
img = cv.imread(dic)
#cv.imshow("x",img)


cor_para_amarelo = (255, 0, 0)

im = Image.open(dic).convert('RGB')
#plt.imshow(im)
#plt.show()

# Pega a imagem como um numpy.array com formato altura x largura x num_canais
data = np.array(im)

vermelho, verde, azul = data.T

# Defino a condição (ser branco)
condicao = (vermelho >= 200) & (verde >= 150) & (azul <= 50)
# Substitui a cor branca pela cor desejada
data[condicao.T] = cor_para_amarelo

# Volto o array para uma imagem do PIL
im2 = Image.fromarray(data)
im2.save("seeYellow.png")


img = cv.imread("seeYellow.png")
#cv.imshow("y",img)

grey = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
#plt.imshow(grey,cmap="gray")
#plt.show()


kernel = np.ones((2,2),np.uint8)
# Blurring and erasing little details
grey = cv.GaussianBlur(grey,(9,9),0)
grey = cv.morphologyEx(grey, cv.MORPH_OPEN, kernel)
grey = cv.morphologyEx(grey, cv.MORPH_CLOSE, kernel)
#plt.imshow(grey,cmap="gray")
#plt.show()

canny = cv.Canny(grey,170,200)
#plt.imshow(canny,cmap="gray")
#plt.show()


circles = cv.HoughCircles(canny,
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


#img1 = cv.imread("img3.png")


print("###")


#plt.imshow(cimg)

red_image = PIL.Image.open(dic)
red_image_rgb = red_image.convert("RGB")
counter = 0
verde = 0
vermelho = 0
amarelo = 0


for i in circles[0,:]:
  rgb_pixel_value = red_image_rgb.getpixel((i[0],i[1]))
  print(rgb_pixel_value)
  if rgb_pixel_value == (38, 115, 0):
    verde = verde+1
  elif rgb_pixel_value == (255, 0, 0):
    vermelho = vermelho+1
  elif rgb_pixel_value == (255, 170, 0):
    amarelo = amarelo+1
  counter = 1+counter

postes_livre = amarelo+verde

#info[0,x]=coordenada, info[1,x]=cor
info = []
for y in range(2):
  linha = []
  for x in range(postes_livre):
    linha.append(0)
  info.append(linha)
aux1 = 0
for i in circles[0,:]:
  rgb_pixel_value = red_image_rgb.getpixel((i[0],i[1]))
  print(rgb_pixel_value)
  if rgb_pixel_value == (38, 115, 0):
    verde = verde+1
  elif rgb_pixel_value == (255, 0, 0):
    vermelho = vermelho+1
  elif rgb_pixel_value == (255, 170, 0):
    amarelo = amarelo+1
  if (rgb_pixel_value == (255, 170, 0)) or (rgb_pixel_value == (38, 115, 0)):
    info[0][aux1] = i
    info[1][aux1] = rgb_pixel_value
    aux1 = aux1+1
  counter = 1+counter


print("Número de postes:", counter)
print("Número de postes em verde:", verde)
print("Número de postes em vermelho:", vermelho)
print("Número de postes em amarelo:", amarelo)
print("Postes livres (amarelo e verde):", postes_livre)

plt.axis("off")
plt.plot([18,45],[42,54])
plt.imshow(im)
plt.show()
plt.savefig('foo.png', bbox_inches='tight', transparent = True)
print(type(circles))
print(math.dist([18,45],[42,54]))


#for i in info[0][:]:
#  print(i[0])

mais_perto=999
for i in info[0][:]:
  j=i+1
  for j in info[0][:]:
    if math.dist([i[0],j[0]],[i[1],j[1]])<mais_perto and i[0]!=j[0] and i[1]!=j[1]:
      mais_perto=math.dist([i[0],j[0]],[i[1],j[1]])
      x_1=i[0]
      x_2=j[0]
      y_1=i[1]
      y_2=j[1]
print(mais_perto)
print(x_1)
print(x_2)
print(y_1)
print(y_2)
