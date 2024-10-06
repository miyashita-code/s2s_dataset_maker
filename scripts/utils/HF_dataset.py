import os
import asyncio
import json
import torch
from typing import List, Optional

from dotenv import load_dotenv  
from datasets import Dataset, load_dataset
class DatasetModule:
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
    
    @staticmethod
    def extract_snac_tokens(dataset: Dataset) -> List[torch.Tensor]:
        """
        データセットからSNACトークンを抽出する。

        Args:
            dataset (Dataset): SNACトークンを抽出するデータセット

        Returns:
            List[str]: 抽出されたSNACトークンのリスト
        """
        return dataset["answer_snac"]
    
    @staticmethod
    def extract_answers(dataset: Dataset) -> List[torch.Tensor]:
        """
        データセットから回答テキストを抽出する。

        Args:
            dataset (Dataset): SNACトークンを抽出するデータセット

        Returns:
            List[str]: 抽出されたSNACトークンのリスト
        """
        return dataset["answer"]
    
    def load_text_from_json(self, filename: str) -> List[str]:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data  # List[str]として返す