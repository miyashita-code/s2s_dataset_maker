import asyncio 
import os
from dotenv import load_dotenv
from scripts.translation.translator import Translator, JSONWriter

from scripts.utils.HF_dataset import DatasetModule

# 環境変数の読み込み
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
#必要なインスタンスの初期化
translator = Translator(api_key)
jsonwriter = JSONWriter()
dataset_handler = DatasetModule()

async def main():
    """メイン関数。翻訳処理の全体の流れを制御する。"""
    # 環境変数の読み込み
    api_key = os.getenv("OPENAI_API_KEY")

    #必要なインスタンスの初期化
    translator = Translator(api_key)
    jsonwriter = JSONWriter()
    dataset_handler = DatasetModule()

    #データセットの読み込む
    dataset = dataset_handler.load_dataset("gpt-omni/VoiceAssistant-400k")
    filter_dataset = dataset_handler.filter_dataset(dataset, "identity")
    questions = dataset_handler.extract_answers(filter_dataset)

    # 翻訳の実行
    translated_text = await translator.batch_translate_en2ja(questions[:550], max_size= 10)

    print("翻訳が完了しました")


#if __name__ == "__main__":
#    asyncio.run(main())


async def ajustment_speak():

    #データの読み込み
    text_list = dataset_handler.load_text_from_json("answer_spoken.json")

    await translator.batch_translate_text2spoken_with_filler(text_list[1:50], max_size=5)


asyncio.run(ajustment_speak())
