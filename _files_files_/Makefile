.PHONY: install test lint clean

install:
    pip install -r requirements.txt

test:
    pytest

lint:
    flake8 aws_tagging_tool
    black --check aws_tagging_tool

clean:
    rm -rf __pycache__
    rm -rf .pytest_cache
    rm -rf .coverage
    find . -type d -name "*.egg-info" -exec rm -rf {} +
