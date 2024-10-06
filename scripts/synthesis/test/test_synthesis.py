import os
import sys
import pytest
import pathlib

sys.path.insert(0, './')

from scripts.synthesis.style_bert_vits2_infer import VoiceSynthesizer

@pytest.fixture
def synthesizer():
    """
    Provides a VoiceSynthesizer instance for testing.
    """
    return VoiceSynthesizer(is_debug=True)

@pytest.fixture
def sample_text():
    """
    Provides sample text for testing.
    """
    return "これはテストです。音声合成が正しく動作するか確認します。"

@pytest.fixture
def save_path():
    """
    Provides a temporary path for saving synthesized audio.
    """
    return pathlib.Path("buffer/systhesis_test_outputs/output.wav")

class TestVoiceSynthesizer:
    """
    Test cases for the VoiceSynthesizer class.
    """

    def test_synthesize_with_model(self, synthesizer, sample_text, save_path):
        """
        Test synthesizing audio with a specified model and checking if the file is saved correctly.
        """
        synthesizer.synthesize(
            text=sample_text,
            save_path=str(save_path),
            model=list(synthesizer.models_name_map.keys())[0]
        )
        assert save_path.exists()
        os.remove(save_path)

    def test_synthesize_random_model(self, synthesizer, sample_text, save_path):
        """
        Test synthesizing audio with a random model and checking if the file is saved correctly.
        """
        synthesizer.synthesize(
            text=sample_text,
            save_path=str(save_path),
            is_random=True
        )
        assert save_path.exists()
        os.remove(save_path)

    def test_invalid_model(self, synthesizer, sample_text, save_path):
        """
        Test that a ValueError is raised when an invalid model is specified.
        """
        with pytest.raises(ValueError):
            synthesizer.synthesize(
                text=sample_text,
                save_path=str(save_path),
                model="invalid_model"
            )

    def test_long_text_split(self, synthesizer, save_path):
        """
        Test synthesizing long text that needs splitting and checking if the file is saved correctly.
        """
        long_text = "これは非常に長いテキストです。" * 30  # Over 100 characters
        synthesizer.synthesize(
            text=long_text,
            save_path=str(save_path)
        )
        assert save_path.exists()
        os.remove(save_path)

    def test_long_jp_text(self, synthesizer, save_path):
        """
        Test synthesizing long Japanese text and checking if the file is saved correctly.
        """
        long_text = """
            こんにちわ。
            私はオムニです。
            リアルタイムでの対話が得意なユニークな音声アシスタントです。
            質問への回答から複雑なソリューションの提供まで、
            幅広い言語タスクに対応できます。
            他のアシスタントモデルとは異なり、
            私は高度なハードウェアで訓練されており、
            音声を使った推論能力やタイムリーで正確な応答が強化されています。"""
        
        synthesizer.synthesize(
            text=long_text,
            save_path=str(save_path),
            model=list(synthesizer.models_name_map.keys())[3]
        )
        assert save_path.exists()
        #os.remove(save_path)

