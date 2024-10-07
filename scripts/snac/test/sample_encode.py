"""
このスクリプトは、音声ファイルを入力して、HuggingFaceのデータセット「VoiceAssistant400k」にあるsnac_tokensの形式に合わせるためのサンプルコードです。
"""
import torch
import torchaudio
import soundfile as sf
from snac import SNAC
from scripts.utils.snac_utils import log_device_info, generate_audio_data
from scripts.snac.snac_module import SNACDecoder, SNACEncoder

# 読み込みたい音声ファイルのパスを指定
audio_path = "output/answer_output_1.wav"  # 例: 読み込む音声ファイルのパス
output_path = "data/decoded_1.wav"  # 例: 保存する音声ファイルのパス

#エンコーダーを初期化
encoder = SNACEncoder()

#デコーダーを初期化
decoder = SNACDecoder()

#音声ファイルを渡してトークンにデコード
tokens = encoder.encode_to_tokens(audio_path)
#print(tokens)

# 変換の実行
snac_tokens = encoder.make_snac_tokens(tokens)
print("snac_tokens is", snac_tokens)


"""
以下は、トークンを取得して音声にデコードするためのサンプルコードです。
したがって、コメントアウトを解除すればエンコード→デコードの検証ができます。
"""
#以下、実際のコード

audio_list = decoder.parse_snac_tokens(snac_tokens)
#print("parsed for reconstruct", audio_list)

#トークンと出力先を渡して音声にデコードする
audio_hat = decoder.decode_to_audio_44kHz(audio_list, output_path)

