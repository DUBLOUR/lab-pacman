from model import Model
from view import View
from presenter import Presenter


def main():
    model = Model()
    view = View()
    presenter = Presenter(model, view)
    presenter.show()


if __name__ == '__main__':
    main()
