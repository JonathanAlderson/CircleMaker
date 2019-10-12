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


def isCircleInAnyOtherCircle(this,all):
    """ Sees if a new cirlce is in any other circle """
    for currentCircle in all:
        if(currentCircle.isInCircle(this.x,this.y,this.radius)):
            return True
    return False



for test in range(10):

    imageWidth = 1920
    imageHeight = 1080
    allCircles = []
    maxAttempts = random.randint(10,10000)
    attempts = 0
    times = random.randint(50,8000)
    maxSize = random.randint(50,600)
    minSize = random.randint(1,100)
    quit = False

    for i in range(times):
        print(str(int((i/times)*100)),"%"," attempts: ",attempts)
        if(quit == False):

            newX = random.randint(0,imageWidth)
            newY = random.randint(0,imageHeight)
            a = circle(newX,newY,minSize)

            attempts = 0
            # create a valid circle that's really small
            while(isCircleInAnyOtherCircle(a,allCircles) and attempts < maxAttempts):
                    attempts += 1
                    newX = random.randint(0,imageWidth)
                    newY = random.randint(0,imageHeight)
                    a = circle(newX,newY,minSize)

            if(attempts >= maxAttempts):
                quit = True
                print("Ending Now")
            # keep making it bigger until it dosen't fit
            while(isCircleInAnyOtherCircle(a,allCircles) == False and a.radius < maxSize):
                a = circle(newX,newY,a.radius + 1)

            allCircles.append(a)




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
            if(point[0] > 0 and point[0] < imageWidth and point[1] > 0 and point[1] < imageHeight):
                imData[point[1]*imageWidth + point[0]] = tuple((0,0,0))
        except:
            pass


    textFile = open("count.txt","r")
    value = textFile.read()
    textFile.close()

    textFile = open("count.txt","w")
    textFile.write(str(int(value)+1))
    textFile.close()

    im2 = Image.new(im.mode, im.size)
    im2.putdata(imData)

    im2.save(str("output" + str(int(value)+1) + ".png"))
