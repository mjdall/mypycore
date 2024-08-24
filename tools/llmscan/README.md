# llmscan

`llmscan` is a Python script that generates a markdown summary of your codebase for use with your preffered AI assistant. It scans a directory, extracts file contents, and includes a directory structure overview.

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
This copies the markdown summary to your clipboard.

To save the summary to a file:
```bash
llmscan path/to/your/codebase -o summary.md
```

To get help on additional parameters:
```bash
llmscan --help
```

## License

MIT License.
