import datetime
import os
from threading import Thread

import cv2
from flask import Flask, request
from waitress import serve

app = Flask(__name__)
cam2Record = False
cam1Record = False


@app.route('/cam2', methods=['GET', 'POST'])
def cam2():
    global cam2Record
    action = request.args.get('action')
    match action:
        case 'on':
            if not cam2Record:
                print('on cam2')
                cam2Record = True
                fps = 4
                cameraCapture = cv2.VideoCapture('http://second-espcam.local:80')
                size = (int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                videoWriter = cv2.VideoWriter(f'{datetime.datetime.now().strftime("%m.%d.%Y - %H.%M.%S")}.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
                numFrames = 0
                while cam2Record:
                    success, frame = cameraCapture.read()
                    cv2.imshow('frame', frame)
                    frame = cv2.putText(frame, datetime.datetime.now().strftime("%m.%d.%Y - %H:%M:%S"),
                                        (10, 30),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 255, 255),
                                        2)
                    cv2.imshow('frame', frame)

                    videoWriter.write(frame)
                    numFrames += 1
                cameraCapture.release()
        case 'off':
            print('off cam2')
            cam2Record = False
        case _:
            print(action)
            return 'Incorrect action', 400
    return 'ok'


def cam2record():
    global cam2Record



if __name__ == '__main__':
    if os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False):
        serve(app, host='0.0.0.0', port=8881, url_scheme='http')
    else:
        serve(app, host='192.168.1.10', port=8881, url_scheme='http')
