
import cv2
import cvzone
import numpy as np
from Hand_Tracking_Module import Hand_Detector
from pynput.keyboard import Controller, Key
import time
from pynput.mouse import Controller as MouseController


detector=Hand_Detector(maxHands=2,detectionCon=0.8,minTrackCon=0.8)
mouse = MouseController()


cap= cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)

wordlist = [
    'hello','help','here','hey','good','great','game','gamer','python','predict','presentation',
    'virtual','keyboard','test','text','thanks','today','time','typing','track'
]


Keys=[['Q','W','E','R','T','Y','U','I','O','P','<'],
      ['A','S','D','F','G','H','J','K','L',',',' '],
      ['Z','X','C','V','B','N','M','.','?','!','_']]

TipId=[4,8,12,16,20]

keyboard = Controller()


class Button():
    def __init__(self,posi,text,size=(80,80)):
        self.posi=posi
        self.text=text
        self.size=size
        
    #def draw(self,img):
        

        #return img

'''mybutton0=Button((20,20),'Q')
mybutton1=Button((20+50,20),'W')
mybutton2=Button((20+50+50,20),'E')
'''
def get_suggestions(FinalTxt, max_sugs=3):
    if not FinalTxt or FinalTxt.endswith(' '):
        return []
    prefix = FinalTxt.split()[-1]
    suggestions = [w for w in wordlist if w.startswith(prefix.lower())]
    return suggestions[:max_sugs]

def DrawAll(img, buttonlist,FinalTxt=''):
    '''for button in buttonlist:
        x,y= button.posi
        w,h=button.size
        cv2.rectangle(img, button.posi, (x+w, y+h), (153,255,153), cv2.FILLED )
        cv2.putText(img, button.text, (x+9, y+30), cv2.FONT_HERSHEY_PLAIN, 2, (51,51,51), 2)

    return img'''

    newimg= np.zeros_like(img, np.uint8)
    sug_start_x = 40
    sug_y = 60
    for i, sug in enumerate(suggestionList):
        x = sug_start_x + i*160
        y = sug_y
        w, h = 150, 40
        cv2.rectangle(newimg, (x,y), (x+w,y+h), (255,255,0), cv2.FILLED)
        cv2.putText(newimg, sug, (x+10, y+28), cv2.FONT_HERSHEY_PLAIN, 2, (51,51,51), 2)

    for button in buttonlist:
        x,y=button.posi
        w,h=button.size

        cvzone.cornerRect(img,(button.posi[0],button.posi[1],button.size[0],button.size[1]),12,2,rt=0,colorC=(255,255,0))
        cv2.rectangle(newimg, button.posi, (x+w, y+h), (255,0,0), cv2.FILLED )#153,255,153
        text_size = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 2, 2)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(newimg, button.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (51, 51, 51), 2)


        output_bar_x = KyXp
        output_bar_y = 500
        output_bar_width = 880
        output_bar_height = 50

        cvzone.cornerRect(img, (output_bar_x - 2, output_bar_y - 10, output_bar_width, output_bar_height), 10, 2, rt=0, colorC=(200, 200, 200))
        cv2.rectangle(newimg, (output_bar_x, output_bar_y), (output_bar_x + output_bar_width, output_bar_y + output_bar_height), (205, 205, 205), cv2.FILLED)
        safe_text = FinalTxt.encode('ascii', 'ignore').decode() if FinalTxt else ''
        cv2.putText(newimg, safe_text, (output_bar_x + 10, output_bar_y + 35), cv2.FONT_HERSHEY_PLAIN, 3, (51, 51, 51), 3)



        #cv2.rectangle(newimg, (200,230), (690, 17), (50,50,50), cv2.FILLED )

    out = img.copy()
    alpha = 0.3
    mask = newimg.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, newimg, 1 - alpha, 0)[mask]
    return out

