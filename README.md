# RepoPromptGenerator

RepoPromptGenerator generates a comprehensive analysis prompt of a directory or list of files, focusing on source code files, for use in automated code review and evaluation processes.

## Features

- Extracts and analyzes the file structure of a given directory, filtering for Python source code files
- Generates an output string that presents a comprehensive description of the codebase's file structure and code snippets
- Ideal for use in code evaluation and review contexts, or as an assistant tool for codebase familiarization

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/yourusername/python-source-code-analyzer.git
cd python-source-code-analyzer
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## Usage

You can run the script from the command line with arguments:

```bash
python -m repopg --dir /path/to/directory
```

or

```bash
python -m repopg --files file1.py file2.py
```

Where `--dir` points to the directory you want to analyze, and `--files` lists the specific files you want to analyze.

You can also specify the file extensions you're interested in with the `--ext` argument:

```bash
python -m repopg --dir /path/to/directory --ext .py .txt
```

This script only analyzes Python (`*.py`) files by default.
