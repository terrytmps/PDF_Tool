# Variables
PYTHON = python3
APP_DIR = app
ASSETS_DIR = assets
BUILD_DIR = build
DIST_DIR = dist

# Tâche par défaut
all: install run

# Installer les dépendances
install:
	$(PYTHON) -m venv venv
	venv/bin/pip install -r requirements.txt

# Construire un executable Windows
buildWin:
	venv/bin/pyinstaller --onefile --windowed --icon=assets/icone.ico app/main.py

# Exécuter l'application
run:
	$(PYTHON) -m $(APP_DIR).main

# Nettoyer les fichiers générés
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) __pycache__
	find $(APP_DIR) -type d -name "__pycache__" -exec rm -r {} +

# Tâche pour exécuter les tests
test:
	venv/bin/pytest

# Tâche pour formater le code
format:
	venv/bin/black $(APP_DIR)

# Tâche pour vérifier le style du code
lint:
	venv/bin/flake8 $(APP_DIR)

# Tâche pour créer une distribution
# dist:
#	$(PYTHON) setup.py sdist bdist_wheel

# Tâche pour exécuter le script shell
execute:
	./execute.sh

# Tâche pour mettre à jour le projet
update:
	./update.sh

.PHONY: all install buildWin run clean test format lint dist execute update
