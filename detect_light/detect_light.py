import cv2
import numpy as np


def detect_light_in_image(image_path):
    # Đọc ảnh
    image = cv2.imread(image_path)
    if image is None:
        print("Could not open or find the image.")
        return

    # Chuyển ảnh sang không gian màu HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Xác định khoảng ngưỡng của màu trắng trong không gian màu HSV
    # Các giá trị này có thể cần được điều chỉnh tùy thuộc vào điều kiện ánh sáng và đèn
    # HSV Hue (H): Mô tả màu sắc của pixel và có giá trị nằm trong khoảng từ 0 đến 179
    # Saturation (S): Mô tả độ bão hòa của màu sắc. Mức độ bão hòa càng cao, màu càng "rực rỡ"
    #Value (V): Mô tả độ sáng của màu sắc. Mức độ sáng càng cao, màu càng "sáng".

    lower_white = np.array([0, 0, 200], dtype="uint8") #độ bão hòa
    upper_white = np.array([0, 25, 255], dtype="uint8") # độ sáng

    # Tạo mask để phát hiện màu trắng
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Áp dụng các bộ lọc để cải thiện kết quả của mask
    kernel = np.ones((10, 5), np.uint8)
    # kich thước của kernel 7x7 thay vì 5x5) sẽ có hiệu ứng mạnh hơn trong việc giãn nở hoặc co rút các vùng của ảnh
    mask = cv2.dilate(mask, kernel, iterations=1) # làm cho các vùng trắng lớn hơn và kết nối các vùng trắng gần nhau số lần :1
    mask = cv2.erode(mask, kernel, iterations=1) # làm ngược lại, loại bỏ các pixel trắng ở biên của các vùng trắng, giúp loại bỏ nhiễu và định hình lại đối tượng màu trắng

    # Tìm contours trong mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Phát hiện và đánh dấu đèn
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 600:  # Ngưỡng diện tích để xác định đèn
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, 'Light ON', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Hiển thị ảnh
    #cv2.namedWindow("Window", cv2.WINDOW_NORMAL)
    #cv2.imshow("Window", image)
    resized_image = cv2.resize(image, (1000, 900))
    cv2.imshow("Resized Image", resized_image)
  #  cv2.imshow("Mask", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Điền đường dẫn tới ảnh của bạn
detect_light_in_image('light_detect.jpg')
