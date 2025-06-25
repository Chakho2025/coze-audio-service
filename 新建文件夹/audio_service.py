from flask import Flask, request, jsonify
from pydub import AudioSegment
import base64
import io
import os
import logging

app = Flask(__name__)

# 从环境变量获取API密钥
API_KEY = os.environ.get("API_KEY", "default-secret-key")

@app.route('/process-audio', methods=['POST'])
def process_audio():
    # 验证API密钥
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 获取请求数据
        data = request.json
        audio_b64 = data['audio_data']
        action = data['action']
        
        # 解码Base64音频
        audio_bytes = base64.b64decode(audio_b64)
        audio_format = data.get('format', 'mp3')
        
        # 创建音频对象
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=audio_format)
        
        # 根据操作类型处理音频
        if action == 'trim':
            start = data['start'] * 1000  # 秒转毫秒
            end = data['end'] * 1000
            result = audio[start:end]
            output_format = audio_format
        
        elif action == 'change_speed':
            speed_factor = data['factor']
            result = audio.speedup(playback_speed=speed_factor)
            output_format = audio_format
        
        elif action == 'convert':
            new_format = data['to_format']
            result = audio
            output_format = new_format
        
        # 导出处理后的音频
        output_buffer = io.BytesIO()
        result.export(output_buffer, format=output_format)
        
        # 返回Base64编码结果
        return jsonify({
            "status": "success",
            "audio_data": base64.b64encode(output_buffer.getvalue()).decode('utf-8'),
            "format": output_format
        })
        
    except Exception as e:
        logging.error(f"处理失败: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()