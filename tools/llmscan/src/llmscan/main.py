import os
import re
import argparse
import subprocess
from pathlib import Path
import pyperclip
import toml


def load_config_from_pyproject(pyproject_path: Path) -> dict:
    """
    Loads configuration for llmscan from pyproject.toml.
    
    :param pyproject_path: Path to the pyproject.toml file.
    :return: Dictionary with configuration settings.
    """
    with open(pyproject_path, "r", encoding="utf-8") as pyproject_file:
        pyproject_data = toml.load(pyproject_file)
        return pyproject_data.get("tool", {}).get("llmscan", {})


def scan_directory(
    directory: Path, extensions: list[str], ignore_dirs: list[str], ignore_re: list[str]
) -> dict:
    """
    Scans the directory for files with specific extensions, ignoring certain folders and files matching a regex.

    :param directory: The directory to scan.
    :param extensions: A list of file extensions to include (e.g., [".py", ".js"]).
    :param ignore_dirs: A list of folder names to ignore (e.g., ["__pycache__", "node_modules"]).
    :param ignore_re: A regex pattern to ignore matching files and directories.
    :return: A dictionary where keys are relative file paths and values are file contents.
    """
    files_dict = {}
    ignore_patterns = [re.compile(pattern) for pattern in ignore_re]
    matches_a_regex = lambda x: any([p.match(x) for p in ignore_patterns])
    
    for root, dirs, files in os.walk(directory):
        # Ignore specific folders
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]

        # Apply regex pattern to directories
        dirs[:] = [d for d in dirs if not matches_a_regex(d)]

        for file in files:
            if file.startswith("."):
                continue

            if matches_a_regex(file):
                continue

            if any(file.endswith(ext) for ext in extensions):
                file_path = Path(root) / file
                with open(file_path, "r", encoding="utf-8") as f:
                    files_dict[file_path.relative_to(directory)] = f.read()
    return files_dict


def get_directory_structure(directory: Path) -> str:
    """
    Uses the "tree" command to get a visual representation of the directory structure.

    :param directory: The directory to scan.
    :return: The output of the "tree" command as a string.
    """
    try:
        result = subprocess.run(
            ["tree", str(directory)], capture_output=True, text=True
        )
        return result.stdout
    except FileNotFoundError:
        return "The `tree` command is not available on this system."


def generate_markdown(file_contents: dict, directory_structure: str) -> str:
    """
    Generates a markdown-formatted string with the directory structure and file contents.

    :param file_contents: A dictionary of file paths and their contents.
    :param directory_structure: The directory structure as a string.
    :return: A markdown-formatted string.
    """
    md_output = f"# Directory Structure\n\n```\n{directory_structure}\n```\n\n"

    for file_path, content in file_contents.items():
        md_output += f"## {file_path}\n\n```{file_path.suffix[1:]}\n{content}\n```\n\n"

    return md_output


def main():
    parser = argparse.ArgumentParser(
        description="Generate a markdown summary of your codebase for your preferred AI assistant."
    )
    parser.add_argument(
        "directory", type=str, help="The path to the codebase directory to scan."
    )
    parser.add_argument(
        "-e",
        "--extensions",
        type=str,
        nargs="+",
        help="File extensions to include (e.g., '.py', '.js').",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output markdown file name. If not provided, the output will be copied to the clipboard.",
    )
    parser.add_argument(
        "-id",
        "--ignore-dirs",
        type=str,
        nargs="+",
        help="Directories to ignore (e.g., '__pycache__', 'node_modules').",
    )
    parser.add_argument(
        "-ir",
        "--ignore-re",
        type=str,
        nargs="+",
        help="Regex patterns to ignore matching files and directories. You can specify multiple patterns.",
    )

    args = parser.parse_args()

    # Load config from pyproject.toml if available
    pyproject_path = Path(args.directory) / "pyproject.toml"
    config = {}
    if pyproject_path.exists():
        config = load_config_from_pyproject(pyproject_path)

    # Override config with command-line arguments if provided
    extensions = args.extensions if args.extensions else config.get("extensions", [".py", ".js"])
    ignore_dirs = args.ignore_dirs if args.ignore_dirs else config.get("ignore_dirs", ["__pycache__", "node_modules"])
    ignore_re = args.ignore_re if args.ignore_re else config.get("ignore_re", [])

    directory_path = Path(args.directory)
    
    if not directory_path.exists() or not directory_path.is_dir():
        print(f"Error: The directory {directory_path} does not exist or is not a valid directory.")
        return

    file_contents = scan_directory(directory_path, extensions, ignore_dirs, ignore_re)
    directory_structure = get_directory_structure(directory_path)
    markdown = generate_markdown(file_contents, directory_structure)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as md_file:
            md_file.write(markdown)
        print(f"Markdown summary generated at {args.output}")
    else:
        pyperclip.copy(markdown)
        print("Markdown summary copied to clipboard.")



if __name__ == "__main__":
    main()
