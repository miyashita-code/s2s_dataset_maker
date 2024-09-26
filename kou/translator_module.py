"""
英語から日本語への翻訳を行うモジュール。

このモジュールは、VoiceAssistant-400kデータセットから英語のテキストを抽出し、
日本語に翻訳して、結果をJSONファイルに保存します。
"""

import os
import asyncio
import json
from typing import List, Optional

from dotenv import load_dotenv
from datasets import Dataset, load_dataset
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain

from translate_prompt import SYSTEM_INSTRUCTION


class DatasetHandler:
    """データセットの処理を行うクラス。"""

    @staticmethod
    def load_dataset(dataset_name: str, split: str = "train") -> Dataset:
        """
        指定されたデータセットを読み込む。

        Args:
            dataset_name (str): 読み込むデータセットの名前
            split (str, optional): データセットのスプリット。デフォルトは"train"

        Returns:
            Dataset: 読み込まれたデータセット
        """
        return load_dataset(dataset_name, split=split)

    @staticmethod
    def filter_dataset(dataset: Dataset, split_name: str) -> Dataset:
        """
        データセットをフィルタリングする。

        Args:
            dataset (Dataset): フィルタリングするデータセット
            split_name (str): フィルタリングに使用するsplit_name

        Returns:
            Dataset: フィルタリングされたデータセット
        """
        return dataset.filter(lambda example: example["split_name"] == split_name)

    @staticmethod
    def extract_questions(dataset: Dataset) -> List[str]:
        """
        データセットから質問テキストを抽出する。

        Args:
            dataset (Dataset): 質問を抽出するデータセット

        Returns:
            List[str]: 抽出された質問のリスト
        """
        return dataset["question"]


class Translator:
    """英語から日本語への翻訳を行うクラス。"""

    def __init__(self, api_key: str, model: str = "gpt-4-0125-preview"):
        """
        Translatorクラスのコンストラクタ。

        Args:
            api_key (str): OpenAI APIキー
            model (str, optional): 使用する言語モデル。デフォルトは"gpt-4-0125-preview"
        """
        self.llm = ChatOpenAI(model=model, temperature=0, openai_api_key=api_key)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_INSTRUCTION),
            ("user", "次の文章を英語から日本語に翻訳してください。その際、日本人に馴染みのある表現で、自然な会話のように翻訳してください。{prompt_text}")
        ])

    async def translate(self, text: str) -> Optional[str]:
        """
        単一のテキストを翻訳する。

        Args:
            text (str): 翻訳する英語のテキスト

        Returns:
            Optional[str]: 翻訳された日本語のテキスト。エラーの場合はNone
        """
        try:
            chain = LLMChain(llm=self.llm, prompt=self.prompt)
            result = await chain.arun({"prompt_text": text})
            return result
        except Exception as e:
            print(f"翻訳エラー: テキスト: {text}, エラー: {e}")
            return None

    async def batch_translate(self, text_list: List[str]) -> List[Optional[str]]:
        """
        複数のテキストを並行して翻訳する。

        Args:
            text_list (List[str]): 翻訳する英語のテキストのリスト

        Returns:
            List[Optional[str]]: 翻訳された日本語のテキストのリスト
        """
        tasks = [self.translate(text) for text in text_list]
        return await asyncio.gather(*tasks)


class JSONWriter:
    """JSONファイルへの書き込みを行うクラス。"""

    @staticmethod
    def write_to_json(data: List[str], filename: str):
        """
        データをJSONファイルに書き込む。

        Args:
            data (List[str]): 書き込むデータ
            filename (str): 出力するJSONファイルの名前
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


async def main():
    """メイン関数。翻訳処理の全体の流れを制御する。"""
    # 環境変数の読み込み
    load_dotenv()
    api_key = os.getenv("OPEN_API_KEY")

    # データセットの準備
    dataset = DatasetHandler.load_dataset("gpt-omni/VoiceAssistant-400k")
    split_name = "identity"
    filtered_dataset = DatasetHandler.filter_dataset(dataset, split_name)
    question_text_list = DatasetHandler.extract_questions(filtered_dataset)

    print("データセットの抽出が完了しました")

    # 翻訳の実行
    translator = Translator(api_key)
    translated_text_list = await translator.batch_translate(question_text_list)

    print("翻訳が完了しました")

    # 結果の出力
    JSONWriter.write_to_json(translated_text_list, "translated.json")

    print("JSONファイルへの書き込みが完了しました")


if __name__ == "__main__":
    asyncio.run(main())