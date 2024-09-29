import torch
import soundfile as sf
import torchaudio
from snac import SNAC
from scripts.utils.snac_utils import generate_audio_data, log_device_info


class SNACDecoder:
    """
    SNACトークンを音声データにデコードするクラス。

    このクラスは、提供されたSNACトークンリストを使用して、
    音声データを生成し、指定されたパスに保存します。
    """

    def __init__(self, model_name: str = "hubertsiuzdak/snac_24khz"):
        """
        クラスの初期化メソッド。

        Args:
            model_name (str, optional): 使用するSNACモデルの名前。デフォルトは "hubertsiuzdak/snac_24khz"。
        """
        self.model_name = model_name
        self.device = self._setup_device()
        self.snac_model = self._load_model()

    def _setup_device(self) -> torch.device:
        """
        使用可能なデバイスを設定する。

        GPUが利用可能であればCUDAを、それ以外の場合はCPUを使用する。

        Returns:
            torch.device: 設定されたデバイス。
        """
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        log_device_info(device)
        return device

    def _load_model(self) -> SNAC:
        """
        事前学習済みのSNACモデルをロードする。

        Returns:
            SNAC: ロードされたSNACモデル。
        """
        model = SNAC.from_pretrained(self.model_name).eval().to(self.device)
        return model

    def parse_snac_tokens(self, input_str: str) -> list:
        """
        SNACトークンの文字列を解析し、リストに分割する。

        Args:
            input_str (str): SNACトークンの文字列。

        Returns:
            list: 分割されたSNACトークンのリスト。
        """
        return input_str.split(" ")

    def decode_to_audio(self, snac_tokens: list, output_path: str) -> None:
        """
        SNACトークンを音声データにデコードし、ファイルに保存する。

        Args:
            snac_tokens (list): デコードするSNACトークンのリスト。
            output_path (str): 出力する音声ファイルのパス。
        """
        # SNACトークンから音声データを生成する
        audio_hat = generate_audio_data(snac_tokens, self.snac_model, self.device)

        # 生成された音声データをファイルに保存する
        sf.write(
            output_path,
            audio_hat.squeeze().cpu().numpy(),
            24000,
        )

        print(f"音声データを{output_path}に保存しました。")

class SNACEncoder:
    """
    音声ファイルをSNACトークンにエンコードするクラス。
    """

    def __init__(self, audio_path: str, output_path: str):
        """
        初期化メソッド。

        :param audio_path: 読み込む音声ファイルのパス
        :param output_path: 出力する音声ファイルのパス
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SNAC.from_pretrained("hubertsiuzdak/snac_44khz").eval().to(self.device)
        self.audio_path = audio_path
        self.output_path = output_path

    def encode_to_tokens(self):
        """
        音声ファイルを処理し、エンコードおよびデコードを行うメソッド。
        """
        # 音声ファイルを読み込み
        waveform, sample_rate = torchaudio.load(self.audio_path)
        waveform = waveform.unsqueeze(0).to(self.device)  # バッチ次元を追加してGPUに転送

        # モデルを使用してエンコード
        with torch.inference_mode():
            tokens = self.model.encode(waveform)
        
        return tokens

    def decode_from_tokens(self, tokens):
        """
        トークンを音声データにデコードする。
        """
        with torch.inference_mode():
            audio_hat = self.model.decode(tokens)

        # 生成された音声データをファイルに保存する
        sf.write(
            self.output_path,
            audio_hat.squeeze().cpu().numpy(),
            44100,
        )

        print(f"音声データを{self.output_path}に保存しました。")