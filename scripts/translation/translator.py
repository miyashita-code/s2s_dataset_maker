import asyncio
from typing import List, Optional
from abc import ABC, abstractmethod

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .prompts import (
    translate_en2ja_prompt, 
    translate_en2ja_system_prompt,
    translate_text2spoken_prompt, 
    translate_text2spoken_system_prompt, 
    translate_text2spoken_filler_system_prompt
)


class BaseTranslator(ABC):
    """
    抽象基底クラス：翻訳器の共通インターフェースと機能を定義します。

    Attributes:
        llm (ChatOpenAI): 言語モデルのインスタンス
        prompt (ChatPromptTemplate): 翻訳用のプロンプトテンプレート
        input_variable_name (str): 翻訳時に使用する入力変数名
    """

    def __init__(self, api_key: str, model: str):
        """
        BaseTranslatorを初期化します。

        Args:
            api_key (str): OpenAI APIキー
            model (str): 使用する言語モデル
        """
        self.llm = ChatOpenAI(model=model, temperature=0, openai_api_key=api_key)
        self.prompt = self._create_prompt()
        self.input_variable_name = self._get_input_variable_name()

    @abstractmethod
    def _create_prompt(self) -> ChatPromptTemplate:
        """
        翻訳器用のChatPromptTemplateを作成します。

        Returns:
            ChatPromptTemplate: 翻訳用のプロンプトテンプレート
        """
        pass

    @abstractmethod
    def _get_input_variable_name(self) -> str:
        """
        各サブクラスで期待する入力変数名を返します。

        Returns:
            str: 入力変数名
        """
        pass

    async def translate(self, text: str, is_retry: bool = False) -> Optional[str]:
        """
        単一のテキストを翻訳します。

        Args:
            text (str): 翻訳するテキスト
            is_retry (bool): リトライ試行かどうか

        Returns:
            Optional[str]: 翻訳されたテキスト、失敗時はNone
        """
        try:
            chain = self.prompt | self.llm | StrOutputParser()
            result = await chain.ainvoke({self.input_variable_name: text})
            return result
        except Exception as e:
            import traceback
            traceback.print_exc()
            if is_retry:
                return None
            else:
                return await self.translate(text, is_retry=True)

    async def batch_translate(self, texts: List[str], max_size: int = 100) -> List[Optional[str]]:
        """
        複数のテキストを並列で翻訳します。ただし、指定されたmax_sizeごとにバッチを分割し、
        各バッチ内は並列、バッチ間は直列に処理します。

        Args:
            texts (List[str]): 翻訳するテキストのリスト
            max_size (int): 一度に処理するテキストの最大数

        Returns:
            List[Optional[str]]: 翻訳されたテキストのリスト
        """
        results = []
        # テキストをmax_sizeごとに分割
        for i in range(0, len(texts), max_size):
            batch = texts[i:i + max_size]
            tasks = [self.translate(text) for text in batch]
            # バッチ内は並列に実行
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
        return results


class EnglishToJapaneseTranslator(BaseTranslator):
    """英語から日本語への翻訳を行うクラス"""

    def _create_prompt(self) -> ChatPromptTemplate:
        """英日翻訳用のChatPromptTemplateを作成します。"""
        return ChatPromptTemplate.from_messages([
            ("system", translate_en2ja_system_prompt),
            ("user", translate_en2ja_prompt)
        ])

    def _get_input_variable_name(self) -> str:
        """英日翻訳時に使用する入力変数名を返します。"""
        return "prompt_text"


class TextToSpokenTranslator(BaseTranslator):
    """書き言葉を話し言葉スタイルに変換するクラス"""

    def _create_prompt(self) -> ChatPromptTemplate:
        """書き言葉から話し言葉への変換用ChatPromptTemplateを作成します。"""
        return ChatPromptTemplate.from_messages([
            ("system", translate_text2spoken_system_prompt),
            ("user", translate_text2spoken_prompt)
        ])
    
    def _get_input_variable_name(self) -> str:
        """話し言葉変換時に使用する入力変数名を返します。"""
        return "written_text"


