from model import *
from view import *
from presenter import * 


def main():
    presenter = Presenter(levels=["1t", "2"])
    # presenter = Presenter(levels=["1", "2"])
    presenter.start_game()


if __name__ == '__main__':
    main()
