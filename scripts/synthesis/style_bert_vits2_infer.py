import json
import random
import requests
import os

import dotenv

class VoiceSynthesizer:
    """
    音声合成を行うためのクラス。

    このクラスは、指定されたテキストを音声に変換し、指定されたパスに保存します。
    使用するモデルは、初期化時に読み込まれ、指定のモデルまたはランダムに選択されます。
    テキストが100文字を超える場合、自動的に分割して合成します。
    """

    def __init__(self, is_debug: bool = False):
        """
        VoiceSynthesizerの初期化メソッド。

        - `model_list.json`から利用可能なモデルを読み込みます。
        - 環境変数からAPIのベースURLを取得します。
        """
        self.is_debug = is_debug

        # 環境変数の読み込み
        dotenv.load_dotenv()

        # 環境変数からAPIのベースURLを取得
        self.url = os.getenv("STYLE_BERT_VITS2_API_LOCAL_URL")
        self.voice_synthesizer_url = self.url + "/voice"
        self.doc_url = self.url + "/docs"
        self.models_info_url = self.url + "/models/info"
        self.models_name_map = {}

        # モデルリストの読み込み
        with open("scripts/synthesis/model_list.json", "r", encoding="utf-8") as f:
            model_names = json.load(f)["models"]
            self._debug_print(f"<VoiceSynthesizer.__init__> models: {model_names}")

            model_infos = self.__get_models_info()

            for model_name in model_names:
                model_id = self.__find_model_id(model_infos, model_name)

                if model_id is None:
                    raise Exception(f"モデル '{model_name}' が存在しません。")

                self._debug_print(f"<VoiceSynthesizer.__init__> model_id: {model_id}")
                self.models_name_map[model_name] = model_id

        self.check_is_server_ready()

    def synthesize(self, text: str, save_path: str, model: str = None, isRandom: bool = False):
        """
        テキストを音声に合成し、指定されたパスに保存します。

        Args:
            text (str): 読み上げ対象のテキスト。
            save_path (str): 合成された音声ファイルの保存先パス。
            model (str, optional): 使用するモデルの名前。指定がない場合はデフォルトモデルを使用。
            isRandom (bool, optional): Trueの場合、利用可能なモデルからランダムに選択します。

        Raises:
            ValueError: 指定されたモデルが存在しない場合。
            Exception: API呼び出し時にエラーが発生した場合。
        """
        self._debug_print(f"<VoiceSynthesizer.synthesize> called, text: {text}, save_path: {save_path}, model: {model}, isRandom: {isRandom}")

        # モデルの選択
        if model:
            if model not in self.models_name_map:
                raise ValueError(f"モデル '{model}' が存在しません。")
            selected_model = model
        elif isRandom:
            selected_model = random.choice(list(self.models_name_map.keys()))
        else:
            selected_model = list(self.models_name_map.keys())[0]  # デフォルトモデル

        # テキストの分割
        segments = self._split_text(text)

        # 音声合成と保存
        audio_segments = []
        for segment in segments:
            params = self._get_params(segment, self.models_name_map[selected_model])
            response = requests.get(self.voice_synthesizer_url, params=params)
            if response.status_code == 200:
                audio_segments.append(response.content)
            else:
                raise Exception(f"APIエラー: ステータスコード {response.status_code}")

        # 音声ファイルの結合と保存
        with open(save_path, "wb") as f:
            for audio in audio_segments:
                f.write(audio)
        print(f"音声ファイルを '{save_path}' に保存しました。")
    
    def __get_models_info(self):
        """
        モデルの情報を取得します。
        """
        response = requests.get(self.models_info_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"モデル情報の取得に失敗しました。ステータスコード: {response.status_code}")

    def _get_params(self, text: str, model_id: str):
        """
        API呼び出しに使用するパラメータを生成します。

        Args:
            text (str): 合成するテキストのセグメント。
            model_id (str): 使用するモデルのID。

        Returns:
            dict: API呼び出しに必要なパラメータの辞書。
        """
        return {
            "text": text,
            "model_id": model_id,
            "encoding": "utf-8",
            "speaker_id": 0,
            "sdp_ratio": 0.2,
            "noise": 0.5,
            "noisew": 0.7,
            "length": 1.0,
            "language": "JP",
            "auto_split": False,
            "assist_text": "",
            "assist_text_weight": 1,
            "style": "Neutral",
            "style_weight": 5
        }
    
    def __find_model_id(self, data, model_name):
        """
        data = {
            `${model_id}` : {
                "spk2id" : {
                    `${model_name}` : 0
                }
            },
            ...
        }
        
        """
        # Iterate through the JSON data
        for key, value in data.items():
            # Check if the model_name exists in the "spk2id" keys
            if model_name in value.get("spk2id", {}):
                return key
        return None

    def _split_text(self, text: str, max_length: int = 100):
        """
        テキストを指定された最大長さ以下に分割します。

        分割は、指定された区切り文字（「、」「。」「,」「.」「 」など）の最大インデックスで行います。
        区切り文字が見つからない場合は、単純に指定された長さで分割します。

        Args:
            text (str): 分割対象のテキスト。
            max_length (int, optional): 各セグメントの最大文字数。デフォルトは100。

        Returns:
            list: 分割されたテキストセグメントのリスト。
        """
        delimiters = ["、", "。", ",", ".", " ", "　"]
        segments = []
        while len(text) > max_length:
            for delim in reversed(delimiters):
                index = text.rfind(delim, 0, max_length)
                if index != -1:
                    segments.append(text[:index+1])
                    text = text[index+1:]
                    break
            else:
                segments.append(text[:max_length])
                text = text[max_length:]
        if text:
            segments.append(text)
        return segments
    
    def _debug_print(self, message: str):
        if self.is_debug:
            print(message)

    def check_is_server_ready(self):
        """
        サーバーが準備されているかを確認します。
        """
        response = requests.get(self.doc_url)
        if response.status_code != 200:
            raise Exception(f"サーバーが準備されていません。ステータスコード: {response.status_code}")
        
        self._debug_print(f"<VoiceSynthesizer.check_is_server_ready> called, response: {response}")

    def get_usable_models(self):
        """
        使用可能なモデルのリストを取得します。
        """
        return list(self.models_name_map.keys())

