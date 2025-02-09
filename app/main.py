from app.views.main_view import MainWindow
from app.core.utils import get_output_dir


def main():
    output_dir = get_output_dir()
    app = MainWindow(output_dir)
    app.mainloop()


if __name__ == "__main__":
    main()
