import cv2
import winsound
from email.message import EmailMessage
import smtplib

Alarm_status=False
mail_status=False

def mail_function():
    owner_gmail="Enter Reciever gmail"
    subject='Suspect Found !'
    body="warning a suspicious person reported in XYZ Atm"
    em=EmailMessage()
    em['subject']=subject
    em.set_content(body)

    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login("Enter Sender gmail",'password')
        server.sendmail("Enter Sender gmail",owner_gmail,em.as_string())
        print('sent to {}'.format(owner_gmail))
    except Exception as e:
        print(e)

eye_cascade=cv2.CascadeClassifier(r"D:\Computer_vision\2nd project\haarcascade_eye.xml")
face_cascade=cv2.CascadeClassifier(r"D:\Computer_vision\2nd project\haarcascade_frontalface_default.xml")

cap=cv2.VideoCapture(0)
found=False
while True:
    suc,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    eyes=eye_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=15)
    faces=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=15)
    if(len(eyes)>0):
        for (x,y,w,h) in eyes:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
    if(len(faces)>0):
        for(p,q,r,s) in faces:
            cv2.rectangle(img,(p,q),(p+r,q+s),(20,180,30),3)
    if(len(faces)<1) & (len(eyes)<1):
            cv2.putText(img,"...............",(15,440),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),3)
            print('.........................')
    if(len(faces)>0) & (len(eyes)>0):
            cv2.putText(img,"Normal",(15,440),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),3)
            print('Normal Person')
    if(len(faces)>0) & (len(eyes)<1):
            cv2.putText(img,"Normal",(15,440),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),3)
    if(len(eyes)>0) & (len(faces)<1):
            found=True
            cv2.putText(img,"Alert !",(15,440),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),3)
            print("suspects found")
            if mail_status==False:
                mail_function()
                mail_status=True
            if Alarm_status==False:
                winsound.PlaySound("alert.wav",winsound.SND_ASYNC)
                Alarm_status=True

    cv2.imshow('image',img)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()