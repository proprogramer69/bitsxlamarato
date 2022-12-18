import cv2
import numpy as np
import sys

#################################################################################################

def main(png,a, b, c, d):
    
   
    image = png
    img = png

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
        y = a
        y2 = b
        y3 = c
        y4 = d
        pts=0
        pts2=0
        pts3 = 0
        pts4 = 0
        color2 = np.array([0, 0, maska], np.uint8)
        mask = cv2.inRange(imgHSV, color1, color2)
        
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
                if mask[i + 1, j] == 255 and mask[i + 2, j] == 255 and mask[i + 3, j] == 255:  # abs(i-y4) < 4
                    if mask[i, j] == 0:
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
    
    y = a
    y2 = b
    y3 = c
    y4 = d
    
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

    return lin, lin2, lin3, lin4


#################################################################################################

def detcontraccion(electro): #On electro es una imatge del electrocardiograma retallada als marges dissenyats
    dimv = electro.shape[0]
    dimh = electro.shape[1]
    #print("Dimensio V: ", dimv, " Dimensio H: ", dimh)
    
    #Busquem on comença la linea, tant horitzontalment com verticalment
    x = 0
    y = int(dimv*(1/5))
    
    electro = cv2.GaussianBlur(electro,(7,7),0)
    pics = 0
    diastoles = []
    while x < dimh:
        if electro[y,x][1] > 100:
            pics = pics + 1
            diastoles.append(x)
            #print("Afegida diastoles",x)
            if x+50 > dimh:
                x = x+1
            else:
                x = x+50
        else:
            x = x + 1
    ret = []
    
    #print("\nS'han trobat", pics, "pics, la mida de diastoles es", len(diastoles), "\n")
    
    if len(diastoles) >= 2:
        dist = diastoles[1] - diastoles[0]
        if dist/2 < diastoles[0]:
            ret.append(0) #El primer element és una sistole
            ret.append(int(diastoles[0] - dist/2))
        else:
            ret.append(1) #El primer element és una diastole
    else:
        print("Error")
        sys.exit(1)
        
    #Escriu diastole - sistole, fins acabar
    dist = 0
    for i in range(0,len(diastoles)):
        #print("Afegit",diastoles[i])
        ret.append(diastoles[i])
        if i < len(diastoles) - 1: #Si no és l'última
            dist = (diastoles[i+1] - diastoles[i])/2
            ret.append(int(diastoles[i] + dist))
        else:
            if diastoles[i] + dist < dimh:
                ret.append(int(diastoles[i] + dist))
    
    return ret

#################################################################################################

#input_file = 'C:/Users/Adrià/Desktop/PC/Adrià/Estudis/Uni/Hackathon/videoscor/AVI/995/0W/AVI/2018-06-27-16-22-03_2018-04-13-10-49-44_1.avi'
#numimg = 3 #HAN DE SER COMPLETES!!!!!!!!!!!!!!!!!!!C:/Users/Adrià/Desktop/PC/Adrià/Estudis/Uni/Hackathon/videoscor/AVI/995/0W/AVI/2018-06-27-16-22-03_2018-04-13-10-49-44_1.avi

input_file = input('Indica el directorio hasta el fichero, si pones . emepzará a buscar desdel directorio actual: ')
vidcap = cv2.VideoCapture(input_file)

numimg = int(input('Indica el número de fotos COMPLETAS que tiene el video, poner de más podría dar distancias de media erroneas: '))



print(input_file,numimg)

vidcap = cv2.VideoCapture(input_file)

data = []

it = 19
for i in range(0,numimg):
    for j in range(0,it):
        success, image = vidcap.read()
        
    i1 = image
    success, image = vidcap.read()
    success, image = vidcap.read()
    success, image = vidcap.read()
    i2= image
    if success:
        i1 = i1[0:i1.shape[0], 0:int(i1.shape[1]/2)]
        i2 = i2[0:i2.shape[0], int(i2.shape[1]/2):int(i2.shape[1])]
    
        image1 = np.concatenate((i1, i2), axis=1)
        
        data.append(image1)
        
    if i%3 == 0 and i != 0:
        it -= 2


