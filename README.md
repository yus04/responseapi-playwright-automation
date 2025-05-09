# responseapi-playwright-automation

こちらのリポジトリのコードは [Microsoft の公式ドキュメント](https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/responses?tabs=python-secure) をベースに書いています。公式ドキュメントに載っているコードは [こちら](document/main.py) から確認できます。

また、画面操作用のサンプルアプリは別途 [こちらのリポジトリ](https://github.com/yus04/contract-application-form) で用意しています。

# ローカルでの実行

.env.sample を参考にして .env を作成したのち以下の手順に従って下さい。

仮想環境を作成
```
python -m venv .venv
```

仮想環境を有効化
```
source .venv/bin/activate
```

必要な Python ライブラリのインストール
```
pip install -r requirements.txt
```

メディアや画面描画などに必要なライブラリのインストール
```
sudo apt update && sudo apt install -y \
  libgtk-4-1 \
  libgraphene-1.0-0 \
  libxslt1.1 \
  libwoff1 \
  libvpx7 \
  libopus0 \
  libgstreamer-plugins-base1.0-0 \
  libgstreamer-plugins-good1.0-0 \
  libgstreamer-gl1.0-0 \
  libgstreamer-plugins-bad1.0-0 \
  libflite1 \
  libwebpdemux2 \
  libavif13 \
  libharfbuzz-icu0 \
  libwebpmux3 \
  libenchant-2-2 \
  libhyphen0 \
  libmanette-0.2-0 \
  libgles2-mesa \
  libx264-dev \
  fonts-noto-cjk
```

画面操作用ライブラリのインストール
```
playwright install
```

アプリの実行
```
python main.py
```

上記コマンドを実行後、`Enter a task to perform (or 'exit' to quit):` と表示されるのでタスクを入力して Enter を押す。

# トラブルシューティング

> openai.AuthenticationError: Error code: 401 - {'error': {'code': 'PermissionDenied', 'message': 'The principal `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` lacks the required data action `Microsoft.CognitiveServices/accounts/OpenAI/responses/write` to perform `POST /openai/responses` operation.'}}
上記のエラーが出た場合は自身のプリンシパルに Cognitive Services OpenAI User ロールを付与してください。