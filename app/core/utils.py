import os
import functools
import logging


def get_downloads_folder():
    """Retourne le chemin du dossier Téléchargements"""
    return os.path.join(os.path.expanduser("~"), "Downloads")


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
