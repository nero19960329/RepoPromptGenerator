import argparse
from loguru import logger
from typing import Dict, List, Optional
from pathlib import Path

FileStructure = Dict[str, Optional["FileStructure"]]


def get_file_structure(dir: Path, ext: List[str]) -> FileStructure:
    """
    Get the file structure of a directory, and include only files with certain extensions.

    Args:
        dir (str): The directory to get the file structure of.
        ext (List[str]): The file extensions to include in the file structure.

    Returns:
        FileStructure: The file structure of the directory.
    """

    file_structure: FileStructure = {}
    for file in dir.iterdir():
        if file.is_dir():
            # If file is a directory, get its structure recursively
            try:
                sub_structure = get_file_structure(file, ext)
                # Only add this sub directory to the structure if it is not empty
                if sub_structure:
                    file_structure[file.resolve().as_posix()] = sub_structure
            except Exception as e:
                logger.error(f"Failed to get file structure of {file}: {str(e)}")
                raise
        elif file.suffix in ext:
            # If file is a normal file with desired extension, include it in the structure
            try:
                file_structure[file.resolve().as_posix()] = None
            except Exception as e:
                logger.error(f"Failed to include {file} in file structure: {str(e)}")
                raise
    return file_structure


def file_structure_to_string(file_structure: FileStructure, indent: int = 0) -> str:
    """
    Convert a file structure to a string.

    Args:
        file_structure (FileStructure): The file structure to convert.
        indent (int): The indentation level.

    Returns:
        str: The file structure as a string, using |, |- as a prefix for directories and files respectively.
    """

    file_structure_str = ""
    for file, structure in file_structure.items():
        file_structure_str += f"{'| ' * indent}|- {Path(file).name}\n"
        if structure is not None:
            # If current file is a directory, get its structure string recursively
            file_structure_str += file_structure_to_string(structure, indent + 1)
    return file_structure_str


def get_files(file_structure: FileStructure) -> List[str]:
    """
    Extract all file paths from a file structure.

    Args:
        file_structure (FileStructure): The file structure to extract files from.

    Returns:
        List[str]: The list of file paths.
    """
    file_paths = []
    for file, structure in file_structure.items():
        if structure is None:
            # If current file is a normal file, include it in the list
            file_paths.append(file)
        else:
            # If current file is a directory, get its files recursively
            file_paths += get_files(structure)
    return file_paths


def main(
    dir: str | None,
    files: List[str] | None,
    ext: List[str],
) -> None:
    base_dir = None
    if dir:
        base_dir = Path(dir)
        if not base_dir.exists():
            raise FileNotFoundError(f"The directory {base_dir} does not exist.")
        file_structure = get_file_structure(base_dir, ext)
    else:
        # If dir is None, treat each file in files as a separate file
        file_structure = {file: None for file in (files or [])}

    file_structure_str = file_structure_to_string(file_structure)
    file_paths = get_files(file_structure)

    # Validate the file paths
    file_paths = [file for file in file_paths if Path(file).exists()]

    # Read codes from each file
    codes = {}
    for file in file_paths:
        try:
            if base_dir:
                file_relative = Path(file).relative_to(base_dir.resolve()).as_posix()
            else:
                file_relative = Path(file).name
            codes[file_relative] = Path(file).read_text()
        except Exception as e:
            logger.error(f"Failed to read code from {file}: {str(e)}")
            raise
    code_str = "\n\n".join(
        [f"{file}:\n```python\n{codes[file]}```" for file in codes if codes[file]]
    )

    # Generate the prompt string
    prompt = f"""You are a helpful assistant with software development knowledge.
Please analysis the following file structure and the code snippets, then answer the questions below.

{file_structure_str}

{code_str}

1. What is the purpose of the code? (1-2 sentences)
2. Is there any problem with the code? If so, what is it? (1-2 sentences)
3. How would you improve the code? (1-2 sentences)
4. Please score the code on a scale of 1-10 at the following aspects:
    - Readability
    - Maintainability
    - Performance
    - Security
    - Reliability
"""
    print(prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str)
    parser.add_argument("--files", type=str, nargs="*")
    parser.add_argument("--ext", type=str, nargs="+", default=[".py"])
    args = parser.parse_args()

    main(args.dir, args.files, args.ext)
