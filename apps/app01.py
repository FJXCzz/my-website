from fastapi import APIRouter
from pydantic import BaseModel,Field,field_validator



app01 = APIRouter()

class Item(BaseModel):
    price: float=Field(gt=0)
    tax: float 


    @field_validator("tax")
    def tax_must_15(cls,v):
        if v <= 10.8:
            raise ValueError('tax must be smalthan 10.8')
        return v



@app01.post("/items/{item_id}")
async def update_item(item_id: int, name: str,item: Item):
    print(f"id:{item_id},n:{name},{item}")

    return {
        "ID":item_id
    }

