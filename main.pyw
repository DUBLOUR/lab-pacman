from model import *
from view import *
from presenter import * 


def main():
    model = Model()
    view = View(model)
    presenter = Presenter(model, view)
    model.init_level(2)
    view.paint_background()
    view.create_memes()
    presenter.set_binds()
    #view.show_grid()
    presenter.moveBall()
    presenter.show()


if __name__ == '__main__':
    main()
