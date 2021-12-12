import math
import cv2
import cv2.aruco as aruco
import numpy as np

class Camera:
    def __init__(self, show:bool, captureIndex:int, camRes:tuple,) -> None:
        self.show = show
        self.captureIndex = captureIndex
        self.resolution = camRes
        self.out = False

    def set_camera_settings(self, focal_length:float):
        self.cap = cv2.VideoCapture(self.captureIndex, cv2.CAP_DSHOW)
        self.cap.set(3, self.resolution[0])
        self.cap.set(4, self.resolution[1])
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.focalL = focal_length
    
    def set_aruco_settings(self, markerSize, totalMarkers, arucoWidth):
        self.aruco_key = aruco.Dictionary_get(getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}'))
        self.aruco_params = aruco.DetectorParameters_create()
        self.aruco_params.adaptiveThreshConstant = 10
        self.aruco_real_width = arucoWidth
        self.num_of_arucos = 0
    
    def calc_focal_length(self):
        pass
    
    def distance_to_camera(self, aruco_size_px):
        return (self.aruco_real_width * self.focalL) / aruco_size_px
    
    def set_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame
            self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def detect_aruco(self):
        #if hasattr(self, 'frame'):
        corners, ids, _ = aruco.detectMarkers(self.gray, self.aruco_key, parameters=self.aruco_params)
        if np.all(ids != None):
            self.ids = ids.flatten()
            print(self.ids)
            self.arucoDetected = True
            self.num_of_arucos = len(self.ids)

            aruco.drawDetectedMarkers(self.frame, corners)

            markers = [cv2.minAreaRect(c) for c in corners]
            dims = [sum(marker[1])/2.0 for marker in markers]
            
            self.dist2cam_real_cm_all = [self.distance_to_camera(dim) for dim in dims]
            
            # Kameranın orta noktasını bulma
            (h, w) = self.frame.shape[:2] #w:image-width and h:image-height
            self.centerCamera = (w//2,h//2)
            
            # Aruconun orta noktasını bulma
            self.centerArucos = [(int(marker[0][0]), int(marker[0][1])) for marker in markers]

            # Orta noktaların arsındaki çizginin; önce pixel sonra cm uzunluğu buldurma, en son olarak derece buldurma
            dist2center_frame_px_all = [centerAruco[0] - self.centerCamera[0] for centerAruco in self.centerArucos]

            self.dist2_yaxis_real_cm_all = [(self.aruco_real_width / dims[i] ) * dist2center_frame_px_all[i] for i in range(self.num_of_arucos)]
            self.angles= [math.degrees(math.atan(self.dist2_yaxis_real_cm_all[j]/self.dist2cam_real_cm_all[j])) for j in range(self.num_of_arucos)]
        else:
            self.arucoDetected = False
        
        if self.show:
            self.draw_in_frame()
    
    def draw_in_frame(self):
        x = self.resolution[0]//2
        cv2.line(self.frame, (x,0), (x,self.resolution[1]), (128, 0, 0), 1)
        if self.arucoDetected:
            for i, id in enumerate(self.ids):
                # Kamera ile Aruconun orta noktaları arasına çizgi çektirme
                cv2.line(self.frame, self.centerCamera, self.centerArucos[i], (128, 0, 128), 2)
                # izdüşüm
                cv2.line(self.frame, (self.centerCamera[0], self.centerArucos[i][1]), self.centerArucos[i], (0, 0, 255), 2)
                # Ekrana değerleri yazdırma
                strg = str(id)+', '+str(np.round(self.dist2cam_real_cm_all[i],2))+" cm"
                cv2.putText(self.frame, "Id: " + strg, (5,15 + (i * 32)), self.font, 0.5, (0,255,0),1,cv2.LINE_AA)
                strg = '{:.5f} cm {:.2f} degree'.format(abs(self.dist2_yaxis_real_cm_all[i]), self.angles[i])
                cv2.putText(self.frame, strg, (5,30 + (i * 32)), self.font, 0.5, (0,0,255),1,cv2.LINE_AA)
                cv2.imshow('frame',self.frame)
        else:
            cv2.putText(self.frame, "No Ids", (5, 15), self.font, 0.5, (0,255,0), 1, cv2.LINE_AA)
            cv2.imshow('frame',self.frame)
    
    def break_and_release(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.out = True
            self.cap.release()
            cv2.destroyAllWindows()
