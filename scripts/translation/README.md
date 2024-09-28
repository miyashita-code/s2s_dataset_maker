# Translatorモジュールの使用方法

このモジュールは、単発でのテキストの翻訳とバッチでの翻訳をサポートしています。英語から日本語への翻訳、書き言葉から話し言葉への変換、そしてフィラーを含む口語スタイルへの変換が可能です。以下に各使用例を示します。

## Translatorクラスの概要

`Translator`クラスは、以下の主要なメソッドを提供します：

- `translate_en2ja`: 英語から日本語へ翻訳します。
- `translate_text2spoken`: 書き言葉を話し言葉スタイルに変換します。
- `translate_text2spoken_with_filler`: 書き言葉をフィラーを含む口語スタイルに変換します。

これらのメソッドには、単一のテキストを処理する同期バージョンと、複数のテキストを一括で処理する非同期バッチバージョンがあります。

## 単発翻訳の使用例

単一のテキストを翻訳する方法です。

```python
import asyncio
from translator import Translator

async def single_translate():
    translator = Translator(api_key="your_api_key")
    result = await translator.translate_en2ja("Hello, world!")
    print(result)

asyncio.run(single_translate())
```

## バッチ翻訳の使用例

複数のテキストを一括で翻訳する方法です。

```python
import asyncio
import os

from dotenv import load_dotenv

from translator import Translator

load_dotenv()

async def batch_translate():
    translator = Translator(api_key=os.getenv("OPENAI_API_KEY"))
    texts = ["Hello, world!", "How are you?", "Good morning!"]
    results = await translator.batch_translate_en2ja(texts, max_size=100)
    for original, translated in zip(texts, results):
        print(f"{original} -> {translated}")

asyncio.run(batch_translate())
```

## 各メソッドの詳細な使用例

### `translate_en2ja` メソッドの使用例

英語から日本語への翻訳を行います。

```python
import asyncio
import os

from dotenv import load_dotenv

from translator import Translator

load_dotenv()

async def translate_en2ja_example():
    translator = Translator(api_key=os.getenv("OPENAI_API_KEY"))
    english_texts = ["Hello, how are you?", "The weather is nice today."]
    translations = await translator.batch_translate_en2ja(english_texts, max_size=5)
    for original, translated in zip(english_texts, translations):
        print(f"{original} -> {translated}")

asyncio.run(translate_en2ja_example())
```

### `translate_text2spoken` メソッドの使用例

書き言葉を話し言葉スタイルに変換します。

```python
import asyncio
import os

from dotenv import load_dotenv

from translator import Translator

load_dotenv()

async def translate_text2spoken_example():
    translator = Translator(api_key=os.getenv("OPENAI_API_KEY"))
    written_texts = [...]
    translations = await translator.batch_translate_text2spoken(written_texts, max_size=5)
    for original, translated in zip(written_texts, translations):
        print(f"{original} -> {translated}")

asyncio.run(translate_text2spoken_example())
```

### `translate_text2spoken_with_filler` メソッドの使用例

書き言葉をフィラーを含む口語スタイルに変換します。

```python
import asyncio
import os

from dotenv import load_dotenv

from translator import Translator

load_dotenv()

async def translate_text2spoken_with_filler_example():
    translator = Translator(api_key=os.getenv("OPENAI_API_KEY"))
    written_texts_for_filler = [...]
    translations = await translator.batch_translate_text2spoken_with_filler(written_texts_for_filler, max_size=5)
    for original, translated in zip(written_texts_for_filler, translations):
        print(f"{original} -> {translated}")

asyncio.run(translate_text2spoken_with_filler_example())
```

## 負荷分散を考慮したバッチ翻訳の使用例

大量のテキストを処理する際に、システムリソースとAPIの制限を考慮した使用方法です。

```python
import asyncio
import os

from dotenv import load_dotenv

from translator import Translator

load_dotenv()

async def load_balanced_batch_translate():
    translator = Translator(api_key=os.getenv("OPENAI_API_KEY"))
    test_input : list[str] = [...] #like size 1000
    max_size = 100 # sample_size

    # example1 : バッチ翻訳　(non reccomended)
    translations = await translator.batch_translate_en2ja(test_input, max_size=max_size)

    # examlpl2 : バッチごとに分割して翻訳(recommended)
    for i in range(0, len(test_input), max_size):
        batch = test_input[i:i + max_size]
        translations = await translator.batch_translate_en2ja(batch, max_size=max_size)
        # 結果を保存または処理
        save_results(batch, translations)

asyncio.run(load_balanced_batch_translate())
```

## 注意事項

- このREADMEは `Translator` モジュール専用です。プロジェクト全体のセットアップや依存関係については含まれていません。
- バッチ翻訳を行う際は、システムのリソースやAPIの制限を考慮して `max_size` を設定してください。

このREADMEは、`Translator`クラスの主要な機能と使用方法を説明しています。各メソッドの詳細な動作については、コード内のdocstringを参照してください。


