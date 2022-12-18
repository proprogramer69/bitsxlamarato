import cv2
import numpy as np
def main(png):
    image = cv2.imread(png)
    img = cv2.imread(png)

    blur = cv2.blur(image,(11,11))
     #l'altre potser 70 / 50/ 20/ 50
    imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    color1 = np.array([0, 0, 0], np.uint8)
    mi1 = 0
    mi2 = 0
    mi3 = 0
    mi4= 0
    mila=0
    mila2=0
    mila3=0
    mila4=0

    lin = []
    lin2 = []
    lin3 = []
    lin4 = []


    #img= np.zeros((imgHSV.shape[0],imgHSV.shape[1],3), np.uint8)
    for maska in range(2, 70, 2):
        pts=0
        pts2=0
        pts3 = 0
        pts4 = 0
        color2 = np.array([0, 0, maska], np.uint8)
        mask = cv2.inRange(imgHSV, color1, color2)
        y = 303
        y2 = 269
        y3 = 117
        y4 = 69
        for j in range (mask.shape[1]):
            for i in range (y-3, y+3):
                if mask[i,j] == 0:
                        if mask[i-1,j] == 255 and mask[i-2,j] == 255 and mask[i-3,j] == 255:
                                y = i
                                pts=pts+1
            for i in range(y2 - 5, y2 + 5):
                        if mask[i, j] == 0:
                            if mask[i - 1, j] == 255 and mask[i - 2, j] == 255 and mask[i - 3, j] == 255:
                                y2 = i
                                pts2 = pts2 + 1
            for i in range(y3 - 5, y3 + 5):
                if mask[i, j] == 0:
                    if mask[i + 1, j] == 255 and mask[i + 2, j] == 255 and mask[i + 3, j] == 255:  # abs(i-y4) < 4
                        y3 = i
                        pts3 = pts3 + 1
            for i in range(y4 - 5, y4 + 5):
                if mask[i, j] == 0:
                    if mask[i + 1, j] == 255 and mask[i + 2, j] == 255 and mask[i + 3, j] == 255:  # abs(i-y4) < 4
                        y4 = i
                        pts4 = pts4 + 1

        if pts>mi1:
            mila=maska
            mi1=pts
        if pts2 > mi2:
            mila2 = maska
            mi2 = pts2
        if pts3>mi3:
            mila3=maska
            mi3=pts3
        if pts4 > mi4:
            mila4 = maska
            mi4 = pts4
    color2 = np.array([0, 0, mila3], np.uint8)
    mask = cv2.inRange(imgHSV, color1, color2)

    y = 303
    y2 = 270
    y3 = 98
    y4 = 69
    a = False
    for j in range(mask.shape[1]):
                a = False
                for i in range(y3 - 5, y3 + 5):
                        if mask[i, j] == 0:
                            if mask[i + 1, j] == 255 and mask[i + 2, j] == 255 and mask[i + 3, j] == 255:  # abs(i-y4) < 4
                                if not a:
                                     lin3.append(i)
                                img[i, j] = [142,255,122]
                                y3 = i
                                a = True
                if not a:
                    lin3.append(None)


    color2 = np.array([0, 0, mila4], np.uint8)
    mask = cv2.inRange(imgHSV, color1, color2)
    for j in range(mask.shape[1]):
                a = False
                for i in range(y4 - 5, y4 + 5):
                        if mask[i, j] == 0:
                                if mask[i + 1, j] == 255 and mask[i + 2, j] == 255 and mask[i + 3, j] == 255:  # abs(i-y4) < 4
                                    if not a:
                                        lin4.append(i)
                                    img[i, j] =  [101,255,230]
                                    y4 = i
                                    a = True
                if not a:
                    lin4.append(None)

    color2 = np.array([0, 0, mila], np.uint8)
    mask = cv2.inRange(imgHSV, color1, color2)
    for j in range(mask.shape[1]):
        a = False
        for i in range(y-3, y+3):
            if mask[i, j] == 0:
                    if mask[i - 1, j] == 255 and mask[i - 2, j] == 255 and mask[i - 3, j] == 255:
                        if not a:
                            lin.append(i)
                        img[i, j] = [255,0,0]
                        y = i
                        a = True
        if not a:
            lin.append(None)

    color2 = np.array([0, 0, mila2], np.uint8)
    mask = cv2.inRange(imgHSV, color1, color2)
    for j in range(mask.shape[1]):
        a = False
        for i in range(y2 - 5, y2 + 5):
            if mask[i, j] == 0:
                    if mask[i - 1, j] == 255 and mask[i - 2, j] == 255 and mask[i - 3, j] == 255:
                            if not a:
                                lin2.append(i)
                            img[i, j] = [255,163,255]
                            y2 = i
                            a= True
        if not a:
            lin2.append(None)
    print(lin, lin2, lin3, lin4)
    cv2.imshow('maskRed', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return(lin, lin2, lin3, lin4)

png = '/home/pol/Documentos/HACKATHON/cor2.png'
main(png)