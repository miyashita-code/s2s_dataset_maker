import os
import sys
import pytest

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
def save_path(tmp_path):
    """
    Provides a temporary path for saving synthesized audio.
    """
    return tmp_path / "test_output.wav"

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
