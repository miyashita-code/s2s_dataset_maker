import os
from scripts.snac.snac_module import SNACDecoder
from scripts.utils.HF_dataset import DatasetHandler

import pytest

# HuggingFaceからデータセットをロードする。
dataset = DatasetHandler.load_dataset("gpt-omni/VoiceAssistant-400k", split="train")

# データセットから「identity」のデータを抽出する。
filtered_dataset = DatasetHandler.filter_dataset(dataset, "identity")

# データセットから「SNACトークン」のデータを抽出する。
snac_tokens = DatasetHandler.extract_snac_tokens(filtered_dataset)

@pytest.fixture
def decoder():
    """SNACDecoderのインスタンスを提供するフィクスチャ"""
    return SNACDecoder()

def test_decode_to_audio(decoder):
    """
    デコーダーを使用してSNACトークンを音声ファイルにデコードするテスト。
    """
    # SNACトークンを解析
    parsed_snac_tokens = decoder.parse_snac_tokens(snac_tokens[0])  # 最初のトークンを使用

    # 音声ファイルを出力するパス
    output_path = "output.wav"

    # デコードを実行
    decoder.decode_to_audio(parsed_snac_tokens, output_path)

    # 出力ファイルが生成されたかを確認
    assert os.path.exists(output_path), "出力ファイルが生成されていません。"

if __name__ == "__main__":
    pytest.main()