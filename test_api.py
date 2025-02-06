import requests
import json
import os
from dotenv import load_dotenv

def test_claude_api():
    # 加载 .env 文件中的环境变量
    load_dotenv()
    
    # 从环境变量获取 API Key
    api_key = os.getenv('ALLOW_API_KEY')
    if not api_key:
        print("错误：未找到 ALLOW_API_KEY 环境变量")
        return False

    url = "http://127.0.0.1:8000/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": [
            {"role": "user", "content": "你好，请做个自我介绍"}
        ],
        "stream": True
    }

    try:
        response = requests.post(url, headers=headers, json=data, stream=True, timeout=(10, 120))
        response.raise_for_status()
        
        print("API 测试成功！收到回复：")
        # 添加调试信息
        print("开始读取响应流...")
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                print(f"收到原始数据: {line}")  # 调试信息
                if line.startswith('data: '):
                    data = line[6:]
                    print(f"处理后的数据: {data}")  # 调试信息
                    if data != '[DONE]':
                        try:
                            result = json.loads(data)
                            print(f"解析的 JSON: {result}")  # 调试信息
                            if 'content' in result.get('delta', {}):
                                content = result['delta']['content']
                                print(content, end='', flush=True)
                        except json.JSONDecodeError as e:
                            print(f"JSON 解析错误: {e}")  # 调试信息
                            continue
        print("\n完成响应读取")  # 调试信息
        return True
    except requests.exceptions.RequestException as e:
        print(f"API 测试失败：{e}")
        if hasattr(e.response, 'text'):
            print(f"错误详情：{e.response.text}")
        return False

if __name__ == "__main__":
    print("开始测试 API...")
    test_claude_api() 