.PHONY: setup run test lint

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	PYTHONPATH=. python scripts/setup_db.py

run:
	PYTHONPATH=. python main.py --invoice_path=$(path)

test:
	PYTHONPATH=. python -m pytest tests/ -v

lint:
	python -m black src/ tests/
	python -m flake8 src/ tests/