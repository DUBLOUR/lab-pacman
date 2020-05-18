from model import *
from view import *
from presenter import * 


def main():
    model = Model()
    view = View(model)
    presenter = Presenter(model, view)
    
    model.init_level(2)
    view.load_textures()
    view.draw_background()
    view.create_enemies()
    presenter.set_binds()
    #view.show_grid()
    presenter.main_loop()
    presenter.show()


if __name__ == '__main__':
    main()
