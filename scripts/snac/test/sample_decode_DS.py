from snac import SNAC
import torch
import torchaudio
import soundfile as sf

from scripts.utils.HF_dataset import DatasetHandler
from scripts.snac.snac_module import SNACDecoder

#デコーダーを初期化
decoder = SNACDecoder()

#データセット関係のクラスを初期化
dataset_class = DatasetHandler()

#データセットからSNACトークンを取得
dataset = dataset_class.load_dataset("gpt-omni/VoiceAssistant-400k")
#データセットから「identity」がsplit_nameのものを抽出
filterd_dataset = dataset_class.filter_dataset(dataset, "identity")
#さらに「snac_toknes」の列のみを抽出
snac_token_list = dataset_class.extract_snac_tokens(dataset)

#データセットから取得したトークンを調整
audio_list = decoder.parse_snac_tokens(snac_token_list[0])
#トークンと出力パスを渡してデコード（英語の音声は24kHz）
decoder.decode_to_audio_24kHz(audio_list, "output.wav")

