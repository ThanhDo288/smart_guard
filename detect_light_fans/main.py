import cv2
import numpy as np

# Khởi tạo BackgroundSubtractorMOG2
backSub = cv2.createBackgroundSubtractorMOG2()

def detect_objects(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # Tìm contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 300:
            # Xác định hình dạng dựa trên đặc điểm của contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

            if len(approx) == 3:
                shape_name = "Triangle"
            elif len(approx) == 4:
                shape_name = "Quadrilateral"
            elif len(approx) > 10:
                shape_name = "Circle"

            # Vẽ và ghi nhãn contour
            x, y, w, h = cv2.boundingRect(approx)
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            cv2.putText(frame, shape_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

def process_frame(frame):
    # Chuyển ảnh sang không gian màu HSV để phát hiện đèn
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 220], dtype="uint8")
    upper_white = np.array([0, 50, 255], dtype="uint8")
    mask_light = cv2.inRange(hsv, lower_white, upper_white)
    kernel = np.ones((10, 10), np.uint8)
    # kich thước của kernel 7x7 thay vì 5x5) sẽ có hiệu ứng mạnh hơn trong việc giãn nở hoặc co rút các vùng của ảnh
    mask_light = cv2.dilate(mask_light, kernel, iterations=1)  # làm cho các vùng trắng lớn hơn và kết nối các vùng trắng gần nhau số lần :1
    mask_light = cv2.erode(mask_light, kernel,iterations=1)  # làm ngược lại, loại bỏ các pixel trắng ở biên của các vùng trắng, giúp loại bỏ nhiễu và định hình lại đối tượng màu trắng

    # Phát hiện quạt quay bằng cách sử dụng trừ nền
    fgMask = backSub.apply(frame)
    # Áp dụng các phép xử lý hình ảnh để cải thiện kết quả phát hiện
    fgMask = cv2.erode(fgMask, np.ones((5, 5), np.uint8), iterations=1)
    fgMask = cv2.dilate(fgMask, np.ones((5, 5), np.uint8), iterations=1)
    # Làm mịn mask để giảm nhiễu
    fgMask = cv2.GaussianBlur(fgMask, (3, 3), 0)
    # Đóng các vùng trắng trong mask
    fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    # Ngưỡng hóa để tạo ra mask nhị phân
    _, fgMask = cv2.threshold(fgMask, 130, 255, cv2.THRESH_BINARY)
    # Sử dụng Canny để phát hiện cạnh và tìm contours
    fgMask = cv2.Canny(fgMask, 20, 200)
    contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Vẽ contours lên frame gốc
    '''for contour in contours:
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            cv2.putText(frame, 'Fan Movement', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)'''
    for i in range(len(contours)):
        (x, y, w, h) = cv2.boundingRect(contours[i])
        area = cv2.contourArea(contours[i])
        if area > 50:
            cv2.drawContours(fgMask, contours[i], 0, (0, 0, 255), 6)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Fan Movement', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    # Tìm và đánh dấu vị trí của đèn
    contours_light, _ = cv2.findContours(mask_light, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_light:
        area = cv2.contourArea(contour)
        if area > 50:  # Ngưỡng diện tích để xác định đèn
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, 'Light ON', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return frame


# Mở video từ camera
capture = cv2.VideoCapture('test3.mp4')  # Hoặc đường dẫn đến video của bạn
#capture = cv2.VideoCapture(0)  # Hoặc đường dẫn đến video của bạn

while True:
    ret, frame = capture.read()
    if not ret:
        break

    # Xử lý frame hiện tại
    processed_frame = process_frame(frame)

    # Hiển thị frame đã xử lý
    cv2.imshow('Processed Frame', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
