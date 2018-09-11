import urllib.request
import cv2
import numpy as np
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
port = 1234
address = (ip,port)
server.bind(address)
server.listen(1)
print('Started listening to ',ip,':',port)
client,addr = server.accept()
print('Got connection from',addr[0],':',addr[1])

kp=0.5
ki=0
kd=0
integrate=0
last_error=0

def motion_x(spd,area):
    if(area<800):
        n=0
        msg = str(spd)+ str(n)+ "\r"
    elif(area>1000):
        n=1
        msg = str(spd)+ str(n)+ "\r"
    else:
        n=2
        msg = str(spd)+ str(n)+ "\r"
    msg_b=msg.encode()
    if(not client.send(msg_b)):
        return
    
url='http://192.168.43.1:8080/shot.jpg'

while(True):
    RawImg=urllib.request.urlopen(url) 
    imgNP=np.array(bytearray(RawImg.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNP,-1)
    
    img=cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
    blur_img = cv2.GaussianBlur(img, (5, 5), 0)
    
    lower_blue = np.array([0,50,130])
    upper_blue = np.array([50,130,255])
    hsv_img = cv2.inRange(blur_img, lower_blue, upper_blue)
    kernel = np.ones((7,7), np.uint8)
    kernel2 = np.ones((9,9), np.uint8)
    

    hsv_img = cv2.dilate(hsv_img, kernel2, iterations=1)
    hsv_img = cv2.erode(hsv_img, kernel, iterations=1)

    height, width = img.shape[:2]

    mid_h = int(height/2)
    cY=mid_h
    mid_w = int(width/2)
    cX=mid_w
    
    cv2.line(img,(0,mid_h),(width,mid_h),(255,0,0),3)
    cv2.line(img,(mid_w,(mid_h+20)),(mid_w,(mid_h-20)),(255,0,0),3)

    _, contours, _ = cv2.findContours(hsv_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    m = 0

    if(len(contours)>0):
        for cnt in contours:
            # calculate moments of binary image
            if m<len(cnt):
                m = len(cnt)
                con = cnt
        M = cv2.moments(con)
 
        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
 
        # put text and highlight the center
        cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


        area=int(M["m00"])
        print(area)
        error=cX-mid_w
        integrate=integrate+error
        if(integrate>=1000):
            integrate=1000
        elif(integrate<=-1000):
            integrate=-1000
        derivative=error-last_error
        last_error=error
        spd=int(kp*error+ki*integrate+kd*derivative)
        #calling function
        motion_x(spd,area)

        cv2.line(img,(cX,mid_h+4),(mid_w,mid_h+4),(255,255,0),2)
        cv2.line(img,(mid_w+4,mid_h+4),(cX,cY),(0,255,0),4)
        
    else:
        print('no')
    cv2.imshow('IMAGE',img)       
    
    k = cv2.waitKey(3) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
exit(0)
