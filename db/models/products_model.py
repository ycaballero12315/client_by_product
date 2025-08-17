from pydantic import BaseModel 


class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None    

list_products = [Product(name="Producto 1", description="Descripcion 1", price=100.0, tax=10.0),
                 Product(name="Producto 2", description="Descripcion 2", price=200.0, tax=20.0)]