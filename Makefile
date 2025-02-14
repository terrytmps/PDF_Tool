PYTHON = python3
APP_DIR = app
ASSETS_DIR = assets
BUILD_DIR = build

# Tâche par défaut
all: install run

# Installer les dépendances
install:
	$(PYTHON) -m venv venv
	venv/bin/pip install -r requirements.txt

# Exécuter l'application
run:
	$(PYTHON) -m $(APP_DIR).main

# Nettoyer les fichiers générés
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) __pycache__
	find $(APP_DIR) -type d -name "__pycache__" -exec rm -rf {} +
	find tests -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache

# Tâche pour exécuter les tests
test:
	venv/bin/pytest

# Tâche pour formater le code
format:
	venv/bin/black $(APP_DIR)

# Tâche pour vérifier le style du code
lint:
	venv/bin/flake8 $(APP_DIR)

# Pour la preview des PDF
install-apt-dependencies:
	sudo apt-get update
	sudo apt-get install -y poppler-utils
	sudo apt install ghostscript

.PHONY: all install run clean test format lint install-apt-dependencies
