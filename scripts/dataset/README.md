# Dataset Maker モジュール仕様書

## 概要
Dataset Maker モジュールは、テキストデータの翻訳、音声合成、SNACエンコードを行うためのクラスを提供します。主に `Dataset` クラスが含まれており、データセットの作成を簡素化します。

## クラス

### Dataset
テキストデータの翻訳、音声合成、SNACエンコードを行うクラス。

#### メソッド
- `__init__()`
  - 初期化メソッド。環境変数を読み込み、必要なインスタンスを初期化します。

- `translate_texts(texts: list, filename: str) -> None`
  - 指定されたテキストのリストを翻訳し、結果を指定されたファイルに保存します。

- `translation() -> None`
  - データセットの "question" と "answer" を翻訳し、それぞれの結果をファイルに保存します。

- `audio_maker(filename: str) -> None`
  - 指定されたJSONファイルからテキストを読み込み、音声合成を行います。

- `snac_encode() -> None`
  - 音声ファイルをSNACトークンにエンコードし、デコードされた音声を指定したパスに保存します。

## 使用例

### データセットの翻訳
```python
import asyncio
from scripts.dataset.dataset_maker import Dataset

async def main():
    dataset = Dataset()
    await dataset.translation()  # 翻訳を実行

if __name__ == "__main__":
    asyncio.run(main())
```

### 音声合成の実行
```python
async def main():
    dataset = Dataset()
    await dataset.translation()  # 翻訳を実行
    audio_filename = "dataset_answers.json"  # 音声合成したいテキストのJSONファイル名
    await dataset.audio_maker(audio_filename)  # 音声合成を実行

if __name__ == "__main__":
    asyncio.run(main())
```

### SNACエンコードの実行
```python
async def main():
    dataset = Dataset()
    await dataset.translation()  # 翻訳を実行
    audio_filename = "dataset_answers.json"
    await dataset.audio_maker(audio_filename)  # 音声合成を実行
    await dataset.snac_encode()  # SNACエンコードを実行

if __name__ == "__main__":
    asyncio.run(main())
```

## 注意事項
- 翻訳を行う際は、`dataset_maker`から以下の数値を調整してAPIリクエストのRate Limit Errorが出ないように注してください

### dataset_maker.py の translate_textsメソッド
```python
    async def translate_texts(self, texts, filename):
        """
        テキストの翻訳を行う共通メソッド
        """
        #2つのmaxsizeから1batchの処理サイズを調整
        translated_text = await self.translator.batch_translate_en2ja(texts, max_size=10)
        speech_text = await self.translator.batch_translate_text2spoken_with_filler(translated_text, max_size=10)
        #await asyncio.sleep(10)
        results = JSONWriter.write_to_json(speech_text, filename=filename)
        print(f"{filename}の書き込みが完了しました。")
        return results
```
### translator.py の batch_translateメソッド
```python
    async def batch_translate(self, texts: List[str], max_size: int) -> List[Optional[str]]:
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

            # 処理間隔を設定して短時間のAPIリクエスト量を調整する
            await asyncio.sleep(10)
        
        return results
```

- 音声合成やSNACエンコードを行う際は、必要な音声ファイルが生成されていることを確認してください。
- エラーが発生した場合は、エラーメッセージを確認し、必要に応じてコードを修正してください。
- 環境変数にOpenAI APIキーを設定することを忘れないでください。

## まとめ
このプロジェクトを使用することでテキストデータの翻訳、音声合成、SNACエンコードを簡単に実行できます。必要なライブラリをインストールし、環境変数を設定した後、上記の手順に従ってデータセットを作成してください。