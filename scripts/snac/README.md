# SNACモジュール仕様書

## 概要
SNACモジュールは、音声データとSNACトークンの相互変換を行うためのクラスを提供します。主に`SNACDecoder`と`SNACEncoder`の2つのクラスが含まれています。

## クラス

### SNACDecoder
SNACトークンを音声データにデコードするクラス。

#### メソッド
- `__init__()`
  - 初期化メソッド。SNACモデルをロードし、デバイスを設定します。
  
- `_setup_device() -> torch.device`
  - 使用可能なデバイス（CPUまたはGPU）を設定します。

- `_load_model() -> SNAC`
  - 事前学習済みのSNACモデルをロードします。

- `parse_snac_tokens(input_str: str) -> list`
  - SNACトークンの文字列を解析し、リストに分割します。

- `decode_to_audio_44kHz(snac_tokens: list, output_path: str) -> None`
  - 44kHzのSNACトークンを音声データにデコードし、指定されたパスに保存します。

- `decode_to_audio_24kHz(snac_tokens: list, output_path: str) -> None`
  - 24kHzのSNACトークンを音声データにデコードし、指定されたパスに保存します。

### SNACEncoder
音声ファイルをSNACトークンにエンコードするクラス。

#### メソッド
- `__init__(audio_path: str, output_path: str)`
  - 初期化メソッド。音声ファイルのパスを受け取ります。

- `encode_to_tokens(audio_path: str)`
  - 音声ファイルを処理し、SNACトークンにエンコードします。

- `make_snac_tokens(tensor_list: list) -> str`
  - エンコードされたトークンをデータセット用に再構築し、スペースで区切った文字列を返します。

## 使用例

### エンコードの使用例
```python
from scripts.snac.snac_module import SNACEncoder

audio_path = "input.wav"
output_path = "output.wav"

encoder = SNACEncoder()
tokens = encoder.encode_to_tokens(audio_path)
snac_tokens = encoder.make_snac_tokens(tokens)
```

### デコードの使用例
```python
from scripts.snac.snac_module import SNACDecoder

decoder = SNACDecoder()
audio_list = decoder.parse_snac_tokens(snac_tokens)
decoder.decode_to_audio_44kHz(audio_list, output_path)
```

## 注意事項
- 音声ファイルのサンプリングレートに応じて、適切なデコードメソッドを使用してください（44kHzまたは24kHz）。
- モデルのロードには時間がかかる場合がありますので、初期化時に注意してください。