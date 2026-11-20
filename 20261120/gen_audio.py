"""
批量生成 20261120 每日日语音频
"""
import asyncio
import sys
import os

OUT_DIR = r"e:\日本語を勉強\每日日语\20261120"
VOICE = "ja-JP-NanamiNeural"

WORDS = [
    {
        "id": "w01",
        "word": "焦る",
        "examples": [
            "失敗しても焦らず、一つずつ確認していこう。",
            "締め切りが近づくと、つい焦ってしまう。",
        ],
    },
    {
        "id": "w02",
        "word": "調整",
        "examples": [
            "会議の時間を調整してもらえますか。",
            "体調を崩したので、仕事量を調整する必要がある。",
        ],
    },
    {
        "id": "w03",
        "word": "大袈裟",
        "examples": [
            "彼は小さなミスを大袈裟に言う癖がある。",
            "大袈裟に驚かないで、まずは冷静に状況を見て。",
        ],
    },
    {
        "id": "w04",
        "word": "さすが",
        "examples": [
            "さすがは先輩だ。難しい問題もすぐに解いた。",
            "さすがに今日は疲れたので、早めに帰ろう。",
        ],
    },
    {
        "id": "w05",
        "word": "滑る",
        "examples": [
            "雨の日は道が滑りやすいので、足元に気をつけて。",
            "氷の上で足を滑らせて、転んでしまった。",
        ],
    },
    {
        "id": "w06",
        "word": "節約",
        "examples": [
            "電気代を節約するために、出るときは必ず消すようにしている。",
            "無駄遣いをやめて、もう少し節約しよう。",
        ],
    },
    {
        "id": "w07",
        "word": "硬い",
        "examples": [
            "このパンは焼きすぎて、とても硬くなってしまった。",
            "緊張すると、肩が硬くなってしまう。",
        ],
    },
    {
        "id": "w08",
        "word": "見通し",
        "examples": [
            "来年の売り上げの見通しは明るい。",
            "工事がいつ終わるか、まだ見通しが立たない。",
        ],
    },
    {
        "id": "w09",
        "word": "励ます",
        "examples": [
            "先生は落ち込んでいる学生を優しく励ました。",
            "試合に負けた友達を励ますメッセージを送った。",
        ],
    },
    {
        "id": "w10",
        "word": "稼ぐ",
        "examples": [
            "学生の頃は、アルバイトで生活費を稼いでいた。",
            "前半で点差を稼いだのが、勝ちにつながった。",
        ],
    },
]


async def synthesize(text: str, out_path: str):
    cmd = [
        sys.executable, "-m", "edge_tts",
        "--voice", VOICE,
        "--text", text,
        "--write-media", out_path,
    ]
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE
    )
    _, err = await proc.communicate()
    if proc.returncode != 0:
        print(f"  [FAIL] {out_path}: {err.decode(errors='ignore')}")
    else:
        print(f"  [OK] {os.path.basename(out_path)}")


async def main():
    tasks = []
    for w in WORDS:
        # word audio
        tasks.append(synthesize(w["word"], os.path.join(OUT_DIR, f"{w['id']}.mp3")))
        # example audios
        for i, ex in enumerate(w["examples"], 1):
            tasks.append(synthesize(ex, os.path.join(OUT_DIR, f"{w['id']}_e{i}.mp3")))
    print(f"Generating {len(tasks)} audio files...")
    await asyncio.gather(*tasks)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
