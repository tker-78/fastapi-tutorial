from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from enum import Enum
from typing import Union, List, Set, Annotated

from pydantic import BaseModel, Field, HttpUrl, EmailStr
import re
import json
from datetime import datetime, timedelta, time
from uuid import UUID


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
# @app.get("/items/")
# async def read_items(
#     tel: Union[str, None] = Query(
#         default="080-1234-5678", 
#         min_length=11,
#         max_length=13, 
#         pattern="^[0-9]{3}(-*)[0-9]{4}(-*)[0-9]{4}$", 
#         alias="item-query",
#         deprecated=True
#         )):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if tel:
#         if "-" in tel:
#             tel = re.sub("-", "", tel)

#         results.update({"tel": tel})
#     return results


# パスパラメータと数値の検証
# @app.get("/items/{item_id}")
# async def read_items(
#     *,
#     item_id: int = Path(title="The ID of the item to get", ge=1),
#     q: str
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# ボディ-複数のパラメータ
# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int = Path(title="The ID of the item to get", ge=0, le=100),
#     q: Union[str, None] = None,
#     item: Union[Item, None] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     return results


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(embed=True)):
#     results = {"item_id": item_id, "item": item }
#     return results

# ボディ-フィールド

# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = Field(
#         default=None, title="The description of the item", max_length=300
#     )
#     price: float = Field(gt=0, description="The price must be greater than 0")
#     tax: Union[float, None] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        embed=True,
        examples=[
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        ])):
    results = {"item_id": item_id, "item": Item}
    return results



# ボディ-ネストされたモデル
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than 0")
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[List[Image], None] = None
    # スキーマの追加
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

@app.get("/json_schema")
async def json_schema():
    return json.dumps(Item.model_json_schema())


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at :Union[time, None] = Body(default=None)
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration
    }

# クッキーのパラメータ


@app.get("/items/")
async def read_items(user_agent: Union[str, None] = Header(default=None)): # user_agent -> User-Agentに自動的に変換される
    return {"User-Agent": user_agent}


# Cookie Parameter Models
class Cookies(BaseModel):
    model_config= {"extra": "forbid"}
    session_id: str
    fatebook_tracker: Union[str, None] = None
    googall_tracker: Union[str, None] = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies


# Header Parameter Models
class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Union[str, None] = None
    traceparent: Union[str, None] = None
    x_tag: list[str] = []

@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    return headers


# レスポンスモデル
@app.post("/items/", response_model = Item)
async def create_item(item: Item) -> Any:
    return item

@app.get("/items/", response_model=List[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: int):
    return item[item_id]