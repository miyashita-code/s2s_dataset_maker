import os
import asyncio
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from dotenv import load_dotenv
from datasets import load_dataset

#VoiceAssistant-400kのデータセットを取得する
dataset = load_dataset("gpt-omni/VoiceAssistant-400k", split="train")

load_dotenv()

api_key = os.getenv("OPEN_API_KEY")

#`split_name`列の`identity`のデータを抽出したデータセット
dataset_identity = dataset.filter(lambda example: example["split_name" == "identity"])

#`question`のテキストデータを抽出したリスト
question_text_list = dataset_identity["question"]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

template = "次の文章を英語から日本語に翻訳してください。{prompt_text}"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたは英日翻訳者です。"),
        ("user", template)
    ]
)

output_parser = StrOutputParser()

#翻訳結果を保存するリスト
translated_text_list = []

#個々の翻訳処理を定義した関数
async def translate(text):
    try:
        chain = LLMChain(llm= llm, prompt= prompt)
        result1 = await chain.arun({"prompt_text": text})
        return result1
    except Exception as e:
        print("Translating Error: {text}, Error: {e}")
        return None

#複数の翻訳処理を並行処理する関数
async def mulch_translate(text_list):
    tasks = [translate(text) for text in text_list]
    result2 = await asyncio.gather(*tasks)
    return result2

#`mulch_translate`関数に翻訳前データを渡して実行するJSONファイルに出力する関数
async def translate_text():
    translated_text_list = await mulch_translate(question_text_list)

    #JSONファイルに書き込む
    with open("translated.json", "w") as f:
        json.dump(translated_text_list, f, indent= 4)

asyncio.run(translate_text)

""""
for translate_text in dataset_question:
    chain = prompt | llm | output_parser
    translation = chain.invoke({"prompt_text": translate_text})
    translated_text.append(translation)
"""

"""
# 翻訳結果を表示
for original, translated in zip(text_to_translate, translated_text):
    print(f"Original: {original}")
    print(f"Translated: {translated}")
    print("-" * 40)
"""