from ultralytics import YOLO
import cv2

#Model Çağırma
model = YOLO(r"C:\Users\Cuma\Downloads\cuma-face-v2.v1i.yolov8\runs\detect\cuma-face-v23\weights\best.pt")
# model = YOLO(r"yolov8n.pt")


# Kamera Bağlantısı
USERNAME = "..."
PASSWORD = "..."
CAMERA_IP = "192.168.??.??"
RTSP_PORT = "554"

rtsp_url = f"rtsp://{USERNAME}:{PASSWORD}@{CAMERA_IP}:{RTSP_PORT}/stream1"

cap = cv2.VideoCapture(rtsp_url)
cv2.namedWindow("Kamera",cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Kamera",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
if not cap.isOpened():
    print("Kamera akışına bağlanılamadı. IP ve kimlik bilgilerini kontrol edin.")
    exit()

print("Kameraya bağlanıldı. Çıkmak için 'q' tuşuna basın.")
while cap.isOpened():
    ret,frame = cap.read()
    if not ret:
        break

    result = model(frame)[0]
    # frame = cv2.resize(frame,dsize=(1080,1080))
    for box in result.boxes:
        x1,y1,x2,y2 = map(int,box.xyxy[0])
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        label = f"Cuma {conf:.2f}"
        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 2
        thickness = 3
        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),9)

        (text_w,text_h),baseline = cv2.getTextSize(label,font,font_scale,thickness)
        cv2.rectangle(frame,(x1,y1-text_h-10),(x1+text_w+5,y1),(255,0,0),-1)

        cv2.putText(frame,label,(x1,y1-3),font,font_scale,(255,255,255),thickness) 



   
    cv2.imshow("Kamera",frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