class TextToSpokenWithFillerTranslator(BaseTranslator):
    """フィラーを含む口語スタイルへの翻訳を行うクラス"""

    def _create_prompt(self) -> ChatPromptTemplate:
        """フィラーを含む口語翻訳用のChatPromptTemplateを作成します。"""
        return ChatPromptTemplate.from_messages([
            ("system", translate_text2spoken_filler_system_prompt),
            ("user", translate_text2spoken_prompt)
        ])
    
    def _get_input_variable_name(self) -> str:
        """フィラー付き口語変換時に使用する入力変数名を返します。"""
        return "written_text"


class Translator:
    """
    メイン翻訳クラス：異なるタイプの翻訳器をカプセル化します。

    Attributes:
        en2ja_translator (EnglishToJapaneseTranslator): 英日翻訳器
        text2spoken_translator (TextToSpokenTranslator): 書き言葉から話し言葉への変換器
        text2spoken_with_filler_translator (TextToSpokenWithFillerTranslator): フィラー付き口語変換器
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Translatorを初期化し、各種翻訳器を設定します。

        Args:
            api_key (str): OpenAI APIキー
            model (str): 使用する言語モデル（デフォルト: "gpt-4o-mini"）
        """
        self.en2ja_translator = EnglishToJapaneseTranslator(api_key, model)
        self.text2spoken_translator = TextToSpokenTranslator(api_key, model)
        self.text2spoken_with_filler_translator = TextToSpokenWithFillerTranslator(api_key, model)

    async def translate_en2ja(self, english_text: str) -> Optional[str]:
        """
        英語テキストを日本語に翻訳します。

        Args:
            english_text (str): 翻訳する英語テキスト

        Returns:
            Optional[str]: 翻訳された日本語テキスト、失敗時はNone
        """
        return await self.en2ja_translator.translate(english_text)

    async def batch_translate_en2ja(self, texts: List[str], max_size: int = 100) -> List[Optional[str]]:
        """
        複数の英語テキストを並列で日本語に翻訳します。ただし、max_sizeごとにバッチを分割します。

        Args:
            texts (List[str]): 翻訳する英語テキストのリスト
            max_size (int): 一度に処理するテキストの最大数

        Returns:
            List[Optional[str]]: 翻訳された日本語テキストのリスト
        """
        return await self.en2ja_translator.batch_translate(texts, max_size=max_size)

    async def translate_text2spoken(self, writing_text: str) -> Optional[str]:
        """
        書き言葉を話し言葉スタイルに変換します。

        Args:
            writing_text (str): 変換する書き言葉テキスト

        Returns:
            Optional[str]: 変換された話し言葉スタイルのテキスト、失敗時はNone
        """
        return await self.text2spoken_translator.translate(writing_text)

    async def batch_translate_text2spoken(self, texts: List[str], max_size: int = 100) -> List[Optional[str]]:
        """
        複数の書き言葉テキストを並列で話し言葉スタイルに変換します。ただし、max_sizeごとにバッチを分割します。

        Args:
            texts (List[str]): 変換する書き言葉テキストのリスト
            max_size (int): 一度に処理するテキストの最大数

        Returns:
            List[Optional[str]]: 変換された話し言葉スタイルのテキストのリスト
        """
        return await self.text2spoken_translator.batch_translate(texts, max_size=max_size)

    async def translate_text2spoken_with_filler(self, writing_text: str) -> Optional[str]:
        """
        書き言葉をフィラーを含む口語スタイルに変換します。

        Args:
            writing_text (str): 変換する書き言葉テキスト

        Returns:
            Optional[str]: フィラーを含む口語スタイルに変換されたテキスト、失敗時はNone
        """
        return await self.text2spoken_with_filler_translator.translate(writing_text)
    
    async def batch_translate_text2spoken_with_filler(self, texts: List[str], max_size: int = 100) -> List[Optional[str]]:
        """
        複数の書き言葉テキストを並列でフィラーを含む口語スタイルに変換します。ただし、max_sizeごとにバッチを分割します。

        Args:
            texts (List[str]): 変換する書き言葉テキストのリスト
            max_size (int): 一度に処理するテキストの最大数

        Returns: 
            List[Optional[str]]: フィラーを含む口語スタイルに変換されたテキストのリスト
        """
        return await self.text2spoken_with_filler_translator.batch_translate(texts, max_size=max_size)