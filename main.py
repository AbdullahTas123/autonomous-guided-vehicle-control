import sys
import signal
import argparse
from config import Config


def signal_handler(signal, frame):
    print("program exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-M', '--mode',         default=0,                 help='Set the mode to run',                        action='store',      type=int,   dest='mode')
    parser.add_argument('-S', '--show',         default=True,             help='Show processed OpenCV video capture frames', action='store_true',             dest='show')
    parser.add_argument('-I', '--captureIndex', default=0,                 help='OpenCV VideoCapture index value',            action='store',      type=int,   dest='captureIndex')
    parser.add_argument('-W', '--capWidth',     default=1280,              help='Width of Cam resolution frame',              action='store',      type=int,   dest='capWidth')
    parser.add_argument('-H', '--capHeight',    default=720,              help='Height of Cam resolution frame',             action='store',      type=int,   dest='capHeight')
    parser.add_argument('-f', '--focalLenght',  default=966.9541358947754, help='Focal lenght of Camera',                     action='store',      type=float, dest='focalLenght')
    parser.add_argument('-m', '--markerSize',   default=4,                 help='Marker size of ArUco',                       action='store',      type=int,   dest='markerSize')
    parser.add_argument('-t', '--totalMarkers', default=50,                help='Total markers of ArUco',                     action='store',      type=int,   dest='totalMarkers')
    parser.add_argument('-w', '--arucoWidth',   default=6,                 help='Width of ArUco',                             action='store',      type=int,   dest='arucoWidth')

    args = parser.parse_args()
    args_dict = vars(args)
    CONFIG = Config(args=args_dict)

    while True:
        CONFIG.camera.set_frame()
        CONFIG.camera.detect_aruco()
        CONFIG.camera.break_and_release()
        if CONFIG.camera.out:
            break
