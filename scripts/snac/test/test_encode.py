import os
import pytest
from scripts.snac.snac_module import SNACEncoder

# テスト用の音声ファイルのパス
AUDIO_PATH = "data/test_input_audio2.wav"
OUTPUT_PATH = "data/test_output_tokens.wav"

@pytest.fixture
def encoder():
    """SNACEncoderのインスタンスを提供するフィクスチャ"""
    return SNACEncoder(AUDIO_PATH, OUTPUT_PATH)

def test_encode_and_decode(encoder):
    """
    音声ファイルをSNACトークンにエンコードし、デコードするテスト。
    """
    # 音声ファイルをトークンにエンコード
    tokens = encoder.encode_to_tokens()
    assert tokens is not None, "トークンが生成されていません。"

    # トークンを音声データにデコード
    encoder.decode_from_tokens(tokens)

    # 出力ファイルが生成されたかを確認
    assert os.path.exists(OUTPUT_PATH), "出力ファイルが生成されていません。"

if __name__ == "__main__":
    pytest.main()