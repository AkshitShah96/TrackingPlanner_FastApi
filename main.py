from fastapi import FastAPI, Depends
from models import Product
from fastapi.middleware.cors import CORSMiddleware
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def Greet():
    return "Akshit Tracker System"



products = [
    Product(id=1, name="phone", description="budget", price=56445.5, quantity=5),
    Product(id=2, name="Akshit", description="budget", price=544225.5, quantity=6),
    Product(id=3, name="yashvi", description="budget", price=54565645.5, quantity=1),
    Product(id=4, name="mahek", description="budget", price=5433345.5, quantity=99),
]


def get_data():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    if db.query(database_models.Product).count() == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()


@app.get("/products")
def all_my_products(db: Session = Depends(get_data)):
    return db.query(database_models.Product).all()


@app.post("/products")
def create_any_product(product: Product, db: Session = Depends(get_data)):
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    return product


@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_data)):
    db_prod = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_prod:
        return db_prod
    return "product not found"

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_data)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product updated"
    return "no product found"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_data)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted"
    return "product not found"
