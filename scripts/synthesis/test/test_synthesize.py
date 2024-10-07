import os
import sys
import io
import asyncio
from pydub import AudioSegment

from scripts.synthesis.style_bert_vits2_infer import VoiceSynthesizer
from scripts.utils.HF_dataset import DatasetModule

dataset_module = DatasetModule()
synthesizer = VoiceSynthesizer()

async def synthesize_audio(text, index):
    """音声合成を行う非同期関数"""
    output_dir = "output"  # 保存先のディレクトリ名
    os.makedirs(output_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

    save_path = os.path.join(output_dir, f"answer_output_{index}.wav")  # 保存先のパスを修正
    # テキストを音声合成する
    audio = synthesizer.synthesize(text, save_path,  "jvnv-M2-jp")
    return save_path  # 保存先のパスを返す

async def audio_maker():
    """音声合成を行うメイン関数"""

    filename = "answer_spoken.json"
    if not os.path.exists(filename):
        print(f"ファイルが存在しません: {filename}")
    else:
        print(f"ファイルが見つかりました: {filename}")

    # テキストを読み込む
    text_list = dataset_module.load_text_from_json(filename)

    # 非同期タスクを作成
    tasks = [synthesize_audio(text, i) for i, text in enumerate(text_list[:10])]
    
    # タスクを並列に実行
    results = await asyncio.gather(*tasks)

    print("音声合成が完了しました:", results)

# メインの非同期処理を実行
if __name__ == "__main__":
    asyncio.run(audio_maker())


        

