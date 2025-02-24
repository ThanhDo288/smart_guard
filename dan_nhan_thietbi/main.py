
import cv2
import numpy as np
import json

rois = []
labels = []
# Khởi tạo các đối tượng BackgroundSubtractorMOG2 riêng biệt cho mỗi ROI
backSubs = []

# Hàm để lưu các ROI và nhãn vào file
def save_rois(rois, labels, filename="rois.json"):
    data = {'rois': rois, 'labels': labels}
    with open(filename, 'w') as f:
        json.dump(data, f)

# Hàm để tải các ROI và nhãn từ file
def load_rois(filename="rois.json"):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['rois'], data['labels']

# Hàm để vẽ các ROI
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, rois, labels
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        roi = (ix, iy, x - ix, y - iy)
        label = input("Enter the label for this ROI (lamp/fan): ")
        rois.append(roi)
        labels.append(label)
        backSubs.append(cv2.createBackgroundSubtractorMOG2())
        cv2.imshow('image', img)

        save_rois(rois, labels)  # Lưu các ROI mới khi hoàn thành
        #cv2.destroyAllWindows()

def process_frame(frame):
    global rois, labels, backSubs
    for roi, label, backSub in zip(rois, labels, backSubs):
        x, y, w, h = roi
        # Đảm bảo rằng ROI có kích thước hợp lệ và không nằm ngoài phạm vi của ảnh
        if w > 0 and h > 0 and x + w <= frame.shape[1] and y + h <= frame.shape[0]:
            roi_frame = frame[y:y + h, x:x + w]
            hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)


        if label == 'lamp':
            process_lamp(hsv, x, y, w, h, frame)
        if label == 'fan':
            # Áp dụng Gaussian Blur để giảm nhiễu và làm mịn hình ảnh
            blurred_frame = cv2.GaussianBlur(roi_frame, (5, 5), 0)

            # Cập nhật các tham số của BackgroundSubtractor
            fgMask = backSub.apply(blurred_frame, None,0.5)  # Tăng learning rate để nhanh chóng thích ứng với thay đổi
            _, fgMask = cv2.threshold(fgMask, 25, 255, cv2.THRESH_BINARY)
            fgMask = cv2.erode(fgMask, np.ones((3, 3), np.uint8), iterations=1)
            fgMask = cv2.dilate(fgMask, np.ones((5, 5), np.uint8),iterations=3)  # Dilation mạnh hơn để nối các vùng chuyển động nhỏ

            contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 50:  # Điều chỉnh ngưỡng diện tích tùy theo kích thước ROI
                    x1, y1, w1, h1 = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w1, y + y1 + h1), (0, 255, 0), 2)
                    cv2.putText(frame, 'Fan Movement', (x + x1, y + y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0, 255, 0), 2)
    return frame
def process_lamp(hsv, x, y, w, h, frame):
    lower_white = np.array([0, 0, 150], dtype="uint8")
    upper_white = np.array([0, 50, 255], dtype="uint8")
    mask_light = cv2.inRange(hsv, lower_white, upper_white)
    kernel = np.ones((10, 10), np.uint8)
    mask_light = cv2.dilate(mask_light, kernel, iterations=1)
    mask_light = cv2.erode(mask_light, kernel, iterations=1)
    contours_light, _ = cv2.findContours(mask_light, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    for contour in contours_light:
        area = cv2.contourArea(contour)
        if area > 30:
            cv2.putText(frame, 'Light ON', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
# Chọn khung hình đầu tiên từ video
#capture = cv2.VideoCapture('test3.mp4')
#capture = cv2.VideoCapture(0)
ret, img = capture.read()
capture.release()

if not ret:
    print("Failed to grab frame")
    exit()

if input("Do you want to load previous ROIs? (yes/no): ").lower() == 'yes':
    rois, labels = load_rois()  # Tải lại các ROI nếu người dùng chọn
    backSubs = [cv2.createBackgroundSubtractorMOG2() for _ in rois]

else:
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle)
    while True:
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
            break
    cv2.destroyAllWindows()

# Reload video for processing
#capture = cv2.VideoCapture('test3.mp4')
#capture = cv2.VideoCapture(0)
while True:
    ret, frame = capture.read()
    if not ret:
        break

    processed_frame = process_frame(frame)
    cv2.imshow('Processed Frame', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
