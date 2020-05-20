from model import *
from view import *
from presenter import * 


def main():
    levels = ["1t", "2"]
    # levels = ["1", "2t", "2"]
    presenter = Presenter(levels)
    presenter.start_game()


if __name__ == '__main__':
    main()
