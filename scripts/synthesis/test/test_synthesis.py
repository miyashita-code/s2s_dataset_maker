import os
import sys

import pytest

sys.path.insert(0, './')

from scripts.synthesis.style_bert_vits2_infer import VoiceSynthesizer

@pytest.fixture
def synthesizer():
    """
    テスト用のVoiceSynthesizerインスタンスを提供するフィクスチャ。
    """
    return VoiceSynthesizer(is_debug=True)

@pytest.fixture
def sample_text():
    """
    テスト用のサンプルテキストを提供するフィクスチャ。
    """
    return "これはテストです。音声合成が正しく動作するか確認します。"

@pytest.fixture
def save_path(tmp_path):
    """
    テスト用の一時保存パスを提供するフィクスチャ。
    """
    return tmp_path / "test_output.wav"

def test_synthesize_with_model(synthesizer, sample_text, save_path):
    """
    指定したモデルで音声合成を行い、ファイルが正しく保存されるかをテストする。
    """
    synthesizer.synthesize(sample_text, str(save_path), model=list(synthesizer.models_name_map.keys())[0])
    assert save_path.exists()
    os.remove(save_path)

def test_synthesize_random_model(synthesizer, sample_text, save_path):
    """
    ランダムに選択されたモデルで音声合成を行い、ファイルが正しく保存されるかをテストする。
    """
    synthesizer.synthesize(sample_text, str(save_path), isRandom=True)
    assert save_path.exists()
    os.remove(save_path)

def test_invalid_model(synthesizer, sample_text, save_path):
    """
    存在しないモデルを指定した場合にValueErrorが発生することをテストする。
    """
    with pytest.raises(ValueError):
        synthesizer.synthesize(sample_text, str(save_path), model="invalid_model")

def test_long_text_split(synthesizer, save_path):
    """
    長いテキストを分割して合成し、ファイルが正しく保存されるかをテストする。
    """
    long_text = "これは非常に長いテキストです。" * 30  # 100文字以上
    synthesizer.synthesize(long_text, str(save_path))
    assert save_path.exists()
    os.remove(save_path)
