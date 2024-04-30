import numpy as np
import cv2
import pytesseract
import os

per = 25
roi = [[(176, 150), (271, 171), 'text', 'Registration Number'],[(517, 150), (590, 170), 'text', 'Registration Date'],[(177, 195), (237, 211), 'text', 'Fuel Type']]


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

imgQ = cv2.imread('image2.jpg')
h,w,c = imgQ.shape
# imgQ = cv2.resize(imgQ,(w//3,h//3))

orb = cv2.ORB_create(1000)
kp1, des1 = orb.detectAndCompute(imgQ,None)
# imgKp1 = cv2.drawKeypoints(imgQ,kp1,None)

path = 'registration'
myPicList = os.listdir(path)
for j,y in enumerate(myPicList):
    img = cv2.imread(path +"/"+y)
    # cv2.imshow(y,img)
    kp2, des2 = orb.detectAndCompute(img,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.match(des2,des1)
    list(matches).sort(key= lambda x: x.distance)
    good = matches[:int(len(matches)*(per/100))]
    imgMatch = cv2.drawMatches(img,kp2,imgQ,kp1,good[:200],None,flags=2)
    # imgMatch = cv2.resize(imgMatch, (w//2, h//2))
    # cv2.imshow(y, imgMatch)

    srcPoints = np.float32([kp2[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dstPoints = np.float32([kp1[m.trainIdx].pt for m in good]).reshape(-1,1,2)

    M, _ =cv2.findHomography(srcPoints,dstPoints,cv2.RANSAC,5.0)
    imgScan = cv2.warpPerspective(img,M,(w,h))
    # cv2.imshow(y, imgScan)

    imgShow = imgScan.copy()
    imgMask = np.zeros_like(imgShow)

    myData = []

    for x,r in enumerate(roi):
        cv2.rectangle(imgMask, ((r[0][0]),(r[0][1])),((r[1][0]),(r[1][1])),(0,0,255),cv2.FILLED)
        imgShow = cv2.addWeighted(imgShow,0.99,imgMask,0.3,0)

        imgCrop = imgScan[r[0][1]:r[1][1], r[0][0]:r[1][0]]
        # cv2.imshow(str(x), imgCrop)

        if r[2] == 'text':
            # print(f'{r[3]}: {pytesseract.image_to_string(imgCrop)}')
            myData.append(pytesseract.image_to_string(imgCrop))
    # cv2.imshow(y, imgShow)

with open('DataVerificationPUC.csv','a+') as f:
    for data in myData:
        f.write((str(data)+','))
    f.write('\n')


# cv2.imshow("KeyPointsQuery",imgKp1)
cv2.imshow("Output",imgQ)
cv2.waitKey(0)


