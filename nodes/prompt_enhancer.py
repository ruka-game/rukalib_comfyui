import ollama
import subprocess
import os
import requests
from tqdm import tqdm


def download(url: str, fname: str, chunk_size=1024):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(fname, "wb") as file, tqdm(
        desc=fname,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)


model_dir_path = "ComfyUI/models/rukalib/ollama"
model_gguf_name = "HODACHI-EZO-Humanities-9B-gemma-2-it-IQ4_XS.gguf"
model_path = "/".join([model_dir_path, model_gguf_name])

model_gguf_source_url = "https://hf.rst.im/mmnga/HODACHI-EZO-Humanities-9B-gemma-2-it-gguf/resolve/main/HODACHI-EZO-Humanities-9B-gemma-2-it-IQ4_XS.gguf"

model_name = "prompt_enhancer"
model_file = f'''
FROM  ./{model_path}

# set the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1.0

# set the system message
SYSTEM """
assistantは動画生成プロンプトを生成するためだけに存在する機械です
assistantとしての説明や提案などの余計な返答はせずに、動画生成プロンプトのみを英語で返します
返す文字数の目安や内容については都度の指示に従うこと
"""
'''


def get_response(prompt, num_tokens, keep_on_gpu):
    try:
        model_list = ollama.list()
    except Exception:
        subprocess.call("ollama serve")

    try:
        model_list = ollama.list()
    except Exception:
        print("ollamaをインストールしてください")

    is_model_found = False

    for model in model_list["models"]:
        if model["name"] == model_name:
            is_model_found = True
            break

    if not is_model_found:
        if not os.path.exists(model_path):
            if not os.path.exists(model_dir_path):
                os.makedirs(model_dir_path)

            download(model_gguf_source_url, model_path)

        ollama.create(model=model_name, modelfile=model_file)

    response = ollama.chat(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": f"次のユーザの入力から想像を膨らませ、内容に沿って拡張した{num_tokens}トークン程度の英語の動画生成プロンプトをただ一つ生成し、その本文のみを返答せよ",
            },
            {
                "role": "system",
                "content": f"○○などを参考に提示せよという内容で示された例はあくまでも例示なので極力他の類似例も挙げること。プログラムやテンプレートを使わずに自分で選択すること",
            },
            {"role": "user", "content": prompt},
        ],
        keep_alive=-1 if keep_on_gpu else 0,
    )

    return response["message"]["content"]


class RukaPromptEnhancer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                    },
                ),
                "num_tokens": (
                    "INT",
                    {
                        "default": 16,  # 英語は英単語1個くらいで1トークンが目安
                        "min": 0,
                        "max": 256,
                        "step": 1,
                        "display": "number",
                    },
                ),
                "fantasy": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
                "cyberpunk": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
                "modern": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
                "indoor": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
                "outdoor": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
                "girl": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
                "boy": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
                "androgynous": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
                "upper_chest": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
                "random_hairstyle": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
                "random_haircolor": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
                "random_eyecolor": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
                "random_costume": (
                    "BOOLEAN",
                    {
                        "default": True,
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "step": 1,
                    },
                ),
                "keep_on_gpu": (
                    "BOOLEAN",
                    {
                        "default": False,
                    },
                ),
            },
        }

    RETURN_TYPES = ("STRING",)
    # OUTPUT_IS_LIST = (True,)
    # RETURN_NAMES = ("image_output_name",)

    FUNCTION = "generate_prompt"

    # OUTPUT_NODE = False

    CATEGORY = "Prompt"

    def generate_prompt(
        self,
        prompt,
        num_tokens,
        fantasy,
        cyberpunk,
        modern,
        indoor,
        outdoor,
        girl,
        boy,
        androgynous,
        upper_chest,
        random_hairstyle,
        random_haircolor,
        random_eyecolor,
        random_costume,
        seed,
        keep_on_gpu,
    ):
        global last_seed

        tags = [prompt]

        if fantasy:
            tags.append("fantasy")
        if cyberpunk:
            tags.append("cyberpunk")
        if modern:
            tags.append("modern")
        if indoor:
            tags.append("indoor")
        if outdoor:
            tags.append("outdoor")
        if girl:
            tags.append("girl")
        if boy:
            tags.append("boy")
        if androgynous:
            tags.append("androgynous")
        if upper_chest:
            tags.append("upper chest")
        if random_hairstyle:
            tags.append("髪型をボブ/ロング/ミディアムなどを参考に自由な発想でひとつ提示せよ")
        if random_haircolor:
            tags.append("髪色を金/黒/茶などを参考に自由な発想でひとつ提示せよ")
        if random_eyecolor:
            tags.append("瞳の色を青/緑/赤/ピンク/茶などを参考に自由な発想でひとつ提示せよ")
        if random_costume:
            tags.append("場面に合った衣装を洋服/和服/Tシャツ/スーツ/コートなどを参考に自由な発想でひとつ提示せよ")
            
        prompt = ", ".join(tags)
        enhanced_prompt = get_response(prompt, num_tokens, keep_on_gpu)

        return {"ui": {"generated": enhanced_prompt}, "result": (enhanced_prompt,)}


if __name__ == "__main__":
    print(get_response("サイバーパンク", 16))
