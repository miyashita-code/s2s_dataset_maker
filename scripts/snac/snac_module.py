import torch
import soundfile as sf
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
