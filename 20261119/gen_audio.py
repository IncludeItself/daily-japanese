"""
批量生成 20261119 每日日语音频
"""
import asyncio
import subprocess
import sys
import os

OUT_DIR = r"e:\日本語を勉強\每日日语\20261119"
VOICE = "ja-JP-NanamiNeural"

WORDS = [
    {
        "id": "w01",
        "word": "断る",
        "examples": [
            "都合が悪いときは、はっきり断ったほうがいいです。",
            "急なお願いをされて、断るわけにもいかない。",
        ],
    },
    {
        "id": "w02",
        "word": "間違える",
        "examples": [
            "緊張して、相手の名前を間違えてしまった。",
            "電車に乗り遅れないように、時間を間違えないでください。",
        ],
    },
    {
        "id": "w03",
        "word": "培う",
        "examples": [
            "若いときに培った経験は、後で必ず役に立ちます。",
            "長年の努力で信頼関係を培ってきた。",
        ],
    },
    {
        "id": "w04",
        "word": "残業",
        "examples": [
            "今日は急な残業で、帰りが遅くなりそうです。",
            "金曜日の夜は残業しないようにしています。",
        ],
    },
    {
        "id": "w05",
        "word": "交換",
        "examples": [
            "買ったばかりの靴は、サイズを交換してもらいました。",
            "会議の前に、名刺を交換して自己紹介をした。",
        ],
    },
    {
        "id": "w06",
        "word": "種類",
        "examples": [
            "この店はお菓子の種類が豊富です。",
            "どの種類を選べばいいか、まだ迷っています。",
        ],
    },
    {
        "id": "w07",
        "word": "快適",
        "examples": [
            "新しいアパートは日当たりがよくて、とても快適です。",
            "夏でも快適に過ごせるように、風通しをよくした。",
        ],
    },
    {
        "id": "w08",
        "word": "適当",
        "examples": [
            "彼はいつも適当なことを言って、周りに迷惑をかけている。",
            "レポートを適当に書いてはいけない。",
        ],
    },
    {
        "id": "w09",
        "word": "眠い",
        "examples": [
            "昨夜あまり眠れなかったので、今日はとても眠い。",
            "眠いときは、短い昼寝のほうがコーヒーより効く。",
        ],
    },
    {
        "id": "w10",
        "word": "うっかり",
        "examples": [
            "うっかりして、傘を電車に忘れてしまった。",
            "うっかり約束の日を過ぎてしまった。",
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
