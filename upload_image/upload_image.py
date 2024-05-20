import requests

def upload_image_to_imgur(image_path, client_id):
    """
    Tải ảnh lên Imgur và trả về URL công khai của ảnh.
    """
    headers = {
        "Authorization": f"Client-ID {client_id}"
    }
    api_url = "https://api.imgur.com/3/image"
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    response = requests.post(api_url, headers=headers, files={"image": image_data})
    response.raise_for_status()  # Sẽ ném ra exception nếu request thất bại
    return response.json()['data']['link']

# Sử dụng Client ID của ứng dụng đăng ký trên Imgur để thực hiện upload
# Bạn sẽ cần thay thế 'your_client_id_here' bằng Client ID thực tế của mình
client_id = 'ff9d3c920b5beec'
image_path = 'light_detect.jpg'

try:
    # Gọi hàm upload ảnh
    image_url = upload_image_to_imgur(image_path, client_id)
    print(f"Image successfully uploaded. Imgur URL is: {image_url}")
except Exception as e:
    print(f"An error occurred: {e}")
