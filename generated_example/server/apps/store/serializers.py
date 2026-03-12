import pydantic


class OrderIdPath(pydantic.BaseModel):
    orderId: int
