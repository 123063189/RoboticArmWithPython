'''
TPJ655
Robotic Arm with Wireless Control
Server Code
'''
import RPi.GPIO as GPIO
import time
import threading
import json
from flask import Flask,jsonify, render_template, request

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
pwmBase=GPIO.PWM(17, 100)
GPIO.setup(27, GPIO.OUT)
pwmUpdown=GPIO.PWM(27, 100)
GPIO.setup(22, GPIO.OUT)
pwmForbackward=GPIO.PWM(22, 100)
GPIO.setup(24, GPIO.OUT)
pwmGripper=GPIO.PWM(24, 100)
baseAngle ='90'
updownAngle ='90'
forbackwardAngle ='60'
gripperAngle ='40'
speed = '5'
dutyBase = float(baseAngle) / 10.0 + 2.5
dutyUpdown = float(updownAngle) / 10.0 + 2.5
dutyForbackward = float(forbackwardAngle) / 10.0 + 2.5
dutyGripper = float(gripperAngle) / 10.0 + 2.5
data = ''

print('Web server started...')

app = Flask(__name__)

autoWork = False

@app.before_first_request
def autowork_thread():
    def run():
        global pwmBase
        global pwmUpdown
        global pwmForbackward
        global pwmGripper
        global speed
        global autoWork
        global data
        global baseAngle
        global updownAngle
        global forbackwardAngle
        global gripperAngle
        i = 0
        while True:
            i=i+1
            print("keep going"+str(i))
            time.sleep(0.5)
            while autoWork:
                i=i+1
                # Start points position
                if autoWork:
                    duty = float(data["baseAngle_s"]) / 10.0 + 2.5
                    pwmBase.ChangeDutyCycle(duty)
                    print("Base angle change...done")
                    baseAngle = data["baseAngle_s"]
                    time.sleep(float(data["delay"]))
                else:
                    break
                if autoWork:
                    duty = float(data["updownAngle_s"]) / 10.0 + 2.5
                    pwmUpdown.ChangeDutyCycle(duty)
                    print("Up&down angle change...done")
                    updownAngle = data["updownAngle_s"]
                    time.sleep(float(data["delay"]))
                else:
                    break
                if autoWork:
                    duty = float(data["forbackwardAngle_s"]) / 10.0 + 2.5
                    pwmForbackward.ChangeDutyCycle(duty)
                    print("forward&backward angle change...done")
                    forbackwardAngle = data["forbackwardAngle_s"]
                    time.sleep(float(data["delay"]))
                else:
                    break
                if autoWork:
                    duty = float(data["gripperAngle_s"]) / 10.0 + 2.5
                    pwmGripper.ChangeDutyCycle(duty)
                    print("gripper Angle angle change...done")
                    gripperAngle = data["gripperAngle_s"]
                    time.sleep(float(data["delay"]))
                else:
                    break
                #back to orginal position
                if autoWork:
                    duty = float(90 / 10.0 + 2.5)
                    pwmUpdown.ChangeDutyCycle(duty)
                    print("Up&down angle change...done")
                    forbackwardAngle = 90
                    time.sleep(float(data["delay"]))
                
                else:
                    break
                # End points positions
                if autoWork:
                    duty = float(data["baseAngle_e"]) / 10.0 + 2.5
                    pwmBase.ChangeDutyCycle(duty)
                    print("Base angle change...done")
                    baseAngle = data["baseAngle_e"]
                    time.sleep(float(data["delay"]))
                else:
                    break
                if autoWork:
                    duty = float(data["updownAngle_e"]) / 10.0 + 2.5
                    pwmUpdown.ChangeDutyCycle(duty)
                    print("Up&down angle change...done")
                    updownAngle = data["updownAngle_e"]
                    time.sleep(float(data["delay"]))
                else:
                    break
                if autoWork:
                    duty = float(data["forbackwardAngle_e"]) / 10.0 + 2.5
                    pwmForbackward.ChangeDutyCycle(duty)
                    print("forward&backward angle change...done")
                    forbackwardAngle = data["forbackwardAngle_e"]
                    time.sleep(float(data["delay"]))
                else:
                    break
                if autoWork:
                    duty = float(data["gripperAngle_e"]) / 10.0 + 2.5
                    pwmGripper.ChangeDutyCycle(duty)
                    print("gripper Angle angle change...done")
                    gripperAngle = data["gripperAngle_e"]
                    time.sleep(float(data["delay"]))
                #back to orginal position
                else:
                    break
                if autoWork:
                    duty = float(90 / 10.0 + 2.5)
                    pwmUpdown.ChangeDutyCycle(duty)
                    print("Up&down angle change...done")
                    updownAngle = 90
                    time.sleep(float(data["delay"]))
                else:
                    break
                print('autoWorking round'+str(i))
            
    thread = threading.Thread(target=run)
    thread.start()
    
@app.route("/")
def main():
    global pwmBase
    global pwmUpdown
    global pwmForbackward
    global pwmGripper
    global baseAngle
    global updownAngle
    global forbackwardAngle
    global gripperAngle
    global dutyBase
    global dutyUpdown
    global dutyForbackward
    global dutyGripper
    pwmBase.start(0)
    pwmUpdown.start(0)
    pwmForbackward.start(0)
    pwmGripper.start(0)
    pwmBase.ChangeDutyCycle(dutyBase)
    pwmUpdown.ChangeDutyCycle(dutyUpdown)
    pwmForbackward.ChangeDutyCycle(dutyForbackward)   
    pwmGripper.ChangeDutyCycle(dutyGripper) 
    
    templateData = {
        'baseAngle' : baseAngle,       #initial angle for gripper
        'updownAngle' : updownAngle, #initial angle for gripper
        'forbackwardAngle' : forbackwardAngle, #initial angle for gripper
        'gripperAngle' : gripperAngle  #initial angle for gripper
    }
    
    return render_template('main.html',**templateData)

