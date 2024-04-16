import asyncio
import base64
import websockets
import time 
import datetime
import json
import cv2

def getFrame(i):
 
	cap = cv2.VideoCapture("video/Очень толстый кот сидит на лавочке.mp4")
	cap.set(cv2.CAP_PROP_POS_FRAMES,i)
	res,frame = cap.read()
	_,buffer = cv2.imencode(".jpg",frame)
	frame = base64.b64encode(buffer)
	frame = str(frame)[2:-1]
	return "data:image/jpeg;base64,"+frame
def sendFrames(i,fps,current_time):
	
	
	t = str(current_time.hour)+":"+str(current_time.minute)+":"+str(current_time.second)
	frameBase64 = getFrame(i)
	r = {}
	if True: #i%50==0:
		r = {"Время":t,"b64":frameBase64,"Номер кадра":i,"Кадров в секунду": fps,"Название файла":"Очень толстый кот сидит на лавочке.mp4"}
	else:
		r = {"Время":t,"Кадр":i,"Кадров в секунду": fps,"Название файла":"Очень толстый кот сидит на лавочке.mp4"}
	jsonn = json.dumps(r) # note i gave it a different name
	
	print(i)
	return jsonn
		

async def send_message():
    uri = "ws://localhost:8080/ws?type=1" 
    
    async with websockets.connect(uri) as websocket:
        second = 0
        frames = 0
        fps = 0
        i=0
        while True:
            i=i+1
            current_time = datetime.datetime.now().time()
            if second == current_time.second:
                frames = frames+1
            else:
                fps = frames
                frames = 0
                second = current_time.second
            message = sendFrames(i,fps,current_time)
            await websocket.send(message)
            await asyncio.sleep(1/250)  # Ожидание 1 секунды перед отправкой следующего сообщения

asyncio.get_event_loop().run_until_complete(send_message())
