
# Cosmic Canvas / コズミック・キャンバス

This is a multiplayer web game where players collaboratively create a universe from scratch.

これは、プレイヤーが協力してゼロから宇宙を創造するマルチプレイヤーウェブゲームです。

---

## 遊び方 (Japanese Guide)

### 概要

「コズミック・キャンバス」へようこそ！このゲームは、プレイヤー全員で協力し、「要素」を組み合わせて新しい「天体」や「概念」を創造していく、放置型オンラインゲームです。最終目標は、伝説の存在である「宇宙の意識」を誕生させることです。

### ゲームの始め方

1.  **サーバーの起動:**
    ターミナル（コマンドプロンプト）で以下のコマンドを実行して、ゲームサーバーを起動します。
    ```bash
    # 必要なライブラリをインストール (初回のみ)
    pip install Flask Flask-SocketIO eventlet

    # サーバーを起動
    python app.py
    ```
    *(お使いの環境によっては `python3 app.py` や `app.py` で起動する必要があるかもしれません)*

2.  **ゲームへのアクセス:**
    ウェブブラウザを開き、アドレスバーに `http://localhost:5000` と入力してアクセスします。

### 操作方法

1.  **要素を選ぶ:**
    画面の右側にある「Elements」リストから、組み合わせたい要素を**2つ**クリックします。選択した要素は青くハイライトされます。

2.  **組み合わせる:**
    2つ目の要素をクリックすると、組み合わせが自動的に実行されます。

3.  **発見する:**
    *   **成功:** 組み合わせが正しければ、新しい天体が中央のキャンバスに描画されたり、新しい概念が発見されたことが通知されます。発見された新しい要素は、全プレイヤーのリストに追加され、さらなる組み合わせに利用できます。
    *   **失敗:** 何も起こりません。選択を解除し、別の組み合わせを試してみましょう。

### 特徴

*   **協力プレイ:** 誰か一人が新しい要素を発見すると、その成果は全プレイヤーに共有されます。
*   **自動保存:** ゲームの進捗はサーバーに自動で保存されるため、いつでも中断・再開が可能です。

---

## How to Play (English Guide)

### Overview

Welcome to Cosmic Canvas! This is an incremental online game where all players collaborate to create new "celestial bodies" and "concepts" by combining "elements." The ultimate goal is to give birth to the legendary entity, the "Cosmic Consciousness."

### Getting Started

1.  **Start the Server:**
    Run the following commands in your terminal (or command prompt) to start the game server.
    ```bash
    # Install required libraries (only for the first time)
    pip install Flask Flask-SocketIO eventlet

    # Start the server
    python app.py
    ```
    *(Note: Depending on your environment, you might need to use `python3 app.py` or just `app.py`)*

2.  **Access the Game:**
    Open your web browser and navigate to `http://localhost:5000`.

### How to Play

1.  **Select Elements:**
    From the "Elements" list on the right side of the screen, click on **two** elements you want to combine. Selected elements will be highlighted in blue.

2.  **Combine:**
    When you click the second element, the combination is attempted automatically.

3.  **Discover:**
    *   **Success:** If the combination is valid, a new celestial body will be drawn on the central canvas, or a notification will announce the discovery of a new concept. The newly discovered element will be added to everyone's list for further combinations.
    *   **Failure:** Nothing will happen. Deselect the elements and try a different combination.

### Features

*   **Collaborative Play:** When one player discovers a new element, it is shared with all other players.
*   **Auto-Save:** The game's progress is automatically saved on the server, so you can stop and resume playing at any time.
