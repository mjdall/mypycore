# llmscan

`llmscan` is a streamlined Python tool that scans your codebase, generating a concise markdown summary complete with file contents and a directory structure overview. Perfect for preparing your code for analysis by AI assistants, `llmscan` helps you present your project in a clear and organized format.

_this codebase is pretty much all gpt4 generated - piloted by yours truly_

## Installation

1. Clone the repo and navigate into it:
   ```bash
   git clone https://github.com/yourusername/llmscan.git
   cd llmscan
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```

## Usage

### Basic Usage
Run `llmscan` with the path to your codebase:
```bash
llmscan path/to/your/codebase
```
This copies the markdown summary to your clipboard.

To save the summary to a file:
```bash
llmscan path/to/your/codebase -o summary.md
```

### Configuration via `pyproject.toml`
You can configure `llmscan` by adding settings to your `pyproject.toml` file. These settings allow you to specify which directories to ignore and which file extensions to include.

Here’s an example configuration:

```toml
[tool.llmscan]
ignore_dirs = ["__pycache__", "node_modules"]
ignore_re = ["\\.(log|tmp)$", "^test_"]  # Ignore files with .log or .tmp extensions and files starting with "test_"
extensions = [".py", ".js"]
```

- **`ignore_dirs`**: A list of directories to ignore during the scan (e.g., `["__pycache__", "node_modules"]`).
- **`ignore_re`**: A list of regex patterns to ignore files or directories that match them (e.g., `["\\.(log|tmp)$", "^test_"]` to ignore `.log`, `.tmp` files and files starting with "test_").
- **`extensions`**: A list of file extensions to include in the summary (e.g., `[".py", ".js"]`).

### Command-line Overrides
You can override the configuration from `pyproject.toml` using command-line arguments:

- Specify file extensions:
  ```bash
  llmscan path/to/your/codebase -e .py .js
  ```

- Ignore specific directories:
  ```bash
  llmscan path/to/your/codebase -id __pycache__ node_modules
  ```

- Use multiple regex patterns to ignore files and directories:
  ```bash
  llmscan path/to/your/codebase -ir "\\.(log|tmp)$" "^test_"
  ```

### Help
To get help on additional parameters:
```bash
llmscan --help
```

## License

MIT License.
