from scripts.translation.translator import Translator, JSONWriter
from scripts.snac.snac_module import SNACEncoder, SNACDecoder
from scripts.synthesis.style_bert_vits2_infer import VoiceSynthesizer
from scripts.utils.HF_dataset import DatasetModule

import os
import asyncio
from dotenv import load_dotenv

class Dataset:

    def __init__(self) -> None:
        # 環境変数の読み込み
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        #必要なインスタンスの初期化
        self.translator = Translator(api_key)
        self.jsonwriter = JSONWriter()
        self.dataset_module = DatasetModule()
        self.synthesizer = VoiceSynthesizer()
        self.encoder = SNACEncoder()
        self.decoder = SNACDecoder()

    async def translate_texts(self, texts, filename):
        """
        テキストの翻訳を行う共通メソッド
        """
        translated_text = await self.translator.batch_translate_en2ja(texts, max_size=10)
        #await asyncio.sleep(5)
        speech_text = await self.translator.batch_translate_text2spoken_with_filler(translated_text, max_size=10)
        #await asyncio.sleep(10)
        results = JSONWriter.write_to_json(speech_text, filename=filename)
        print(f"{filename}の書き込みが完了しました。")
        return results

    async def translation(self):
        """
        データセットの "question" と "answer を作成します
        """

        # データセットの読み込み
        dataset = self.dataset_module.load_dataset("gpt-omni/VoiceAssistant-400k")
        filter_dataset = self.dataset_module.filter_dataset(dataset, "identity")

        async def translate_question():
            #データセットの読み込む
            questions = self.dataset_module.extract_questions(filter_dataset[1200:1500])

            return await self.translate_texts(questions, filename="dataset_questions.json")

        async def translate_answer():
            #データセットの読み込む
            answers = self.dataset_module.extract_answers(filter_dataset[1200:1500])

            return await self.translate_texts(answers, filename="dataset_answers.json")
    
        await translate_question()
        print("質問テキストを翻訳しました")
        await translate_answer()
        print("回答テキストを翻訳しました")
        
    async def audio_maker(self, filename):
        async def synthesize_audio(text, index, audio_paths):
            """
            音声合成を行う非同期関数
            """
            output_dir = "output"  # 保存先のディレクトリ名
            os.makedirs(output_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

            save_path = os.path.join(output_dir, f"answer_output_{index}.wav")  # 保存先のパスを修正
            # テキストを音声合成する
            self.synthesizer.synthesize(text, save_path,  "jvnv-M2-jp")
            return save_path  # 保存先のパスを返す

        async def make_audio(filename: str):
            """
            音声合成を行うメイン関数

            filename = 音声合成したい日本語テキストのJSONファイル
            """
            if not os.path.exists(filename):
                print(f"ファイルが存在しません: {filename}")
            else:
                print(f"ファイルが見つかりました: {filename}")

            # 音声ファイルのパスを格納するリスト
            audio_paths = []

            # テキストを読み込む
            text_list = self.dataset_module.load_text_from_json(filename)

            # 非同期タスクを作成
            tasks = [synthesize_audio(text, i, audio_paths) for i, text in enumerate(text_list)]
            
            # タスクを並列に実行
            results = await asyncio.gather(*tasks)

            #音声ファイルのパスをリストとしてJSONファイルに出力
            self.jsonwriter.write_to_json(audio_paths, "audio_path.json")

            return results
            
         # make_audioを呼び出す
        await make_audio(filename)

    def snac_encode(self):
        """
        データセットの "answer_snac"を作成する
        """
        # 読み込みたい音声ファイルのパスを指定
        audio_path = "output/answer_output_1.wav"  # 例: 読み込む音声ファイルのパス
        output_path = "data/decoded_1.wav"  # 例: 保存する音声ファイルのパス

        #音声ファイルを渡してトークンにデコード
        tokens = self.encoder.encode_to_tokens(audio_path)
        snac_tokens = self.encoder.make_snac_tokens(tokens)
        print("snac_tokens is", snac_tokens)

        #snac_tokensをJSONファイルに保存する

        """
        データセットの "answer_audio"を作成する
        """
        audio_list = self.decoder.parse_snac_tokens(snac_tokens)

        #トークンと出力先を渡して音声にデコードする
        audio_hat = self.decoder.decode_to_audio_44kHz(audio_list, output_path)