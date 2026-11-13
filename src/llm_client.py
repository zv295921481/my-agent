import requests
import os
from dotenv import load_dotenv
from typing import List, Dict
load_dotenv()

from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model=os.getenv("MODEL_ID"),
    instructions="You are a helpful assistant.",
    input="Hello!"
)

message = client.chat.completions.create(
  model=os.getenv("MODEL_ID"),
  messages=[
    {"role": "user", "content": "Hello!"}
  ]
)

message2 = client.chat.completions.create(
  model=os.environ.get("MODEL_ID"),
  messages=[
    {"role":"user", "content":"Hello!"}
  ],
  stream=True
)

class HelloAgentsLLM:
  def __init__(self, model: str=None, apiKey: str=None, baseUrl: str=None, timeout: int=None):
    self.model = model or os.getenv("MODEL_ID")
    apiKey = apiKey or os.getenv("API_KEY")
    baseUrl = baseUrl or os.getenv("BASE_URL")
    timeout = timeout or int(os.getenv("TIMEOUT") or 60)

    if not all([self.model, apiKey, baseUrl]):
      raise Exception("model, apiKey, baseUrl are required")
    
    self.client = OpenAI(
      api_key=apiKey,
      base_url=baseUrl,
      timeout=timeout
    )

  def think(self, messages: List[Dict[str, str]], temperature: float=0):
    print(f"🧠 正在调用 {self.model} 模型...")
    try:
      response = self.client.chat.completions.create(
        model=self.model,
        messages=messages,
        temperature=temperature,
        stream=True
      )

      # 处理流式响应
      print("✅ 大语言模型响应成功:", response)
      collected_content = []
      if response:
        for chunk in response:
          if not chunk.choices[0].delta.content:
            continue
          content = chunk.choices[0].delta.content
          print(content, end="")
          collected_content.append(content)

        print()
        return "".join(collected_content)
    except Exception as e:
      print(f"🧠 调用 {self.model} 模型失败: {e}")
      return None

if __name__ == "__main__":
  try:
    llmClient = HelloAgentsLLM()
    messages = [
      {"role":"system", "content":"You are a helpful assistant."},
      {"role":"user", "content":"Hello!"}
    ]

    exampleMessages = [
        {"role": "system", "content": "You are a helpful assistant that writes Python code."},
        {"role": "user", "content": "写一个快速排序算法"}
    ]
    
    print("--- 调用LLM ---")
    responseText = llmClient.think(exampleMessages)
    if responseText:
        print("\n\n--- 完整模型响应 ---")
        print(responseText)
  except Exception as e:
    print(f"🧠 调用 {llm.model} 模型失败: {e}")


# prtStr = ""

# for chunk in message2:
#   if not chunk.choices[0].delta.content:
#     continue
#   print(chunk.model_dump_json(indent=2))
#   prtStr += chunk.choices[0].delta.content
#   print(prtStr, end="\n")


# print(f"message: {message.model_dump_json(indent=2)}")
# print(f"response: {response.model_dump_json(indent=2)} >>>{response.output_text}")
