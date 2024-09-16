# s2s_dataset_maker
Speech to Speechの日本語のデータセットを作成するツールです。音声合成にはStyle-Bert-VITS2を使用します。基本的には、VoiceAssistant-400Kの翻訳とITOコーパスベースのデータセットを作成します。

## セットアップ手順

### Windowsの場合

1. リポジトリをクローンします。
    ```sh
    git clone https://github.com/miyashita-code/s2s_dataset_maker.git
    cd s2s_dataset_maker
    ```

2. `pyenv-win`をインストールします。
    ```sh
    choco install pyenv-win
    ```

3. Python 3.10.0をインストールし、グローバルに設定します。
    ```sh
    pyenv install 3.10.0
    pyenv global 3.10.0
    python -V
    # Python 3.10.0
    ```

4. 仮想環境を作成し、アクティベートします。
    ```sh
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

5. 必要なパッケージをインストールします。
    ```sh
    pip install -r requirements.txt
    ```

### MacOS/Linuxの場合

1. リポジトリをクローンします。
    ```sh
    git clone https://github.com/miyashita-code/s2s_dataset_maker.git
    cd s2s_dataset_maker
    ```

2. `pyenv`をインストールします。
    ```sh
    curl https://pyenv.run | bash
    ```

3. 必要な環境変数を設定します。
    ```sh
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ```

4. Python 3.10.0をインストールし、グローバルに設定します。
    ```sh
    pyenv install 3.10.0
    pyenv global 3.10.0
    python -V
    # Python 3.10.0
    ```

5. 仮想環境を作成し、アクティベートします。
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

6. 必要なパッケージをインストールします。
    ```sh
    pip install -r requirements.txt
    ```

## 使用方法

1. データセットの作成を開始します。
    ```sh
    python main.py
    ```

2. 詳細なオプションについては、以下のコマンドを実行して確認してください。
    ```sh
    python main.py --help
    ```

## 注意事項

- Windows環境でのセットアップ手順を記載していますが、MacOSやLinuxでも動作します。適宜コマンドを変更してください。
- `pyenv-win`のインストールにはChocolatey或いはpipが必要です。事前にインストールしておいてください。
- 仮想環境をアクティベートする際、PowerShellの実行ポリシーが制限されている場合があります。その場合は、以下のコマンドを実行してポリシーを変更してください。
    ```sh
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
- このREADMEは, GPT-4oを使用して作成されました。

## Reference
- ITA Corpus: https://github.com/mmorise/ita-corpus
- VoiceAssistant-400K: https://huggingface.co/datasets/gpt-omni/VoiceAssistant-400K
- Style-Bert-VITS2: https://github.com/litagin02/Style-Bert-VITS2
