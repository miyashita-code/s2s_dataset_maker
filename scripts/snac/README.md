# SNACモジュールの使用方法

## SNACDecoderクラスの概要

このモジュールは、SNACトークンを音声データにデコードする機能を提供します。Hugging Faceからデータセットをロードし、SNACトークンを抽出して音声ファイルを生成します。
`SNACDecoder`クラスは、以下の主要なメソッドを提供します：

- `parse_snac_tokens`: SNACトークンの文字列を解析し、リストに分割します。
- `decode_to_audio`: SNACトークンを音声データにデコードし、ファイルに保存します。

## 使用例

### 単発デコードの使用例

単一のSNACトークンをデコードする方法です。

```python
from scripts.snac.snac_module import SNACDecoder
from scripts.utils.HF_dataset import DatasetHandler

#HuggingFaceからデータセットをロードする。
dataset = DatasetHandler.load_dataset("gpt-omni/VoiceAssistant-400k", split="train")

#データセットから「identity」のデータを抽出する。
filtered_dataset = DatasetHandler.filter_dataset(dataset, "identity")   

#データセットから「SNACトークン」のデータを抽出する。
snac_tokens = DatasetHandler.extract_snac_tokens(filtered_dataset)

def main():
    # デコーダーを初期化
    decoder = SNACDecoder()

    # SNACトークンを調整する
    parsed_tokens = decoder.parse_snac_tokens(snac_token)

    # 音声ファイルを出力するパス
    output_path = "output.wav"

    # デコードを実行
    decoder.decode_to_audio(parsed_tokens, output_path)

if __name__ == "__main__":
    main()
```

## 注意事項

- 音声ファイルの出力先は、`output.wav` です。必要に応じて変更してください。
- 動作するコードは、`sample_decode.py` にあります。


## SNACEncoderクラスの概要

このモジュールは、音声データをSNACトークンにエンコードする機能を提供します。音声ファイルを読み込み、SNACトークンを生成します。

`SNACEncoder`クラスは、以下の主要なメソッドを提供します：

- `encode_to_tokens`: 音声ファイルを処理し、SNACトークンにエンコードします。
- `decode_from_tokens`: SNACトークンを音声データにデコードし、ファイルに保存します。

## 使用例

### 単発エンコードの使用例

音声ファイルをSNACトークンにエンコードする方法です。

```python
from scripts.snac.snac_module import SNACEncoder

# 入力する音声ファイルのパス
audio_path = "input.wav"
# 出力する音声ファイルのパス
output_path = "output.wav"

def main():
    # エンコーダーを初期化
    encoder = SNACEncoder(audio_path, output_path)

    # SNACトークンにエンコード
    tokens = encoder.encode_to_tokens()

    # トークンを音声データにデコードし、ファイルに保存
    encoder.decode_from_tokens(tokens)

if __name__ == "__main__":
    main()
```

## 注意事項

- 音声ファイルの入力先は、`input.wav` です。必要に応じて変更してください。
- 出力先の音声ファイルは、`output.wav` です。必要に応じて変更してください。
- 動作するコードは、`sample_encode.py` にあります。

このREADMEは、`SNACEncoder`クラスと`SNACDecoder`クラスの主要な機能と使用方法を説明しています。