# SNACデコーダーモジュールの使用方法

このモジュールは、SNACトークンを音声データにデコードする機能を提供します。Hugging Faceからデータセットをロードし、SNACトークンを抽出して音声ファイルを生成します。

## SNACDecoderクラスの概要

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
- 動作するコードは、`test_decode.py` にあります。

このREADMEは、`SNACDecoder`クラスの主要な機能と使用方法を説明しています。