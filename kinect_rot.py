from pykinect import nui
import keyboard
import time
from threading import Thread
from win32gui import GetForegroundWindow, GetWindowText
import cv2
import numpy
#   User config
_MAX_ANGLE, _MIN_ANGLE = 16, -16
_ANGLE_INC = 8
_CONSTANT_ROTATION_ALLOWED = True

#   Don't change these bro
__CONSTANT_ROTATION_MEME = True
__THREAD_STARTED = False
CUR_CAM = ['left']
RIGHT_CAM = cv2.VideoCapture(0)
BREAKTHRD = [False]
TIME_DELAY = 0.1
TIME_DELAY_INC = 0.05

def video_handler_function(frame):
    global CUR_CAM, RIGHT_CAM
    #print(CUR_CAM[0])
    if CUR_CAM[0] == 'left':
        video = numpy.empty((480,640,4),numpy.uint8)
        frame.image.copy_bits(video.ctypes.data)
    elif CUR_CAM[0] == 'right':
        ret, video = RIGHT_CAM.read()
    cv2.imshow('KINECT Video Stream', video)
    
    
def epic_constant_rotation_meme(camera,running):
    while True:
        if running[0] == True:
            camera.set_elevation_angle(16)
        if running[0] == True:
            camera.set_elevation_angle(-16)

def _rot_quickswap(running):
    running[0] = not running[0]

def rotate_camera(direction, angle_inc, camera):
    angle = camera.get_elevation_angle()
    if direction == "up":
        if angle < _MAX_ANGLE:
            angle += angle_inc
            camera.set_elevation_angle(angle)
    elif direction == "down":
        if angle > _MIN_ANGLE:
            angle -= angle_inc
            camera.set_elevation_angle(angle)
            
def _cam_swap(cur_cam):
    if cur_cam[0] == 'left': cur_cam[0] = 'right'
    else: cur_cam[0] = 'left'

def _breakthrd_quickswap():
    global BREAKTHRD
    BREAKTHRD[0] = not BREAKTHRD[0]

def epic_cam_swap_meme(cur_cam):
    global BREAKTHRD, TIME_DELAY
    while True:
        if not BREAKTHRD[0]: 
            _cam_swap(cur_cam)
            time.sleep(abs(TIME_DELAY))

def adjust_time_delay(adjustment_amnt):
    global TIME_DELAY
    TIME_DELAY += adjustment_amnt
    print(TIME_DELAY)
    if TIME_DELAY <= 0:
        TIME_DELAY = 0.1
        
def run():
    runtime = nui.Runtime()
    running = [False]
    allow_cam_swap = [True]
    # What does this do????? vvvvvvvvvvvvvvvvvvvvvvvvv
    runtime.video_frame_ready += video_handler_function
    runtime.video_stream.open(nui.ImageStreamType.Video, 2,
                             nui.ImageResolution.Resolution640x480,
                             nui.ImageType.Color)
    cv2.namedWindow('KINECT Video Stream', cv2.WINDOW_AUTOSIZE)
    
    
    camera = nui.Camera(runtime)
    Thread(target=epic_constant_rotation_meme,args=(camera,running,)).start()
    Thread(target=epic_cam_swap_meme,args=(CUR_CAM,)).start()
    keyboard.add_hotkey('home', rotate_camera, args=('up',8,camera))
    keyboard.add_hotkey('end', rotate_camera, args=('down',8,camera))
    keyboard.add_hotkey('ctrl+shift+space', _rot_quickswap,
                        args=(running,))
    keyboard.add_hotkey('ctrl+shift+end', _cam_swap,
                        args=(CUR_CAM,))
    keyboard.add_hotkey('ctrl+shift+page up', adjust_time_delay, args=(TIME_DELAY,))
    keyboard.add_hotkey('ctrl+shift+page down', adjust_time_delay, args=(-TIME_DELAY,))
    keyboard.add_hotkey('ctrl+shift+home', _breakthrd_quickswap,args=())
    
    while True:
        key = cv2.waitKey(0)
        if key == 27:
            RIGHT_CAM.release()
            cv2.destroyWindow('KINECT Video Stream')
            runtime.close()
            break
                
if __name__=="__main__":
    run()
