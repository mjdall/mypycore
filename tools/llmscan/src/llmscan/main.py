import os
import argparse
import subprocess

from pathlib import Path


def scan_directory(directory: Path, extensions: list[str], ignore_folders: list[str]) -> dict:
    """
    Scans the directory for files with specific extensions, ignoring certain folders.
    
    :param directory: The directory to scan.
    :param extensions: A list of file extensions to include (e.g., [".py", ".js"]).
    :param ignore_folders: A list of folder names to ignore (e.g., ["__pycache__", "node_modules"]).
    :return: A dictionary where keys are relative file paths and values are file contents.
    """
    files_dict = {}
    for root, dirs, files in os.walk(directory):
        # Ignore specific folders
        dirs[:] = [d for d in dirs if d not in ignore_folders and not d.startswith(".")]
        
        for file in files:
            if file.startswith("."):
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
        result = subprocess.run(["tree", str(directory)], capture_output=True, text=True)
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
    parser = argparse.ArgumentParser(description="Generate a markdown summary of your codebase for your preferred ai assitant.")
    parser.add_argument("directory", type=str, help="The path to the codebase directory to scan.")
    parser.add_argument("-e", "--extensions", type=str, nargs="+", default=[".py", ".js"],
                        help="File extensions to include (e.g., '.py', '.js').")
    parser.add_argument("-o", "--output", type=str, default="ai-summary.md",
                        help="The output markdown file name.")
    parser.add_argument("-i", "--ignore", type=str, nargs="+", default=["__pycache__", "node_modules"],
                        help="Folders to ignore (e.g., '__pycache__', 'node_modules').")
    
    args = parser.parse_args()

    directory_path = Path(args.directory)
    
    file_contents = scan_directory(directory_path, args.extensions, args.ignore)
    directory_structure = get_directory_structure(directory_path)
    markdown = generate_markdown(file_contents, directory_structure)
    
    with open(args.output, "w", encoding="utf-8") as md_file:
        md_file.write(markdown)
    
    print(f"Markdown summary generated at {args.output}")

if __name__ == "__main__":
    main()