@app.route("/<dir>/<status>/<c_speed>")
def driveMotor(dir,status,c_speed):
    dir = dir
    status = status
    global speed
    global baseAngle
    global updownAngle
    global forbackwardAngle
    global gripperAngle
    global pwmBase
    global pwmUpdown
    global pwmForbackward
    global pwmGripper
    global dutyBase
    global dutyUpdown
    global dutyForbackward
    global dutyGripper
    speed = c_speed
    
    if dir == "up" and status == "start":
        if 0 <= float(updownAngle) <= 180:
            updownAngle = str(float(updownAngle) - float(speed))
            duty = float(updownAngle) / 10.0 + 2.5
            pwmUpdown.ChangeDutyCycle(duty)
        if float(updownAngle) < 0:
            updownAngle = 0
            duty = float(updownAngle) / 10.0 + 2.5
            pwmUpdown.ChangeDutyCycle(duty)
        
    if dir == "down" and status == "start":
        if 0 <= float(updownAngle) <= 180:
            updownAngle = str(float(updownAngle) + float(speed))
            duty = float(updownAngle) / 10.0 + 2.5
            pwmUpdown.ChangeDutyCycle(duty)
        if float(updownAngle) > 180:
            updownAngle = 180
            duty = float(updownAngle) / 10.0 + 2.5
            pwmUpdown.ChangeDutyCycle(duty)
        
    if dir == "left" and status == "start":
        if 0 <= float(baseAngle) <= 180:
            baseAngle = str(float(baseAngle) + float(speed))
            duty = float(baseAngle) / 10.0 + 2.5
            pwmBase.ChangeDutyCycle(duty)
        if float(baseAngle) > 180:
            baseAngle = 180
            duty = float(baseAngle) / 10.0 + 2.5
            pwmBase.ChangeDutyCycle(duty)
        
    if dir == "right" and status == "start":
        if 0 <= float(baseAngle) <= 180:
            baseAngle = str(float(baseAngle) - float(speed))
            duty = float(baseAngle) / 10.0 + 2.5
            pwmBase.ChangeDutyCycle(duty)
        if float(baseAngle) < 0:
            baseAngle = 0
            duty = float(baseAngle) / 10.0 + 2.5
            pwmBase.ChangeDutyCycle(duty)
        
    if dir == "forward" and status == "start":
        if 0 <= float(forbackwardAngle) <= 180:
            forbackwardAngle = str(float(forbackwardAngle) + float(speed))
            duty = float(forbackwardAngle) / 10.0 + 2.5
            pwmForbackward.ChangeDutyCycle(duty)  
        if float(forbackwardAngle) > 180:
            forbackwardAngle = 180
            duty = float(forbackwardAngle) / 10.0 + 2.5
            pwmForbackward.ChangeDutyCycle(duty)  
          
    if dir == "backward" and status == "start":
        if 0 <= float(forbackwardAngle) <= 180:
            forbackwardAngle = str(float(forbackwardAngle) - float(speed))
            duty = float(forbackwardAngle) / 10.0 + 2.5
            pwmForbackward.ChangeDutyCycle(duty)
        if float(forbackwardAngle) < 0:
            forbackwardAngle = 0
            duty = float(forbackwardAngle) / 10.0 + 2.5
            pwmForbackward.ChangeDutyCycle(duty)
        
    if dir == "gripper" and status == "pickup":
        gripperAngle = 90
        duty = float(gripperAngle) / 10.0 + 2.5
        pwmGripper.ChangeDutyCycle(duty)
    
    if dir == "gripper" and status == "drop":
        gripperAngle = 40
        duty = float(gripperAngle) / 10.0 + 2.5
        pwmGripper.ChangeDutyCycle(duty)   
        
    return render_template('main.html')


@app.route("/get/<c_angle>")
def getangle(c_angle):
    angle=c_angle
    global baseAngle
    global updownAngle
    global forbackwardAngle
    global gripperAngle
    
    if angle == "baseAngle":
        return str(baseAngle)
    if angle == "updownAngle":
        return str(updownAngle)
    if angle == "forbackwardAngle":
        return str(forbackwardAngle)
    if angle == "gripperAngle":
        return str(gripperAngle)

@app.route("/autowork", methods=['POST'])
def prog():
    global autoWork
    global data
    data = json.loads(request.get_data())
    print(data)
    baseAngle_s = data["baseAngle_s"]
    updownAngle_s = data["updownAngle_s"]
    forbackwardAngle_s = data["forbackwardAngle_s"]
    gripperAngle_s = data["gripperAngle_s"]
    baseAngle_e = data["baseAngle_e"]
    updownAngle_e = data["updownAngle_e"]
    forbackwardAngle_e = data["forbackwardAngle_e"]
    gripperAngle_e = data["gripperAngle_e"]
    delay = data["delay"]
    if str(data["autostatus"]) == '1':
        print("=============1")
        autoWork = True
    else:
        print("=============0")
        autoWork = False
        
    return jsonify(data)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)