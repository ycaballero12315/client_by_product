from fastapi import APIRouter, HTTPException
from db.models.products_model import Product, list_products

router = APIRouter(prefix="/product", tags=["product"],responses={404: {"description": "Not found"}})



@router.get("/")
async def read_products():
    return list_products

@router.get("/{id}")
async def read_root():
    if id < 0 or id >= len(list_products):
        raise HTTPException(status_code=404, detail="Product not found")
    return list_products[id]

@router.get("/products/")
async def read_products(Product: Product):
    return [{"name": "Producto 1"}, {"name": "Producto 2"}]

@router.post("/products/", status_code=201)
async def create_product(product: Product):
    product.name = product.name + " Nuevo"
    product.description = product.description + " Nuevo"
    product.price = product.price + 10
    if product.tax:
        product.tax = product.tax + 2       
    return product  