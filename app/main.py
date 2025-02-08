from app.views.main_view import MainWindow
from app.core.utils import get_downloads_folder


def main():
    downloads_path = get_downloads_folder()
    app = MainWindow(downloads_path)
    app.mainloop()


if __name__ == "__main__":
    main()
