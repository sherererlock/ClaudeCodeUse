import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件
load_dotenv()

# 获取 API Key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("错误: 未找到 OPENAI_API_KEY，请检查 .env 文件。")
    exit(1)

# 初始化客户端
client = OpenAI(api_key=api_key)

try:
    print("正在尝试连接 OpenAI...")
    completion = client.chat.completions.create(
        model="gpt-4o-mini", # 使用较新的模型
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Please confirm this connection works by saying 'Connection successful!'."}
        ]
    )
    print("连接成功！OpenAI 回复：")
    print(completion.choices[0].message.content)

except Exception as e:
    print(f"发生错误: {e}")
