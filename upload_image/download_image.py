import requests

def download_image(image_url, output_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print("Downloaded successfully")
    else:
        print("Failed to download, status code:", response.status_code)

image_url = "https://imgur.com/fTZzqmq.jpg"  # Thay thế bằng URL hình ảnh thực tế của bạn
output_path = 'downloaded_image.jpg'
download_image(image_url, output_path)
