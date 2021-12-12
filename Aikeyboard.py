from time import sleep
import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput import keyboard
from pynput.keyboard import Controller
import cvzone
cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3,1080)
cap.set(4,620)
detetor=HandDetector(detectionCon=0.8)
keys=[["Q","W","E","R","T","Y","U","I","O","P"],
     ["A","S","D","F","G","H","J","K","L",";"],
     ["Z","X","C","V","B","N","M",",",".","/"]]
finalText=''     
keyboard=Controller()
def drawAll(img,buttonlist):
    for button in buttonlist:
        x,y=button.pos
        w,h=button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1],
                                                   button.size[0],button.size[0]), 20 ,rt=0)
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x+10,y+50),
                    cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),4)
    return img
class Button():
    def __init__(self,pos,text,size=[60,65]):
        self.pos=pos
        self.size=size
        self.text=text
 
buttonlist=[]
for i in range(len(keys)):
        for j,key in enumerate(keys[i]):
            buttonlist.append(Button([80*j+30,70*i+50],key))

while True:
    success,img=cap.read()
    img = cv2.flip(img, 1)
    img= detetor.findHands(img)
    lmList,bboxInfo=detetor.findPosition(img)
    img=drawAll(img,buttonlist)
    if lmList:
        for button in buttonlist:
            x,y=button.pos
            w,h=button.size
            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                cv2.putText(img,button.text,(x+10,y+50),
                    cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),4)
                l, _ ,_ = detetor.findDistance(8,12,img,draw=False)
                # print(l)    
                if l<30:
                    keyboard.press(button.text)
                    cv2.rectangle(img,button.pos,(x+w,y+h),(175,0,175),cv2.FILLED)
                    cv2.putText(img,button.text,(x+10,y+50),
                    cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),4)
                    finalText+=button.text
                    sleep(0.15)
                   
    cv2.rectangle(img,(30,320),(700,450),(175,0,175),cv2.FILLED)
    cv2.putText(img,finalText,(60,425),
                cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)                

    cv2.imshow("Virtual-KeyBoard",img)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break