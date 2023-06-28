import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
from time import sleep


cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)


detector = HandDetector(detectionCon=0.8)



def drawAll(img,buttonlist):
        
    for button in buttonlist:

        x,y = button.pos
        w,h = button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255))
        cv2.putText(img,button.text,(x+25,y+75),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)

    return img




class Button():
    def __init__(self,pos,text,size=(100,100)):
        self.pos = pos
        self.text = text
        self.size = size





        
keyboard = Controller()
buttonlist = []
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText = ""

a = 150
for i in range(len(keys)):
    b = 100
    for x,key in enumerate(keys[i]):

        buttonlist.append(Button([100*x+50,a],key))
    a+=100


while True:
    success,img = cap.read()
    hands = detector.findHands(img,draw=False) 
    img = detector.findHands(img)
    drawAll(img[1],buttonlist)

    #hands, img_new = detector.findHands(img[1])  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        
        lmList1 = hand1["lmList"]  # List of 21 Landmark points

        for button in buttonlist:
            x,y = button.pos
            w,h = button.size

            if (x<lmList1[8][0]<x+w) and y<lmList1[8][1]<y+h:
                cv2.rectangle(img[1],button.pos,(x+w,y+h),(175,0,175))
                cv2.putText(img[1],button.text,(x+25,y+75),cv2.FONT_HERSHEY_PLAIN,5,(0,0,255),5)

                l,_= detector.findDistance(lmList1[8][:2],lmList1[12][:2])
                print(l)

                ## when clicked
                if l < 45:
                    keyboard.press(button.text)
                    cv2.rectangle(img[1], button.pos, (x + w, y + h), (0, 255, 0))
                    cv2.putText(img[1], button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.25)

    cv2.rectangle(img[1], (50, 550), (700, 650), (175, 0, 175))
    cv2.putText(img[1], finalText, (60, 630),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)







    cv2.imshow("Image",img[1])
    cv2.waitKey(1)