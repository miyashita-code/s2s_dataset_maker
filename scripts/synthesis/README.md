# Style-Bert-VITS2 環境のセットアップと使用方法

このドキュメントでは、Style-Bert-VITS2環境のセットアップ手順と使用方法について説明します。

## 環境セットアップ

[Style-Bert-VITS2のリポジトリ](https://github.com/litagin02/Style-Bert-VITS2?tab=readme-ov-file)に従って、環境をセットアップします。

## APIサーバーの起動

Style-Bert-VITS2環境で以下のコマンドを実行して、APIサーバーを起動します。

### Pythonを使用する場合
```sh
python server_fastapi.py
```

### 実行ファイルを使用する場合
```sh
./Server.exe
```

## 音声合成の方法

以下の手順で音声合成を行います。

1. `VoiceSynthesizer`クラスのインスタンスを作成します。
    ```python
    synthesizer = VoiceSynthesizer()
    ```

2. `synthesize`メソッドを使用して音声を合成します。以下はその例です。
    ```python
    text = "こんにちは、世界！"
    save_path = "output.wav"
    audio = synthesizer.synthesize(text, save_path)
    ```

    `synthesize`メソッドの引数は以下の通りです：
    - `text` (str): 合成するテキスト。
    - `save_path` (str): 合成された音声ファイルの保存先パス。
    - `model` (str, optional): 使用するモデルの名前。指定がない場合はデフォルトモデルを使用。
    - `isRandom` (bool, optional): Trueの場合、利用可能なモデルからランダムに選択します。

    例：
    ```python
    audio = synthesizer.synthesize(text, save_path, model="female", isRandom=True)
    ```

3. 合成された音声を保存する場合は、以下のようにします。
    ```python
    with open(save_path, "wb") as f:
        f.write(audio)
    ```

これで、指定したテキストから音声を合成し、ファイルに保存することができます。

## テスト

テストは以下のコマンドで行うことができます。
```sh
pytest -s scripts/synthesis/test/test_synthesis.py
```
