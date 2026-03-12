from enum import StrEnum

import pydantic


class OrderStatus(StrEnum):
    placed = "placed"
    approved = "approved"
    delivered = "delivered"


class PetStatus(StrEnum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Address(pydantic.BaseModel):
    street: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None


class Customer(pydantic.BaseModel):
    id: int | None = None
    username: str | None = None
    address: list[Address] | None = None


class Category(pydantic.BaseModel):
    id: int | None = None
    name: str | None = None


class Tag(pydantic.BaseModel):
    id: int | None = None
    name: str | None = None


class Pet(pydantic.BaseModel):
    name: str
    photoUrls: list[str]
    id: int | None = None
    category: Category | None = None
    tags: list[Tag] | None = None
    status: PetStatus | None = None


class Order(pydantic.BaseModel):
    id: int | None = None
    petId: int | None = None
    quantity: int | None = None
    shipDate: str | None = None
    status: OrderStatus | None = None
    complete: bool | None = None


class User(pydantic.BaseModel):
    id: int | None = None
    username: str | None = None
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    password: str | None = None
    phone: str | None = None
    userStatus: int | None = None


class ApiResponse(pydantic.BaseModel):
    code: int | None = None
    type: str | None = None
    message: str | None = None
