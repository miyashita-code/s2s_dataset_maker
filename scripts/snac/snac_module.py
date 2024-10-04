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

    def __init__(self):
        """
        クラスの初期化メソッド。

        Args:
            model_name (str, optional): 使用するSNACモデルの名前。デフォルトは "hubertsiuzdak/snac_24khz"。
        """
        self.model_name = "hubertsiuzdak/snac_44khz"
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

    def decode_to_audio_44kHz(self, snac_tokens: list, output_path: str) -> None:
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
            44100,
        )

        print(f"音声データを{output_path}に保存しました。")
    
    def decode_to_audio_24kHz(self, snac_tokens: list, output_path: str) -> None:
        """
        SNACトークンを音声データにデコードし、ファイルに保存する。

        Args:
            snac_tokens (list): デコードするSNACトークンのリスト。
            output_path (str): 出力する音声ファイルのパス。
        """

        snacmodel = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval().to(self.device)
        # SNACトークンから音声データを生成する
        audio_hat = generate_audio_data(snac_tokens, snacmodel, self.device)

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

    def __init__(self):
        """
        初期化メソッド。

        :param audio_path: 読み込む音声ファイルのパス
        :param output_path: 出力する音声ファイルのパス
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SNAC.from_pretrained("hubertsiuzdak/snac_44khz").eval().to(self.device)

    def encode_to_tokens(self, audio_path: str):
        """
        音声ファイルを処理し、エンコードを行うメソッド。
        """
        # 音声ファイルを読み込み
        waveform, sample_rate = torchaudio.load(audio_path)
        waveform = waveform.unsqueeze(0).to(self.device)  # バッチ次元を追加してGPUに転送
        log_device_info(self.device)


        # モデルを使用してエンコード
        with torch.inference_mode():
            tokens = self.model.encode(waveform)
        
        return tokens
    
    # テンソルのリストを一つの文字列に変換する関数
    def make_snac_tokens(self, tensor_list:list):
        """
        音声からエンコードされたトークンを、データセット用に再構築するメソッド
        """
        flattened_output = []

        # 各テンソルから値を取り出してリストに格納
        tensor1_values = tensor_list[0].cpu().tolist()[0]  # 28個の要素
        tensor2_values = tensor_list[1].cpu().tolist()[0]  # 56個の要素
        tensor3_values = tensor_list[2].cpu().tolist()[0]  # 112個の要素
        tensor4_values = tensor_list[3].cpu().tolist()[0]  # 224個の要素

        idx_t1 = 0
        idx_t2 = 0
        idx_t3 = 0
        idx_t4 = 0

        max_iterations = 28  # ループ回数を28回に設定

        for _ in range(max_iterations):
            flattened_output.extend([
                '#',
                str(tensor1_values[idx_t1]),
                str(tensor2_values[idx_t2]),
                str(tensor3_values[idx_t3]),
                str(tensor4_values[idx_t4]),
                str(tensor4_values[idx_t4 + 1]),
                str(tensor3_values[idx_t3 + 1]),
                str(tensor4_values[idx_t4 + 2]),
                str(tensor4_values[idx_t4 + 3]),
                str(tensor2_values[idx_t2 + 1]),
                str(tensor3_values[idx_t3 + 2]),
                str(tensor4_values[idx_t4 + 4]),
                str(tensor4_values[idx_t4 + 5]),
                str(tensor3_values[idx_t3 + 3]),
                str(tensor4_values[idx_t4 + 6]),
                str(tensor4_values[idx_t4 + 7]),
            ])

            idx_t1 += 1
            idx_t2 += 2
            idx_t3 += 4
            idx_t4 += 8

        # flattened_outputリストをスペースで区切って1つの文字列に変換
        result_string = ' '.join(flattened_output)
        return result_string