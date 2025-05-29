import json
from pathlib import Path
from typing import Any
from htmlmin import minify


def is_file_empty(
    file_path: str | Path,
) -> bool:
    """
    Checks whether a file exists and is empty.

    Args:
        file_path (str | Path): The path to the file to check.

    Returns:
        bool: True if the file exists and is empty, False if it contains data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found.")
    return path.stat().st_size == 0


def save_file(
    data: Any,
    path: str | Path,
) -> None:
    """
    Saves data to a file.

    - If the file extension is `.json`, saves the data as JSON (using `json.dump()`).
    - Otherwise, saves the data as a plain text (using `str(data)` and `f.write()`).

    Args:
        data (Any): The data to save. Should be serializable to JSON if using `.json` extension.
        path (str | Path): The file path to save the data to.

    Raises:
        TypeError: If trying to save non-serializable data as JSON.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix == ".json":
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        with path.open("w", encoding="utf-8") as f:
            f.write(str(data))


def minify_html(
    input_path: str,
    output_path: str | None = None,
) -> None:
    """
    Reads an HTML file, minifies its content by removing comments and extra spaces,
    and writes the minified HTML to the output file.

    If `output_path` is None, the input file will be overwritten.

    Args:
        input_path (str): Path to the input HTML file.
        output_path (str | None): Path to save the minified HTML.
                                 Defaults to None, which means overwrite input file.
    """
    if output_path is None:
        output_path = input_path

    with open(input_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(minified_html)
