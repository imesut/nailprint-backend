import cv2
import mediapipe as mp
from matplotlib import pyplot as plt
import numpy as np
from cvutils import extractPage, resize, showImg, approximation
from scipy.optimize import curve_fit
from stlcreator import *
import os
import shutil
import base64

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


def processHandPhoto(img):
    img = cv2.imread(img)
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # newImg = extractPage(imageRGB)
    # showImg(img)
    # showImg(newImg)

    results = hands.process(imageRGB)

    imgGRY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgGryBlur = cv2.medianBlur(imgGRY, 5)

    fingerCount = 0
    FOLDERNAME = img + "-stl"
    ARCHIVEFILE = ""
    
    os.mkdir(FOLDERNAME)
    
    # if results.multi_hand_landmarks:
    #     for handLms in results.multi_hand_landmarks: # working with each hand
    #         for id, lm in enumerate(handLms.landmark):
    #             h, w, c = img.shape
    #             cx, cy = int(lm.x * w), int(lm.y * h)
    #             if id == 20 or id == 16 or id == 12 or id == 8 or id == 4:
    #                 width = img.shape[0]
    #                 # 60: width of the page
    #                 fW = width / 60 * 3
                    
    #                 area = [(int(cx - fW), int(cy - fW)),
    #                         (int(cx + fW), int(cy + fW))]
                    
    #                 # cv2.circle(img, (cx, cy), int(fW), (255, 0, 255), 4)
                    
    #                 nailImg = imgGRY[area[0][1]:area[1][1],
    #                             area[0][0]:area[1][0]]
                    
    #                 nailCentralPnt = imgGRY[cx, cy]
    #                 # print(nailCentralPnt)
    #                 threshold = nailCentralPnt - 25
                    
    #                 # Some threshold trials
    #                 # t, nailPrcsd = cv2.threshold(nailImg, threshold, 255, cv2.THRESH_TOZERO)
    #                 # t, nailPrcsd = cv2.threshold(nailImg, threshold, 255, cv2.THRESH_TOZERO)
    #                 nailPrcsd = cv2.adaptiveThreshold(nailImg, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 7)
    #                 nailPrcsd = cv2.Canny(nailPrcsd, 10, 200)
    #                 nailPrcsd = cv2.bilateralFilter(nailPrcsd,13,25,25)                
                    
    #                 contours, hierarchy = cv2.findContours(nailPrcsd, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #                 for contour in contours:
    #                     perimeter = cv2.arcLength(contour, True)
    #                     approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
    #                     # if len(approx) > 2:
    #                         # print(approx)    
    #                 # showImg(nailPrcsd)
                    
    #                 yLen = len(nailPrcsd)
    #                 xLen = len(nailPrcsd[0])
    #                 bottomCurve = nailPrcsd[int(yLen/2):yLen, int(xLen/3):int(2*xLen/3)]
    #                 # showImg(bottomCurve)
                    
    #                 yLen = len(bottomCurve)
    #                 xLen = len(bottomCurve[0])
    #                 yvals = []
    #                 xvals = []
    #                 # print("xlen", xLen, "ylen", yLen)
                    
    #                 for y in range(yLen):
    #                     line = bottomCurve[y]
    #                     for x in range(xLen):
    #                         if line[x] > 0:
    #                             xvals.append(x)
    #                             yvals.append(yLen - y)
                                    
    #                 # print(xvals)
    #                 # print(yvals)
                    
    #                 params, cov = curve_fit(approximation, xvals, yvals)
    #                 filename = FOLDERNAME + "/" + fingerCount + ".stl"
    #                 generateCustomizedSTLforFinger(filename, params[0], params[1], params[2])
                                        
    #                 # print(params)
    #                 # print(cov)
                    
    #                 print("finger:", fingerCount, params)
                    
    #                 #visual marking                    
    #                 # cv2.rectangle(img, area[0], area[1], (255,0,0), 2)
    #                 fingerCount += 1
    #                 # cv2.imshow("finger", nailImg)
    #                 # cv2.waitKey(0)
                    
    #         mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    #         shutil.make_archive(FOLDERNAME, 'zip', FOLDERNAME)
            
    #         with open(FOLDERNAME+".zip", "r") as zipFile:
    #             ARCHIVEFILE = base64.b64encode(zipFile.read())
    
    message = ""
    if fingerCount > 0:
        message = "No finger can be identified successfully. You may try to take photo with different lightning conditions."
    else:
        message = "We identified " + fingerCount + " fingers. You can download this archive file for 3D-printable templates. For other fingers you may try to take another photo."
    
    return { "fingerCount": fingerCount, "message": message, "stlArchive": ARCHIVEFILE }
