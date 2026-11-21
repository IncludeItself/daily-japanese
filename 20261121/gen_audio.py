"""
批量生成 20261121 每日日语音频
"""
import asyncio
import sys
import os

OUT_DIR = r"e:\日本語を勉強\每日日语\20261121"
VOICE = "ja-JP-NanamiNeural"

WORDS = [
    {
        "id": "w01",
        "word": "落ち着く",
        "examples": [
            "少し落ち着いてから、もう一度考え直してみます。",
            "引っ越しの片付けが終わり、やっと生活が落ち着きました。",
        ],
    },
    {
        "id": "w02",
        "word": "選択",
        "examples": [
            "どちらのコースを選択するか、今週中に決めてください。",
            "経験を積むと、選択の幅が広がっていきます。",
        ],
    },
    {
        "id": "w03",
        "word": "過ごす",
        "examples": [
            "週末は家でのんびりと過ごしたいと思います。",
            "子供の頃の夏休みは、祖母の家で過ごしました。",
        ],
    },
    {
        "id": "w04",
        "word": "素早い",
        "examples": [
            "猫は動きが素早く、少しの音にも反応します。",
            "素早い対応のおかげで、大きなトラブルになりませんでした。",
        ],
    },
    {
        "id": "w05",
        "word": "盛ん",
        "examples": [
            "この町では昔から茶の栽培が盛んです。",
            "会議では新しい事業について、意見の交換が盛んに行われた。",
        ],
    },
    {
        "id": "w06",
        "word": "割引",
        "examples": [
            "このクーポンを使うと、すべての品物が3割引になります。",
            "平日の昼間は映画の料金が割引になる。",
        ],
    },
    {
        "id": "w07",
        "word": "貯金",
        "examples": [
            "海外旅行に行くために、毎月給料の2割を貯金しています。",
            "急な出費に備えて、少しは貯金しておいたほうがいい。",
        ],
    },
    {
        "id": "w08",
        "word": "許す",
        "examples": [
            "友達はすぐに私の失敗を許してくれました。",
            "時間と体力の許す限り、いろいろな場所を訪ねてみたい。",
        ],
    },
    {
        "id": "w09",
        "word": "近所",
        "examples": [
            "近所に新しいパン屋が開店して、朝から行列ができています。",
            "引っ越してから、近所の人と挨拶を交わすようになりました。",
        ],
    },
    {
        "id": "w10",
        "word": "精一杯",
        "examples": [
            "今日は精一杯がんばったので、もう眠くてたまりません。",
            "精一杯の思いを込めて、手紙を書きました。",
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
