import pytube
import cv2
import numpy
from PIL import Image
import operator
import time
import math
import sys
import random

def removeNegatives(list):

    i = 0
    try:
        while(True):
            if(list[i][0] < 0 or list[i][1] < 0):
                list.remove(list[i])
                continue
            i+= 1
    except:
        pass



def distance(x1,x2,y1,y2):
    return math.sqrt(math.pow((x1 - x2),2) + math.pow((y1 - y2),2))


class circle():

    def __init__(self,x,y,radius):

        self.x = x
        self.y = y
        self.radius = radius
        self.tolerence = 1

    def isInCircle(self,x1,y1,radius1):
        """ return true, if the point x1,y1 is inside the circle """
        if(distance(self.x,x1,self.y,y1) < (self.radius+radius1)):
            return True
        return False

    def drawCircle(self):
        """ draws the circle """

        pointsList = []
        for i in range(self.y-self.radius-1,self.y+self.radius+1):
            for j in range(self.x-self.radius-1,self.x+self.radius+1):

                dist = distance(j,self.x,i,self.y)-self.radius
                if(dist < self.tolerence and dist > -self.tolerence):
                    #print(j,i,"        ",distance(j,self.x,i,self.y))
                    pointsList.append([j,i])
        return pointsList

imageSize = 900

allCircles = []

maxAttempts = 1000
counter = 0

times = 3000

maxSize = 50

for i in range(times):
    print(str(int((i/times)*100)),"%"," attempts: ",counter)
    if(counter == maxAttempts):
        break
    valid = False
    counter = 0
    while (valid == False and counter < maxAttempts):
        valid = True
        a = circle(random.randint(0,imageSize),random.randint(0,imageSize),random.randint(10,maxSize))
        counter += 1
        for thisCircle in allCircles:

            if(thisCircle.isInCircle(a.x,a.y,a.radius)):
                valid = False


    if(counter < maxAttempts):
        allCircles.append(a)
        #print("Circle added: ",a.radius )


circleData = []
for thisCircle in allCircles:
    circleData = circleData[:] + thisCircle.drawCircle()

im = Image.open("input.png")
imData = list(im.getdata())
width, height = im.size

removeNegatives(circleData)

for point in circleData:

    #print(imData[point[0]*900 + point[1]])
    try:
        imData[point[0]*900 + point[1]] = tuple((0,0,0))
    except:
        pass

im2 = Image.new(im.mode, im.size)
im2.putdata(imData)

im2.save(str("output" + str(random.randint(0,100)) + ".png"))
