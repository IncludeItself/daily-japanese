"""
批量生成 20261118 每日日语音频
"""
import asyncio
import subprocess
import sys
import os

OUT_DIR = r"e:\日本語を勉強\每日日语\20261118"
VOICE = "ja-JP-NanamiNeural"

WORDS = [
    {
        "id": "w01",
        "word": "決める",
        "examples": [
            "明日までに出張先を決めなければならない。",
            "彼女は進路を大学院に決めた。",
        ],
    },
    {
        "id": "w02",
        "word": "納得",
        "examples": [
            "説明を聞いて、やっと納得しました。",
            "この料金なら納得できます。",
        ],
    },
    {
        "id": "w03",
        "word": "伝わる",
        "examples": [
            "彼女の熱意はみんなに伝わった。",
            "古い伝統が代々伝わっている。",
        ],
    },
    {
        "id": "w04",
        "word": "丁寧",
        "examples": [
            "先生はいつも丁寧に教えてくれます。",
            "丁寧な手紙を頂き、ありがとうございます。",
        ],
    },
    {
        "id": "w05",
        "word": "いつのまにか",
        "examples": [
            "いつのまにか窓の外は暗くなっていた。",
            "いつのまにか友達がたくさんできた。",
        ],
    },
    {
        "id": "w06",
        "word": "負担",
        "examples": [
            "仕事と家事の両立は大きな負担になっている。",
            "親に負担をかけたくない。",
        ],
    },
    {
        "id": "w07",
        "word": "活気",
        "examples": [
            "朝の公園は活気に満ちている。",
            "新しいリーダーが来て、チームに活気が出た。",
        ],
    },
    {
        "id": "w08",
        "word": "控えめ",
        "examples": [
            "彼は控えめな性格で、あまり目立たない。",
            "辛いものは控えめにしている。",
        ],
    },
    {
        "id": "w09",
        "word": "ぴったり",
        "examples": [
            "この靴は足にぴったりです。",
            "3時にぴったり着きました。",
        ],
    },
    {
        "id": "w10",
        "word": "磨く",
        "examples": [
            "毎日日本語を磨いています。",
            "鏡を磨くと、部屋が明るく見える。",
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
