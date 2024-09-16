from fastapi import FastAPI, Query
from enum import Enum
from typing import Union, List

from pydantic import BaseModel
import re

app = FastAPI()

# 最初のステップ

@app.get("/")
async def root():
    return {"message": "hello fast api."}

# パスパラメータ

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# クエリパラメータ

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

# @app.get("/items")
# async def read_item(skip: int = 0, limit: int = 10):
    # return fake_items_db[skip:skip+limit] # http://localhost:8000/items?skip=1&limit=2

@app.get("/item/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description."}
        )
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long descrtiption."}
        )
    return item


# リクエストボディ
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    if q:
        item_dict.update({"q": q})
    return {"item_id": item_id, **item_dict}


# クエリパラメータと文字列の検証
@app.get("/items/")
async def read_items(
    tel: Union[str, None] = Query(
        default="080-1234-5678", 
        min_length=11,
        max_length=13, 
        pattern="^[0-9]{3}(-*)[0-9]{4}(-*)[0-9]{4}$", 
        alias="item-query",
        deprecated=True
        )):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if tel:
        if "-" in tel:
            tel = re.sub("-", "", tel)

        results.update({"tel": tel})
    return results