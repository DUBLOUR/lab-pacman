from model import *
from view import *
from presenter import * 


def main():
    model = Model()
    view = View()
    presenter = Presenter(model, view)
    presenter.show()


if __name__ == '__main__':
    main()
