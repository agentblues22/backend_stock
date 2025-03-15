import json
import requests
from openai import OpenAI
import pandas as pd
news = json.load(open('news.json', 'r'))
news_series = news["feed"]
datf = pd.DataFrame.from_dict(news_series)
headlines=datf["title"].tolist()



response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
  },
  data=json.dumps({
    "model": "deepseek/deepseek-r1:free", # Optional
    "messages": [
      {
        "role": "user",
        "content": "predict stock market trend based on the given two headlines."+headlines[2]+","+headlines[3]
      }
    ]
  })
)
print(response)
res=response.json()
print(res['choices'][0]['message']['content'])