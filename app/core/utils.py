import os
import functools
import logging
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_file = BASE_DIR / ".env"
# If .env doesn't exist in the project root, fallback to .env.example in the same directory
if not env_file.exists():
    env_file = BASE_DIR / ".env.example"

# Load environment variables from .env file
load_dotenv(dotenv_path=env_file, override=True)

OUTPUT_DIR = os.getenv("OUTPUT_DIR")


def get_output_dir():
    """Retourne le chemin du dossier de sortie"""
    return os.path.expanduser(OUTPUT_DIR)


def handle_errors(func):
    """Décorateur pour la gestion centralisée des erreurs"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Erreur dans {func.__name__}: {str(e)}")
            raise

    return wrapper


def validate_file_path(func):
    """Valide l'existence d'un fichier en premier paramètre"""

    @functools.wraps(func)
    def wrapper(file_path, *args, **kwargs):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cheval de fichier invalide : {file_path}")
        return func(file_path, *args, **kwargs)

    return wrapper
