from openai import OpenAI
import json
import base64
import requests

# CONFIG
config_file = 'config.json'

api_key = "AIzaSyB6MAFkosbeLZPXv22LVLu0magOj-fuPZI"
model_name = "gemini-2.0-flash"
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"


# Hàm đọc config về các trường cần trích xuất
def read_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        _config_json = json.load(file)
    return _config_json


# Hàm chuyển image thành base64
def encode_image(image_url):
    with open('input.jpg', 'wb') as handle:
        _response = requests.get(image_url, stream=True)
        if not _response.ok:
            print(_response)
        for block in _response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    with open("input.jpg", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


config_json = read_config(config_file)

ocr_prompt = 'Trích xuất các dữ liệu trong ảnh. trả về dạng json theo mẫu:\n' + json.dumps(config_json,
                                                                                           ensure_ascii=False)
ocr_photo = 'https://xdcs.cdnchinhphu.vn/446259493575335936/2024/5/3/trang-1-1714725910095750701540.jpg'

base64_image = encode_image(ocr_photo)
client = OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model=model_name,
    messages=[{
        'role': 'user',
        'content': [{
            'type': 'text',
            'text': ocr_prompt,
        }, {
            'type': 'image_url',
            'image_url': {
                'url': f"data:image/jpeg;base64,{base64_image}"
            },
        }],
    }],
    temperature=0.6,
    top_p=0.8,
    max_tokens=128)

print(response.choices[0].message.content)
