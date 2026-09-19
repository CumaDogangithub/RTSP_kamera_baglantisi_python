# cuma-face-v2

YOLOv8 ile tek sınıflı yüz tespiti. Roboflow'da etiketlenen veri setiyle eğitilen model, bir IP kameranın RTSP akışında gerçek zamanlı çalışır.

## Kurulum

Python 3.10.

```bash
python -m venv yolovenv
yolovenv\Scripts\activate
pip install -r yükle.txt
```

GPU kullanacaksanız `torch` ve `torchvision` paketlerini CUDA sürümleriyle kurun.

## Veri Seti

414 görsel: 290 train, 83 valid, 41 test. Tek sınıf (`cuma-face-v2`), 512×512, YOLOv8 formatı.

Kaynak: <https://universe.roboflow.com/cuma-dogan/cuma-face-v2/dataset/1> (CC BY 4.0)

`data.yaml` mutlak yol kullanıyor. Proje başka bir dizine taşınırsa yollar güncellenmeli.

## Eğitim

```bash
yolo train model=yolov8n.pt data=data.yaml epochs=70 imgsz=640 batch=8 name="cuma-face-v2" patience=300
```

Çıktılar `runs/detect/cuma-face-v23/` altına yazılır, ağırlıklar `weights/best.pt` ve `weights/last.pt`.

VRAM yetmezse `batch` değerini düşürün. Daha yüksek doğruluk için `yolov8n.pt` yerine `yolov8l.pt` ile eğitilebilir, karşılığında eğitim ve çıkarım yavaşlar.

Kesilen eğitime devam etmek için:

```bash
yolo train resume model=runs/detect/cuma-face-v23/weights/last.pt
```

Değerlendirme ve test:

```bash
yolo val model=runs/detect/cuma-face-v23/weights/best.pt data=data.yaml
yolo predict model=runs/detect/cuma-face-v23/weights/best.pt source=test/images save=True
```

## Sonuçlar

70 epoch sonunda doğrulama setinde:

| Precision | Recall | mAP@50 | mAP@50-95 |
|---|---|---|---|
| 0.999 | 0.965 | 0.982 | 0.684 |

Grafikler ve karışıklık matrisi `runs/detect/cuma-face-v23/` içinde: `results.png`, `PR_curve.png`, `F1_curve.png`, `confusion_matrix.png`.

## Çalıştırma

```bash
python app.py
```

RTSP üzerinden kameraya bağlanır, her kareyi modelden geçirir ve tespitleri tam ekranda gösterir. Çıkmak için `q`.

Kamera bilgileri dosyanın başında tanımlı:

```python
USERNAME = "..."
PASSWORD = "..."
CAMERA_IP = "192.168.1.100"
RTSP_PORT = "554"
```

RTSP yol soneki markaya göre değişir — TP-Link'te `/stream1`, Hikvision'da `/Streaming/Channels/101`, Dahua'da `/cam/realmonitor?channel=1&subtype=0`.

Bilgisayarın kendi kamerasını kullanmak için `cv2.VideoCapture(rtsp_url)` yerine `cv2.VideoCapture(0)` yazın.
