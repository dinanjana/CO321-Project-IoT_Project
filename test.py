import cv2
import pyaudio
import wave 

def diffImg(t0, t1, t2):

  d1 = cv2.absdiff(t2, t1)

  d2 = cv2.absdiff(t1, t0)

  return cv2.bitwise_and(d1, d2)


  

#face detection

def facedetect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2,
                                     minSize=(80, 80),
                                     flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(faces) == 0:
        
        return []
    else:

        siren()
        
        for f in faces:
            cv2.imshow("camera", img)
            cv2.imwrite("/Images/pic.jpg", img)
            print f

            
            
        return faces


#siren

def siren():
  #define stream chunk   
  chunk = 1024  

  #open a wav format music  
  f = wave.open('siren.wav','rb')  
  #instantiate PyAudio  
  p = pyaudio.PyAudio()  
  #open stream  
  stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)  
  #read data  
  data = f.readframes(chunk)  

  #paly stream  
  while data != '':  
      stream.write(data)  
      data = f.readframes(chunk)  

  #stop stream  
  stream.stop_stream()  
  stream.close()  

  #close PyAudio  
  p.terminate()

  return



cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

chunk = 1024

cam = cv2.VideoCapture(0)
#cam.set(3,1024)
#cam.set(4,720)

winName = "Movement Indicator"
winName2 = "Surveillance Camera"

cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)
cv2.namedWindow(winName2, cv2.CV_WINDOW_AUTOSIZE)

 

# Read three images first:


t_minus = cam.read()[1]

t = cam.read()[1]

t_plus = cam.read()[1]

s,img = cam.read()
 

while True:

  cv2.imshow( winName, diffImg(t_minus, t, t_plus) )  
  s,img = cam.read()
  cv2.imshow( winName2 ,img)
  facedetect(img)

  # Read next image

  t_minus = t

  t = t_plus

  t_plus = cam.read()[1]
  
  key = cv2.waitKey(100)
  
  if key == 27:

    cv2.destroyWindow(winName)

    break

 

print "Goodbye"
