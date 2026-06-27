シンプルなサッカーシミュレーター

セットアップと実行方法

- 前提: Python 3.8+ と仮想環境を推奨します。

- 依存関係のインストール:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- 実行:

```bash
python main.py
```

コード整形

プロジェクト標準のフォーマッタとして `black` と `isort` を推奨します。環境にインストールしたら次を実行してください:

```bash
pip install black isort
black .
isort .
```

ファイル

- [README.md](README.md)
- [requirements.txt](requirements.txt)
- [pyproject.toml](pyproject.toml)

簡単な変更点/注意

- 画面描画時に座標を整数化しました（レンダリングの安定化）。
- 距離比較で `length_squared()` を使い、不要な平方根計算を避けています。
- 型注釈を追加して `mypy` 等の静的解析が使いやすくなっています。

さらにリファクタ希望があれば指示してください。

以上copilotが書いてくれました。
