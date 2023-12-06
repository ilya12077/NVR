import datetime
import os
from threading import Thread

import cv2
from flask import Flask, request
from waitress import serve

app = Flask(__name__)
cam2Record = False
cam1Record = False


@app.route('/cam', methods=['GET', 'POST'])
def cam2():
    global cam2Record
    global cam1Record
    action = request.args.get('action')
    camid = int(request.args.get('camid'))  # 1,2
    match action:
        case 'on':
            if not cam2Record and camid == 2:
                print('on cam' + str(camid))
                cam2Record = True
                Thread(target=camrecord, args=[camid]).start()
            if not cam1Record and camid == 1:
                print('on cam' + str(camid))
                cam1Record = True
                Thread(target=camrecord, args=[camid]).start()
        case 'off':
            if cam2Record and camid == 2:
                print('off cam' + str(camid))
                cam2Record = False
            if cam1Record and camid == 1:
                print('off cam' + str(camid))
                cam1Record = False
        case _:
            print(action, camid)
            return 'Incorrect action', 400
    return 'ok'


def camrecord(camid: [1, 2]):
    global cam2Record
    global cam1Record
    if camid == 2:
        name = 'Elevator'
        fps = 3
        cameraCapture = cv2.VideoCapture('http://second-espcam.local:80')
    elif camid == 1:
        name = 'Hall'
        fps = 3
        cameraCapture = cv2.VideoCapture('http://espcam.local:80')
    else:
        return -1
    size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    videoWriter = cv2.VideoWriter(f'{name} - {datetime.datetime.now().strftime("%m.%d.%Y - %H.%M.%S")}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    while cam1Record if camid == 1 else cam2Record:
        success, frame = cameraCapture.read()
        frame = cv2.putText(frame, datetime.datetime.now().strftime("%m.%d.%Y - %H:%M:%S"),
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 255, 255),
                            2)
        videoWriter.write(frame)
    cameraCapture.release()


if __name__ == '__main__':
    if os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False):
        serve(app, host='0.0.0.0', port=8881, url_scheme='http')
    else:
        serve(app, host='192.168.1.10', port=8881, url_scheme='http')
'''
TODO:
создавать папку если не существует для сохр видео
автоудаление

'''
