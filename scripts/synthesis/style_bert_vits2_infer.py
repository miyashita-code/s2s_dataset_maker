import json
import os
import io
import random
import requests

from pydub import AudioSegment
from dotenv import load_dotenv


class VoiceSynthesizer:
    """
    A class to perform text-to-speech synthesis using the Style-Bert-VITS2 API.

    This class converts given text into speech and saves it to a specified path.
    It loads available models during initialization and allows selection of a specific
    model or a random model for synthesis. If the text exceeds 100 characters, it
    automatically splits the text before synthesis.
    """

    def __init__(self, is_debug: bool = False, silent_interval_ms: int = 300):
        """
        Initialize the VoiceSynthesizer.

        Loads the available models from 'model_list.json' and retrieves model information
        from the API. Also loads the base URL from environment variables.

        Args:
            is_debug (bool): Enable debug mode if True. Default is False.

        Raises:
            EnvironmentError: If the API base URL is not set in environment variables.
            Exception: If a specified model does not exist or the server is not ready.
        """
        self.is_debug = is_debug
        self.silent_interval_ms = silent_interval_ms
        # Load environment variables
        load_dotenv()

        # Get API base URL from environment variable
        base_url = os.getenv("STYLE_BERT_VITS2_API_LOCAL_URL")
        if base_url is None:
            raise EnvironmentError("Environment variable 'STYLE_BERT_VITS2_API_LOCAL_URL' is not set.")

        self.voice_synthesizer_url = f"{base_url}/voice"
        self.doc_url = f"{base_url}/docs"
        self.models_info_url = f"{base_url}/models/info"
        self.models_name_map = {}

        # Load model list from JSON file
        with open("scripts/synthesis/model_list.json", "r", encoding="utf-8") as f:
            model_names = json.load(f)["models"]
            self._debug_print(f"Available models: {model_names}")

        # Get model information from API
        model_infos = self._get_models_info()

        # Map model names to their IDs
        for model_name in model_names:
            model_id = self._find_model_id(model_infos, model_name)

            if model_id is None:
                raise Exception(f"Model '{model_name}' does not exist.")

            self._debug_print(f"Model '{model_name}' has ID: {model_id}")
            self.models_name_map[model_name] = model_id

        # Check if the server is ready
        self.check_server_ready()

    def synthesize(self, text: str, save_path: str, model: str = None, is_random: bool = False):
        """
        Synthesize speech from text and save it to a specified path.

        Args:
            text (str): The text to be synthesized.
            save_path (str): The file path where the synthesized audio will be saved.
            model (str, optional): The model name to use for synthesis. If not specified, the default model is used.
            is_random (bool, optional): If True, select a random model from available models.

        Raises:
            ValueError: If the specified model does not exist.
            Exception: If an error occurs during API calls.
        """
        self._debug_print(
            f"Synthesize called with text: '{text}', save_path: '{save_path}', model: '{model}', is_random: {is_random}"
        )

        # Select the model
        if model:
            if model not in self.models_name_map:
                raise ValueError(f"Model '{model}' does not exist.")
            selected_model = model
        elif is_random:
            selected_model = random.choice(list(self.models_name_map.keys()))
            self._debug_print(f"Randomly selected model: {selected_model}")
        else:
            selected_model = list(self.models_name_map.keys())[0]  # Default model
            self._debug_print(f"Using default model: {selected_model}")

        # Split text into segments if necessary
        segments = self._split_text(text)
        self._debug_print(f"Text segments: {segments}")

        # Synthesize each segment and collect audio data
        combined_audio = AudioSegment.empty()
        silent_segment = AudioSegment.silent(duration=self.silent_interval_ms)  # 無音
        for idx, segment in enumerate(segments):
            params = self._get_params(segment, self.models_name_map[selected_model])
            self._debug_print(f"API parameters: {params}")
            try:
                response = requests.get(self.voice_synthesizer_url, params=params)
                response.raise_for_status()
                audio_segment = AudioSegment.from_file(io.BytesIO(response.content), format="wav")
                combined_audio += audio_segment
                self._debug_print(f"Synthesized segment with length {len(response.content)} bytes")
                
                # 最後のセグメント以外には無音区間を追加
                if idx < len(segments) - 1:
                    combined_audio += silent_segment
                    self._debug_print(f"Inserted a {self.silent_interval_ms} mili second silent interval.")
            except requests.RequestException as e:
                raise Exception(f"API request failed: {e}")
            except Exception as e:
                raise Exception(f"Audio data processing failed: {e}")

        # Write the combined audio data to the output file
        combined_audio.export(save_path, format="wav")
        self._debug_print(f"Synthesized audio saved to '{save_path}'")

    def _get_models_info(self) -> dict:
        """
        Retrieve model information from the API.

        Returns:
            dict: A dictionary containing model information.

        Raises:
            Exception: If model information cannot be retrieved.
        """
        try:
            response = requests.get(self.models_info_url)
            response.raise_for_status()
            self._debug_print("Model information retrieved successfully")
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to retrieve model information: {e}")

    def _get_params(self, text: str, model_id: str) -> dict:
        """
        Generate parameters for the API call.

        Args:
            text (str): The text segment to synthesize.
            model_id (str): The ID of the model to use.

        Returns:
            dict: A dictionary of parameters for the API call.
        """
        params = {
            "text": text.replace(" ", "").replace("、", "、\n").replace("。", "。\n").replace(",", ",\n").replace(".", ".\n").replace(" ", " \n"),
            "model_id": model_id,
            "encoding": "utf-8",
            "speaker_id": 0,
            "sdp_ratio": 0.2,
            "noise": 0.5,
            "noisew": 0.6,
            "length": 1.05,
            "language": "JP",
            "auto_split": True,
            "split_interval": self.silent_interval_ms / 1000,
            "assist_text": "明るく好印象な感じでハキハキと話してください！怒った感じに聞こえないように注意してください！わくわくで幸せ！語尾をものすごく柔らかく優しく発声してください。",
            "assist_text_weight": 0.75,
            "style": "Neutral",
            "style_weight": 1
        }
        return params

    def _find_model_id(self, models_info: dict, model_name: str) -> str:
        """
        Find the model ID corresponding to a given model name.

        Args:
            models_info (dict): The dictionary containing models information.
            model_name (str): The name of the model to find.

        Returns:
            str: The model ID if found, else None.
        """
        for model_id, info in models_info.items():
            if model_name in info.get("spk2id", {}):
                return model_id
        return None

    def _split_text(self, text: str, max_length: int = 100) -> list:
        """
        Split text into segments not exceeding max_length characters.

        If no specified delimiters are found, the method will forcibly split at max_length.
        This ensures that all segments are within the max_length limit, handling potential errors.

        Args:
            text (str): The text to split.
            max_length (int): The maximum length of each text segment.

        Returns:
            list: A list of text segments.
        """
        delimiters = ["、", "。", ",", ".", " ", " "]
        segments = []
        while text:
            if len(text) <= max_length:
                segments.append(text)
                break
            
            split_index = max_length
            for delim in reversed(delimiters):
                index = text.rfind(delim, 0, max_length)
                if index != -1:
                    split_index = index + 1
                    break
            
            segments.append(text[:split_index])
            text = text[split_index:]
        
        return segments

    def _debug_print(self, message: str):
        """
        Print debug messages if debug mode is enabled.

        Args:
            message (str): The debug message to print.
        """
        if self.is_debug:
            print(f"[DEBUG] {message}")

    def check_server_ready(self):
        """
        Check if the API server is ready.

        Raises:
            Exception: If the server is not ready.
        """
        try:
            response = requests.get(self.doc_url)
            response.raise_for_status()
            self._debug_print("Server is ready.")
        except requests.RequestException as e:
            raise Exception(f"Server is not ready: {e}")

    def get_usable_models(self) -> list:
        """
        Get a list of usable models.

        Returns:
            list: A list of model names.
        """
        return list(self.models_name_map.keys())

