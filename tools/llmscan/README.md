# llmscan

`llmscan` is a Python script that generates a markdown summary of your codebase for use with GPT-4. It scans a directory, extracts file contents, and includes a directory structure overview.

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

Run `llmscan` with the path to your codebase:
```bash
llmscan path/to/your/codebase
```
This generates `codebase_summary.md` with the extracted content and structure.

## License

MIT License.
