import cv2
import sys
import time


cascPath = "C:\Users\Evan Williams\Desktop\Webcam-Face-Detect-master\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

facial_areas = []
cont_detections = 0
miss_detections = 0
active1=False
active2=False

while True:
    active1=False
    active2=False
    for area in facial_areas:
        facial_areas.remove(area)
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw rectangles around all faces in frame
    facial_area = int(0)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        ind_facial_area = (x+w)*(y+h)

        # We count only the largest "face" in a frame
        if ind_facial_area > facial_area:
            facial_area = ind_facial_area
    
    # Add result to respective detection category
    if facial_area > 0:
        cont_detections += 1
        facial_areas.append(facial_area)
        
    else:
        miss_detections += 1
        

    # Check if reset needed
    if miss_detections > 2:
        cont_detections = 0
        miss_detections = 0
        facial_areas = []
        
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Determine if face is approaching
    length = len(facial_areas) -1
    if length==0:
        length=length; #do nothing if length is 0
    elif length>0:
        if facial_areas[length]>facial_areas[length-1]:
            print "Area is increasing"
        
    
    if cont_detections > 5:
        i = len(facial_areas)
        if sorted(facial_areas) == facial_areas:
            if active1 == False and active2 == False:
                active1=True
                print "Activated1"
                # Trigger servo for x ms
                # Wait for y ms
                # Trigger servo (reverse) for z ms
                time.sleep(15)
                cont_detections=0
                miss_detections=0
                
            
        elif facial_areas[i-1]>facial_areas[1]:
            if active1 == False and active2 == False:
                active2=True
                print "Activated.2"
                # Trigger servo for x ms
                # Wait for y ms
                # Trigger servo (reverse) for z ms
                time.sleep(15)
                cont_detections=0
                miss_detections=0
                
    time.sleep(.1)
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
