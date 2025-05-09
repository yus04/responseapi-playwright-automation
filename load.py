import json
from pathlib import Path

def load_form_sample(path: str | Path = "input/form-sample.json") -> dict:
    """Load and parse the form-sample JSON file.

    Args:
        path: Relative or absolute path to the JSON file.

    Returns:
        Parsed JSON as a Python dictionary.
    """
    with open(Path(path), "r", encoding="utf-8") as fp:
        return json.load(fp)
