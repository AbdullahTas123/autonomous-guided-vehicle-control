from src.sensors.cam import Camera
from src.run import ManualControl, AutonomousControl

class Config:
    def __init__(self, args:dict) -> None:
        self.camera = Camera(show=args['show'],
                             captureIndex=args['captureIndex'],
                             camRes=(args['capWidth'], args['capHeight']))
        self.camera.set_camera_settings(args['focalLenght'])
        self.camera.set_aruco_settings(markerSize=args['markerSize'],
                                       totalMarkers=args['totalMarkers'],
                                       arucoWidth=args['arucoWidth'])
        self.control = self.define_control_mode(args['mode'])
    
    def define_control_mode(self, mode:int):
        if mode == 0:
            return ManualControl()
        if mode == 1:
            return AutonomousControl()
