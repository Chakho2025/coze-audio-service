import requests
import base64

# 测试音频文件路径（准备一个短音频文件）
TEST_AUDIO = "test.mp3"

# 从文件读取测试音频
with open(TEST_AUDIO, "rb") as f:
    audio_data = base64.b64encode(f.read()).decode('utf-8')

# 测试裁剪功能
payload = {
    "audio_data": audio_data,
    "action": "trim",
    "start": 2,
    "end": 4,
    "format": "mp3"
}

headers = {
    "X-API-Key": "your-test-key",  # 与本地运行使用的密钥一致
    "Content-Type": "application/json"
}

# 本地运行时的URL
LOCAL_URL = "http://localhost:5000/process-audio"

response = requests.post(
    LOCAL_URL,
    json=payload,
    headers=headers
)

if response.status_code == 200:
    result = response.json()
    print("✅ 测试成功！")
    # 保存处理后的音频
    with open("trimmed_audio.mp3", "wb") as f:
        f.write(base64.b64decode(result["audio_data"]))
    print("处理后的音频已保存为 trimmed_audio.mp3")
else:
    print(f"❌ 测试失败: {response.status_code}")
    print(response.text)