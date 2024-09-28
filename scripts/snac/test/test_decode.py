from scripts.snac.snac_module import SNACDecoder
from scripts.utils.HF_dataset import DatasetHandler

#HuggingFaceからデータセットをロードする。
dataset = DatasetHandler.load_dataset("gpt-omni/VoiceAssistant-400k", split="train")

#データセットから「identity」のデータを抽出する。
filtered_dataset = DatasetHandler.filter_dataset(dataset, "identity")

#データセットから「SNACトークン」のデータを抽出する。
snac_tokens = DatasetHandler.extract_snac_tokens(filtered_dataset)

def main():
    """
    デコーダーを使用してSNACトークンを音声ファイルにデコードする例。
    """
    # デコーダーを初期化
    decoder = SNACDecoder()

    parsed_snac_tokens = decoder.parse_snac_tokens(snac_tokens)

    # 音声ファイルを出力するパス
    output_path = "output.wav"

    # デコードを実行
    decoder.decode_to_audio(parsed_snac_tokens, output_path)

if __name__ == "__main__":
    main()