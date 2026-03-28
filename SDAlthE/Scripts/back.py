from pathlib import Path
import json
import random
from datetime import datetime

def root_dir():
    DIR = Path(__file__).resolve().parent.parent
    return DIR

def load_language(language_code):
    import importlib
    module = importlib.import_module(f"Languages.{language_code}")
    return module.translations

def language(selected: dict, key):
    return selected.get(key, "!Text Not Found!")

def grid_gen(container, row=0, column=0, weight=1):
    for c in range(column):
        container.columnconfigure(c, weight=1)
    for r in range(row):
        container.rowconfigure(r, weight=1)

def language_list(root_directory: Path):
    language_directory = root_directory / "Languages"
    return [
        file.stem for file in sorted(language_directory.glob("*.py"))
    ]

def json_load(arch: Path):
    json_path = root_dir() / arch
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def json_save(arch: Path, dictionary: dict):
    json_path = root_dir() / arch
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=4)

def list_model():
    models_directory = root_dir() / "Models"
    return {
        file.stem: file
        for file in sorted(models_directory.glob("*.safetensors"))
    }

def validate_seed(value):
    if value == "":
        return True
    return value.isdigit()

def random_seed(variable):
    seed_random = random.randint(0, 2**32 - 1)
    variable.set(seed_random)

def image_index(folder):
    files = list(folder.glob("*.png"))

    if not files:
        return 1
    
    numbers = []
    for f in files:
        try:
            num = int(f.stem.split("_")[0])
            numbers.append(num)
        except:
            pass

    return max(numbers) + 1 if numbers else 1

def save_image(image, seed):
    output_dir = root_dir() / "Outputs" / datetime.now().strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)

    index = image_index(output_dir)

    filename = f"{index:04d}_{seed}.png"
    file_path = output_dir / filename

    image.save(file_path)

    return file_path