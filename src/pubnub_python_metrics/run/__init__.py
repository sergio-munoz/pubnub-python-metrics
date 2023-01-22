import sys

from ..app import main as main_app

def main(args=None):
    main_app.main(args)

if __name__ == "__main__":
    main.main(sys.argv[1:])