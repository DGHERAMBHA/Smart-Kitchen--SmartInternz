import time
import sys
import ibmiotf.application
import ibmiotf.device
import requests
url = "https://www.fast2sms.com/dev/bulk"


organisation="qpqk20"
deviceType="raspberrypi"
deviceId="123456"
authMethod="token"
authToken="12345678"

def myCommandCallback(cmd):
    print("Command received : %s !" % cmd.data)

try:
    deviceOptions={"org":organisation,"type":deviceType,"id": deviceId,"auth-method":authMethod,"auth-token":authToken}
    deviceCli=ibmiotf.device.Client(deviceOptions)
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit()
    
deviceCli.connect()

jar_weight=2000
cylinder_weight=15
fans="OFF"
leak="OFF"
leakage=0



cylinder_empty=0;
jar_empty=0

while True:
    cylinder_weight=cylinder_weight-0.05
    jar_weight=jar_weight-15

    if (cylinder_weight>0 and cylinder_weight<=5):
        status="LOW"
        time.sleep(0.2)
    elif(cylinder_weight>5 and cylinder_weight<=10):
        status="MODERATE"
    elif (cylinder_weight>10 and cylinder_weight<=15):
        status="HIGH"

    else:
        cylinder_weight=0
        status="EMPTY!!"

        if (cylinder_empty==0):
            payload= "sender_id=FSTSMS&message=Cylinder is empty. Book a new one immediately&language=english&route=p&numbers=8130383672"
            headers={"authorization" : "jskXG7URxi8oIeWLKD9nYVNMaHCtmgZqvfdr4JO2lbE6zTS5pAFv93mURQGb2tWV8gkTdAl4osLpOXIC"}
            response=requests.request("POST",url,data=payload,headers=headers)
            print(response.text)
            print("the cylinder is empty")
            cylinder_empty=1;


    if(jar_weight<300 and jar_weight>=0):
        jar_status="LOW"
        time.sleep(0.2)
    elif (jar_weight>=300 and jar_weight<1100):
        jar_status="MODERATE"
    elif (jar_weight>=1100 and jar_weight<=2000):
        jar_status="HIGH"
    else:
        jar_weight=0
        jar_status="EMPTY!!"
        if (jar_empty==0):
            print("The jar is empty!!")
            payload="sender_id=FSTSMS&message=Jar is empty. Buy the essential soon&language=english&route=p&numbers=8130383672"

            headers={"authorization" : "jskXG7URxi8oIeWLKD9nYVNMaHCtmgZqvfdr4JO2lbE6zTS5pAFv93mURQGb2tWV8gkTdAl4osLpOXIC"}

            response=requests.request("POST",url,data=payload,headers=headers)
            print(response.text)
            jar_empty=1;


    leakage=leakage+1
    if(leakage==50):
        print(" ALERT!!! GAS LEAKAGE in your kitchen. ")
        payload="sender_id=FSTSMS&message=There is a GAS LEAKAGE.Check NOW&language=english&route=p&numbers=8130383672"

        headers={"authorization" : "jskXG7URxi8oIeWLKD9nYVNMaHCtmgZqvfdr4JO2lbE6zTS5pAFv93mURQGb2tWV8gkTdAl4osLpOXIC"}

        response=requests.request("POST",url,data=payload,headers=headers)

        print(response.text)

        fans="ON"
        leak="ON"

    data={ 'cylinder_weight' :round(cylinder_weight,2), 'status': status, 'leak': leak, 'jar_weight':jar_weight, 'jar_status':jar_status,'fans':fans, 'leakage':leakage}

    def myOnPublishCallback():
        print("published cylinder_weight=%s" %round(cylinder_weight,2), "cylinder_status=%s" %status , "gas leakage =%s" %leak, "fans=%s" %fans, "leakage status =%s" %leakage )
        
            

    success =deviceCli.publishEvent("Smart Kitchen","json",data,qos=0,on_publish=myOnPublishCallback)

    if not success:
        print("not coonected to IoTF")
        time.sleep(0.5)
        device.ClicommandCallback=myCoammandCallback
        
deviceCli.disconnect()