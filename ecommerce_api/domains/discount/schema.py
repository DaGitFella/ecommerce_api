from pydantic import BaseModel, ConfigDict


class DiscountSchema(BaseModel):
    name: str
    slug: str
    value: float
    start_date: str
    end_date: str


class DiscountPublic(BaseModel):
    id: int
    name: str
    slug: str
    value: float
    start_date: str
    end_date: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class DiscountList(BaseModel):
    discounts: list[DiscountPublic]
