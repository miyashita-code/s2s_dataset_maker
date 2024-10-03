import pytest
import torchaudio
from scripts.snac.snac_module import SNACDecoder, SNACEncoder

@pytest.fixture
def setup_encoder_decoder():
    encoder = SNACEncoder()
    decoder = SNACDecoder()
    return encoder, decoder

def test_encode_to_tokens(setup_encoder_decoder):
    encoder, _ = setup_encoder_decoder
    audio_path = "data/test_input_audio.wav"
    
    # 音声ファイルをエンコード
    tokens = encoder.encode_to_tokens(audio_path)
    
    # トークンが空でないことを確認
    assert tokens is not None
    assert len(tokens) > 0

def test_make_snac_tokens(setup_encoder_decoder):
    encoder, _ = setup_encoder_decoder
    audio_path = "data/test_input_audio.wav"
    
    # 音声ファイルをエンコード
    tokens = encoder.encode_to_tokens(audio_path)
    snac_tokens = encoder.make_snac_tokens(tokens)
    
    # SNACトークンが空でないことを確認
    assert snac_tokens is not None
    assert len(snac_tokens) > 0

def test_decode_to_audio_44kHz(setup_encoder_decoder):
    _, decoder = setup_encoder_decoder
    audio_path = "data/test_input_audio.wav"
    output_path = "data/test_output_hat.wav"
    
    # エンコーダーを使用してトークンを取得
    encoder = SNACEncoder()
    tokens = encoder.encode_to_tokens(audio_path)
    snac_tokens = encoder.make_snac_tokens(tokens)
    
    # トークンをデコード
    audio_list = decoder.parse_snac_tokens(snac_tokens)
    decoder.decode_to_audio_44kHz(audio_list, output_path)
    
    # 出力ファイルが生成されたことを確認
    assert torchaudio.load(output_path)[0].size(0) > 0  # 音声データが存在することを確認