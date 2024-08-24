## baseline info
Copy the `pyproject.toml` file and update the various points.
You should commit the `poetry.lock` file into version control to ensure dependencies are consistent.

**Install**
```text
poetry install
```

**Add a package**
```text
poetry add package-name
```

**Update packages to their latest versions** (within the defined version constraints)
```text
poetry update
```

**Activate the virtual environment**
```text
poetry shell
```

## using poetry for new codebases
### or each project
**Initialize a new Poetry project:**
```text
poetry new project-name
```

**Or add Poetry to an existing project:**
```text
poetry init
```

### Use pyproject.toml to manage dependencies

**Add dependencies:**
```text
poetry add package-name
```

**Install dependencies:**
```text
poetry install
```

### This setup allows you to:
* Easily manage project-specific dependencies.
* Create isolated environments for each project.
* Handle both pyproject.toml and requirements.txt files.

### For projects with requirements.txt:

**Create a new directory for the project and initialize a Poetry project:**
```text
poetry init
```

**Import requirements:**
```text
poetry add $(cat requirements.txt)
```