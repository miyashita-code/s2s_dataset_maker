from snac import SNAC
from scripts.utils.snac_utils import reconstruct_snac, reconstruct_tensors, generate_audio_data, log_device_info
from scripts.utils.HF_dataset import DatasetHandler
import torch
import torchaudio

import soundfile as sf

def parse_snac_tokens(input_str):    
    return input_str.split(" ")

#HuggingFaceからデータセットをロードする。
dataset = DatasetHandler.load_dataset("gpt-omni/VoiceAssistant-400k", split="train")

#データセットから「identity」のデータを抽出する。
filtered_dataset = DatasetHandler.filter_dataset(dataset, "identity")

#データセットから「SNACトークン」のデータを抽出する。
snac_tokens = DatasetHandler.extract_snac_tokens(filtered_dataset)

#SNACトークンをデコードように調整する
snac_token_list = parse_snac_tokens(snac_tokens[0])

# デバイスの指定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
log_device_info(device)

#SNACトークンから音声にデコードする
snacmodel = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(device)

#audiolist = reconstruct_snac(snac_tokens)
audio_hat = generate_audio_data(snac_token_list, snacmodel, device)

sf.write(
    f"output.wav",
    audio_hat.squeeze().cpu().numpy(),
    24000,
)

print("音声データを出力しました。： output.wav")


