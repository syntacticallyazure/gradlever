default:
    just --list;
    
build:
    uv pip install pyinstaller
    uv run pyinstaller ./main.spec

setup:
    uv venv --clear

lint:
    uv pip install ruff
    uv run ruff format ./src

devops:
    just lint
    -git add -A && git commit -m "chore: linted code"
