from openai import OpenAI
import json

# Cấu hình
config_file = "config.json"
base_url = "http://103.78.3.31:8000/v1"
api_key = "KHONGCAN"


# Hàm đọc file config
# Hàm đọc config về các trường cần trích xuất
def read_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        _config_json = json.load(file)
    return _config_json


config_json = read_config(config_file)

ocr_prompt = 'Trích xuất các dữ liệu trong ảnh. trả về dạng json theo mẫu:\n' + json.dumps(config_json,
                                                                                           ensure_ascii=False)
print(ocr_prompt)

ocr_photo = "https://xdcs.cdnchinhphu.vn/446259493575335936/2024/5/3/trang-1-1714725910095750701540.jpg"

# Nhận diện OCR
client = OpenAI(api_key=api_key, base_url=base_url)
model_name = client.models.list().data[0].id

response = client.chat.completions.create(
    model=model_name,
    messages=[
        {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': ocr_prompt
                },
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': ocr_photo
                    }
                }
            ]
        }
    ],
    temperature=0.6,
    top_p=0.8,
    max_tokens=128
)

print(response.choices[0].message.content)