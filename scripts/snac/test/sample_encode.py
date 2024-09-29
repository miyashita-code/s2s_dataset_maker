import torch
import torchaudio
from snac import SNAC
from scripts.utils.snac_utils import log_device_info

# デバイスの準備
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
log_device_info(device)
# モデルの準備
model = SNAC.from_pretrained("hubertsiuzdak/snac_44khz").eval().to(device)

# 読み込みたい音声ファイルのパスを指定
audio_path = "data/test_input_audio2.wav"  # 例: 読み込む音声ファイルのパス
output_path = "data/test_output_hat.wav"  # 例: 保存する音声ファイルのパス

# 音声ファイルを読み込み
waveform, sample_rate = torchaudio.load(audio_path)

waveform = waveform.unsqueeze(0).to(device)  # バッチ次元を追加してGPUに転送

# モデルを使用してエンコードとデコード
with torch.inference_mode():
    codes = model.encode(waveform)
    audio_hat = model.decode(codes)

# デコードされた音声を保存
# (音声データをCPUに戻して保存)
torchaudio.save(output_path, audio_hat.squeeze(0).cpu(), sample_rate)
print(f"Decoded audio saved to: {output_path}")
