import requests
import json
import pyaudio
import time

def say(text):
    start_time = time.time()

    # エンジン起動時に表示されているIP、portを指定
    host = "127.0.0.1"
    port = 50021

    # 音声化する文言と話者を指定(3で標準ずんだもんになる)
    params = (
        ('text', text),
        ('speaker', 3),
    )

    # 音声合成用のクエリ作成
    query = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )

    # 音声合成を実施
    synthesis = requests.post(
        f'http://{host}:{port}/synthesis',
        headers = {"Content-Type": "application/json"},
        params = params,
        data = json.dumps(query.json())
    )

    # 音声合成時間を表示
    end_time = time.time()
    elapsed_time = time.time() - start_time
    formatted_time = f"{elapsed_time:.1f}"
    print(f"音声合成時間: {formatted_time} 秒")

    # 再生処理
    voice = synthesis.content
    pya = pyaudio.PyAudio()

    # サンプリングレートが24000以外だとずんだもんが高音になったり低音になったりする
    stream = pya.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=24000,
                      output=True)

    stream.write(voice)
    stream.stop_stream()
    stream.close()
    pya.terminate()

if __name__ == "__main__":
    while True:
        text = input("テキストを入力： ")
        say(text)