print("S'han extret les imatges del video",)

#Procesem les imatges en electro i cor

electro = []
cor = []

for x in data:
    print(x.shape[0],x.shape[1])
    electro.append(x[390:445, 15:530])
    cor.append(x[220:380, 15:530])

dimv = cor[0].shape[0]
dimh = cor[0].shape[1]

#Demanem les y's
    
print("A continuació se't mostrarà, imatge per imatge dintre del video font les linies orientatives, l'inici de cada linia ha d'estar a l'inici de cada pared del ventricle, tingues en compte que l'error entre la linia i l'eix real ha de ser molt petit per tal que el programa funcioni correctament")

sis1 = 0 #el 1 es el de dalt de tot
sis2 = 0
sis3 = 0

totsis = 0

dias1 = 0
dias2 = 0
dias3 = 0
totdias = 0

for x in range(0,len(cor)):
    print("------------------------------------------ IMATGE",x+1,"------------------------------------------")
    print("Introdueix un valor inicial per l'eix de les y's, en ordre creixent, tingues en compte que es considera l'eix 0 a dalt a l'esquerra, per tant escriuras de la primera linia a l'última")
    
    conf = 'n'
    eix = []
    dimcv = cor[x].shape[0]
    dimch = cor[x].shape[1]
    
    while conf != 's':
        eix = []
        img = cor[x]
        print("Introdueix els nous valors de Y, han d'estar entre 0 i",dimcv,":")
            
        eix.append(int(input('    Eix Y linea 1: ')))
        for j in range (0,10):
            img[eix[0]][j] = [0,0,255]
            
        eix.append(int(input('    Eix Y linea 2: ')))
        for j in range (0,10):
            img[eix[1]][j] = [0,0,255]
            
        eix.append(int(input('    Eix Y linea 3: ')))
        for j in range (0,10):
            img[eix[2]][j] = [0,0,255]
            
        eix.append(int(input('    Eix Y linea 4: ')))
        for j in range (0,10):
            img[eix[3]][j] = [0,0,255]
        
        cv2.imshow('Linies orientatives', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        conf = input('Indica amb si o no (s/n) si les linies a la següent imatge estan ben posades:')
    
    print("\nLinies inicials confirmades\n")
    #Ara tenim els eixos, demanem a la funció master q ens ho calculi
    
    
    
    v1,v2,v3,v4 = main(cor[x],eix[3],eix[2],eix[1],eix[0])
    
    #x = detcontraccion(electro[x])  NO FUNCIONA(és per fer el calcul de les distancies)
    
    for i in range(1,len(x)):
        
        if not (v1[x[i]] == None or v2[x[i]] == None or v3[x[i]] == None or v4[x[i]] == None):  
            if (x[0] == 0): #Sistole
                sis1 += v4[x[i]] - v3[x[i]]
                sis2 += v3[x[i]] - v2[x[i]]
                sis3 += v2[x[i]] - v1[x[i]]
            
                totsis += 1
                x[0] = 1
            else:
                dias1 += v4[x[i]] - v3[x[i]]
                dias2 += v3[x[i]] - v2[x[i]]
                dias3 += v2[x[i]] - v1[x[i]]
            
                totdias += 1
                x[1] = 1
        
    dias1 /= totdias
    dias2 /= totdias
    dias3 /= totdias

    sis1 /= totsis
    sis2 /= totsis
    sis3 /= totsis

    print("En pixels dias1 - dias3 i sis1 - sis3: ",dias1,dias2,dias3,sis1,sis2,sis3)

print("Introdueix la distància que hi ha horitzontalment, és a dir des de a d'alt fins abaix per tal de poder fer els calculs")



