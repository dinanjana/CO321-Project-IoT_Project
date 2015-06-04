import cv2
#import pyaudio
import wave 
import smtplib
import thread
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import serial

def sensorRead() :

  ser = serial.Serial('/dev/ttyACM0',9600)

  while 1 :
      subject = ser.readline()
      body = ser.readline()
      smtpUser = 'dinanjanagunaratne@gmail.com'
      smtpPass = 'dinanatz<3'

    #subject = 'Intruder Alert!'
      toAdd = 'dinanjanagunaratne@gmail.com'
      fromAdd = smtpUser
      header = 'To:' + toAdd + '\n' + 'From:' + fromAdd + '\n' + 'Subject:' + subject
    #body = 'Intruder Alert '

      s = smtplib.SMTP('smtp.gmail.com',587)
      s.ehlo()
      s.starttls()
      s.ehlo()

      s.login(smtpUser,smtpPass)
      s.sendmail(fromAdd,toAdd,header +'\n' + body)
      s.quit()


def upload(index):
  
  gauth = GoogleAuth()

  gauth.LoadCredentialsFile('mycreds.txt')

  if gauth.credentials is None:

    gauth.LocalWebserverAuth()

  elif gauth.access_token_expired:

    gauth.Refresh()

  else:

    gauth.Authorize()
    

  #gauth.LocalWebserverAuth()

  gauth.SaveCredentialsFile('mycreds.txt')
  
  drive = GoogleDrive(gauth)

  file1 = drive.CreateFile()
  file1.SetContentFile('pics/pic'+str(index)+'.jpg')
  file1.Upload()

  print '%s %s' % (file1['title'],file1['mimeType'])




def diffImg(t0, t1, t2):

  d1 = cv2.absdiff(t2, t1)

  d2 = cv2.absdiff(t1, t0)

  return cv2.bitwise_and(d1, d2)

def alertUser():

  smtpUser = 'dinanjanagunaratne@gmail.com'
  smtpPass = 'dinanatz<3'

  subject = 'Intruder Alert!'
  toAdd = 'dinanjanagunaratne@gmail.com'
  fromAdd = smtpUser
  header = 'To:' + toAdd + '\n' + 'From:' + fromAdd + '\n' + 'Subject:' + subject
  body = 'Intruder Alert '

  s = smtplib.SMTP('smtp.gmail.com',587)
  s.ehlo()
  s.starttls()
  s.ehlo()

  s.login(smtpUser,smtpPass)
  s.sendmail(fromAdd,toAdd,header +'\n' + body)
  s.quit()


  toAdd = '765331132@sms.mobitel.lk'
  s = smtplib.SMTP('smtp.gmail.com',587)
  s.ehlo()
  s.starttls()
  s.ehlo()

  s.login(smtpUser,smtpPass)
  s.sendmail(fromAdd,toAdd,header +'\n' + body)
  s.quit()

  
  return

#face detection

def facedetect(img,index):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2,
                                     minSize=(80, 80),
                                     flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(faces) == 0:
        
        False
    else:

        #siren()
        
        for f in faces:
            cv2.imshow("camera", img)
	    index = index + 1
            cv2.imwrite("pics/pic"+str(index)+".jpg", img)
            try:
              if((index - 1)%10 == 0):
                thread.start_new_thread(alertUser,())
                thread.start_new_thread(upload,(index,))
            except:
              print "Error"
              

            print f

            
            
        return True


#siren

#def siren():
  #define stream chunk   
  #chunk = 1024  

  #open a wav format music  
  #f = wave.open('siren.wav','rb')  
  #instantiate PyAudio  
  #p = pyaudio.PyAudio()  
  #open stream  
  #stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
  #              channels = f.getnchannels(),  
  #              rate = f.getframerate(),  
  #             output = True)   #read data  
  #data = f.readframes(chunk)  

  #paly stream  
  #while data != '':  
  #    stream.write(data)  
  #    data = f.readframes(chunk)  

  #stop stream  
  #stream.stop_stream()  
  #stream.close()  

  #close PyAudio  
  #p.terminate()

  #return

try:
  thread.start_new_thread(sensorRead,())
except:
  print "Sensor Error"

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

chunk = 1024

cam = cv2.VideoCapture(0)
#cam.set(3,320)
#cam.set(4,240)

winName = "Movement Indicator"
winName2 = "Surveillance Camera"

#cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
#cv2.namedWindow(winName2, cv2.CV_WINDOW_AUTOSIZE)

 

# Read three images first:


t_minus = cam.read()[1]

t = cam.read()[1]

t_plus = cam.read()[1]

s,img = cam.read()

index = 0  

while True:

  #cv2.imshow( winName, diffImg(t_minus, t, t_plus) )  
  s,img = cam.read()
  #cv2.imshow( winName2 ,img)
  
  if facedetect(img,index):
     index = index + 1

  # Read next image

  t_minus = t

  t = t_plus

  t_plus = cam.read()[1]
  
  key = cv2.waitKey(100)
  

  if key == 27:

    #cv2.destroyWindow(winName)

    break

 

print "Goodbye"