def Distance3D(lmlist,v1,v2):
    x1,y1,z1=lmlist[v1][0], lmlist[v1][1], lmlist[v1][2]
    x2,y2,z2=lmlist[v2][0], lmlist[v2][1], lmlist[v2][2]
    InRt=((y2-y1)**2)+ ((z2-z1)**2) #((x2-x1)**2) +
    dist=(InRt**(.5))
    
    return (dist//1)


KyXp=50
KyYp = 100  # vertical starting position (you can change this)

prv_mvX,prv_mvY=KyXp,KyYp

button_width = 80
button_height = 80
gap_x = 20   # horizontal spacing between keys
gap_y = 25   # vertical spacing between rows

buttonList = []
for row_idx, row in enumerate(Keys):
    for col_idx, key in enumerate(row):
        x = KyXp + col_idx * (button_width + gap_x)
        y = KyYp + row_idx * (button_height + gap_y)
        buttonList.append(Button((x, y), key, (button_width, button_height)))


prev_lnth1=prev_lnth2=21
prev_bttn1=crnt_bttn1=prev_bttn2=crnt_bttn2=''
FinalTxt=''
Crnt_RectArea1,Prev_RectArea1=0,0.1
Crnt_RectArea2,Prev_RectArea2=0,0.1

def type_and_display(char):
    global FinalTxt
    if char == '<':
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
        FinalTxt = FinalTxt[:-1]
    elif char == ' ':
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        FinalTxt += ' '
    elif char == '_':
        keyboard.press(Key.shift)
        keyboard.press('-')
        keyboard.release('-')
        keyboard.release(Key.shift)
        FinalTxt += '_'
    elif char in {'!', '?'}:
        shift_map = {'!': '1', '?': '/'}
        keyboard.press(Key.shift)
        keyboard.press(shift_map[char])
        keyboard.release(shift_map[char])
        keyboard.release(Key.shift)
        FinalTxt += char
    else:
        keyboard.press(char.lower())
        keyboard.release(char.lower())
        FinalTxt += char


while True:
    success, img = cap.read()
    if not success:
        print("Failed to read from camera.")
        continue
    if not success:
        print("Webcam frame failed!")
        continue


    img=cv2.flip(img,1)
    hands,img= detector.findHands(img, flipType=False)
    #lmlist,boxinfo=detector.findPosition(img)

    suggestionList = get_suggestions(FinalTxt)

    img=DrawAll(img,buttonList,FinalTxt)
    
    if hands:
        #if len(hands) == 1:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)
        if fingers1 == [1, 0, 0, 0, 0]:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            FinalTxt += '\n'  # Optional: to show Enter visually
            print("Thumbs up detected: Enter pressed")
            time.sleep(0.5)  # debounce to prevent spamming

        if fingers1 == [0, 1, 1, 0, 0]:  # Scroll Up
            mouse.scroll(0, 2)
            print("Scroll Up")
            time.sleep(0.3)

        elif fingers1 == [1, 0, 0, 0, 1]:  # Scroll Down
            mouse.scroll(0, -2)
            print("Scroll Down")
            time.sleep(0.3)


        for button in buttonList:
            x,y=button.posi
            w,h=button.size

            FingerCnt1=detector.fingersUp(hand1)


            print('3D_Hand1_P0_X1axis>',lmList1[0][0],'Y1axis>',lmList1[0][1],'Z1axis>',lmList1[0][2])
            ZxsMvmnt1=str(lmList1[0][2])
            
            ZboxRnge1=int(ZxsMvmnt1[-1])

            if ((x< lmList1[8][0] <x+w) and (y< lmList1[8][1] <y+h)) and FingerCnt1[0]==1:
                cv2.rectangle(img, button.posi, (x+w, y+h), (153,255,51), cv2.FILLED )
                cv2.putText(img, button.text, (x+9, y+30), cv2.FONT_HERSHEY_PLAIN, 2, (51,51,51), 2)

                
                
                lnth1=Distance3D(lmList1,8,0)
                
                crnt_bttn1=button.text

                RectHight1=abs( (bbox1[1] - 20) - (bbox1[1] + bbox1[3] + 20) )
                RectWeight1=abs( (bbox1[0] - 20) - (bbox1[0] + bbox1[2] + 20) )
                Crnt_RectArea1= (RectHight1*RectWeight1)//100


                if lnth1<prev_lnth1-3.15 and (prev_bttn1==crnt_bttn1)  and ( Prev_RectArea1-(10-ZboxRnge1)<=(Crnt_RectArea1-ZboxRnge1) ):          #     <=Prev_RectArea1+6
                    print("click")
                    #print('>=>',prev_lnth1,lnth1)
                    
                    cv2.rectangle(img, button.posi, (x+w, y+h), (153,102,255), cv2.FILLED )
                    cv2.putText(img, button.text, (x+9, y+30), cv2.FONT_HERSHEY_PLAIN, 2, (51,51,51), 2)
                    type_and_display(button.text)

                prev_lnth1=lnth1
                
            prev_bttn1=crnt_bttn1
            Prev_RectArea1=Crnt_RectArea1

        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"

            fingers2 = detector.fingersUp(hand2)
            #print('Both>>>>',handType2)
            if fingers2 == [1, 0, 0, 0, 0]:
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                FinalTxt += '\n'
                print("Thumbs up (Hand 2): Enter pressed")
                time.sleep(0.5)

            if fingers2 == [0, 1, 1, 0, 0]:  # Scroll Up
                mouse.scroll(0, 2)
                print("Scroll Up")
                time.sleep(0.3)

            elif fingers2 == [1, 0, 0, 0, 1]:  # Scroll Down
                mouse.scroll(0, -2)
                print("Scroll Down")
                time.sleep(0.3)


            print('3D_Hand2_P0_X2axis>',lmList2[0][0],'Y2axis>',lmList2[0][1],'Z2axis>',lmList2[0][2])
            ZxsMvmnt2=str(lmList2[0][2])
            #print(ZxsMvmnt2[-1])
            ZboxRnge2=int(ZxsMvmnt2[-1])
        
            for button in buttonList:
                x,y=button.posi
                w,h=button.size

                #Zposi8,Zposi0=(lmList1[8][2]), (lmList1[0][2])
                #print('8>>> ',Zposi8, '  0>>> ', Zposi0,'\n','Neg>>> ',(Zposi8-Zposi0))
                #lnth=(Distance3D(lmList1,8,0))
                #print('dist_out>>> ',lnth)

                '''if ((x< lmList1[8][0] <x+w) and (y< lmList1[8][1] <y+h)) :
                    cv2.rectangle(img, button.posi, (x+w, y+h), (153,255,51), cv2.FILLED )
                    cv2.putText(img, button.text, (x+9, y+30), cv2.FONT_HERSHEY_PLAIN, 2, (51,51,51), 2)

                    #print('dist_in>>> ',lnth)

                    #FingerCnt=detector.fingersUp()
                    #print('x>>>',FingerCnt)

                    if FingerCnt[0]==0:
                        print("click")
                        cv2.rectangle(img, button.posi, (x+w, y+h), (153,102,255), cv2.FILLED )
                        cv2.putText(img, button.text, (x+9, y+30), cv2.FONT_HERSHEY_PLAIN, 2, (51,51,51), 2)'''

                if ((x< lmList2[8][0] <x+w) and (y< lmList2[8][1] <y+h)):
                    cv2.rectangle(img, button.posi, (x+w, y+h), (153,255,51), cv2.FILLED )
                    cv2.putText(img, button.text, (x+9, y+30), cv2.FONT_HERSHEY_PLAIN, 2, (51,51,51), 2)


                    lnth2=Distance3D(lmList2,8,0)

                    crnt_bttn2=button.text

                    RectHight2=abs( (bbox2[1] - 20) - (bbox2[1] + bbox2[3] + 20) )
                    RectWeight2=abs( (bbox2[0] - 20) - (bbox2[0] + bbox2[2] + 20) )
                    Crnt_RectArea2= (RectHight2*RectWeight2)//100



                    if lnth2<prev_lnth2-3.15 and (prev_bttn2==crnt_bttn2) and ( Prev_RectArea2-(10-ZboxRnge2)<=(Crnt_RectArea2-ZboxRnge2) ):          #
                        print("click")
                        cv2.rectangle(img, button.posi, (x+w, y+h), (153,102,255), cv2.FILLED )
                        cv2.putText(img, button.text, (x+9, y+30), cv2.FONT_HERSHEY_PLAIN, 2, (51,51,51), 2)
                        type_and_display(button.text)


                    prev_lnth2=lnth2
                prev_bttn2=crnt_bttn2
                Prev_RectArea2=Crnt_RectArea2
        for i, sug in enumerate(suggestionList):
            sx = 40 + i*160; sy = 60; sw, sh = 150, 40
            if (sx < lmList1[8][0] < sx+sw) and (sy < lmList1[8][1] < sy+sh) and fingers1[0]==1:
                current_prefix = FinalTxt.split()[-1]
                FinalTxt = FinalTxt[:-len(current_prefix)] + sug + ' '
                for c in sug + ' ':
                    keyboard.press(c if c!=' ' else Key.space)
                    keyboard.release(c if c!=' ' else Key.space)
                time.sleep(0.3)



    cv2.imshow("Image", img)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
                   break

cap.release()
cv2.destroyAllWindows()