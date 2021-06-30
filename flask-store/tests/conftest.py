from app import create_app
from pytest import fixture
from app.extensions import db
from app.models import Product, Category
from slugify import slugify

@fixture
def app():
    app = create_app()
    app.testing = True
    return app



@fixture
def create_database(app):
    with app.app_context():
        db.create_all()

        yield db

        db.session.remove()
        db.drop_all()


@fixture(autouse=True)
def makedb(create_database):
    p = Product()
    p.name = "Bioneye Cam"
    p.slug = slugify(p.name)
    p.price = 500
    p.description = ""
    #p.image = ""
    p.quantity = 10

    c = Category()
    c.name = "tecnologia"
    c.slug = slugify(c.name)

    c2 = Category()
    c2.name = "medicina"
    c2.slug = slugify(c2.name)



    db.session.add(p)
    db.session.add(c)
    db.session.add(c2)

    db.session.commit()
