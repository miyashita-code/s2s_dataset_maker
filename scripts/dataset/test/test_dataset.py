import asyncio
from scripts.dataset.dataset_maker import Dataset

async def main():
    dataset = Dataset()

    # 翻訳を実行
    await dataset.translation()

    """
    #音声合成を実行する場合は、音声合成したいテキストのJSONファイル名を指定
    audio_filename = "dataset_answers.json"
    await dataset.audio_maker(audio_filename)

    # SNACエンコードを実行する場合は、音声ファイルのパスを指定
    audio_files = ["output/answer_output_0.wav", "output/answer_output_1.wav"]  # 必要に応じてファイル名を変更
    await dataset.snac_encode(audio_files)
    """

if __name__ == "__main__":
    asyncio.run(main())