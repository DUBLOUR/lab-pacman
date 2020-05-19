from model import *
from view import *
from presenter import * 


def main():
    model = Model()
    view = View(model)
    presenter = Presenter(model, view)
    presenter.start_game()


if __name__ == '__main__':
    main()
