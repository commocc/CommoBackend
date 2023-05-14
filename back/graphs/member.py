import datetime
from typing import Optional

from pydantic import EmailStr

from redis_om import (
    EmbeddedJsonModel,
    JsonModel,
    Field,
    HashModel,
    Migrator,

)


class Member(HashModel):
    pass


class Address(EmbeddedJsonModel):
    address_line_1: str
    address_line_2: Optional[str]
    city: str = Field(index=True)
    state: str = Field(index=True)
    country: str
    postal_code: str = Field(index=True)


class MemberJson(JsonModel):
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True)
    join_date: datetime.date
    age: int = Field(index=True)
    bio: Optional[str] = Field(index=True, full_text_search=True,
                               default="")

    # Creates an embedded model.
    address: Address



"""

Schema mapping
    During index creation, you need to map the JSON elements to SCHEMA fields as follows:

    Strings as TEXT, TAG, or GEO.
    Numbers as NUMERIC.
    Booleans as TAG.
    JSON array
        Array of strings as TAG or TEXT.
        Array of numbers as NUMERIC or VECTOR.
        Array of geo coordinates as GEO.
        null values in such arrays are ignored.
You cannot index JSON objects. Index the individual elements as separate attributes instead.
null values are ignored.

{
  "name": "Noise-cancelling Bluetooth headphones",
  "description": "Wireless Bluetooth headphones with noise-cancelling technology",
  "connection": {
    "wireless": true,
    "type": "Bluetooth"
  },
  "price": 99.98,
  "stock": 25,
  "colors": [
    "black",
    "silver"
  ],
  "embedding": [0.87, -0.15, 0.55, 0.03]
}

FT.CREATE {index_name} ON JSON SCHEMA {json_path} AS {attribute} {type}
FT.CREATE memberIdx ON JSON PREFIX 1 item: 
    SCHEMA 
        $.first_name AS first_name TEXT 
        $.last_name as last_name TEXT 
        $.email AS email TEXT
        
FT.CREATE memberIdx ON JSON SCHEMA 
    $.connection.wireless AS wireless TAG 
    $.connection.type AS connectionType TEXT
"""

from redis_om import get_redis_connection

redis_conn = get_redis_connection()

andrew = Member(
    first_name="Andrew",
    last_name="Brookins",
    email="andrew.brookins@example.com",
    join_date=datetime.date.today(),
    age=38,
    bio="Python developer, works at Redis, Inc."
)

# The model generates a globally unique primary key automatically
# without needing to talk to Redis.
print(andrew.pk)

# We can save the model to Redis by calling `save()`:
andrew.save()

# Expire the model after 2 mins (120 seconds)
andrew.expire(120)

# To retrieve this customer with its primary key, we use `Customer.get()`:
assert Member.get(andrew.pk) == andrew

address = Address(
    address_line_1="123 Main St",
    address_line_2="Apt 1",
    city="San Antonio",
    state="TX",
    country="USA",
    postal_code="78201"
)

andrew2 = MemberJson(
    first_name="Andrew",
    last_name="Brookins",
    email="andrew.brookins@example.com",
    join_date=datetime.date.today(),
    age=38,
    bio="Python developer, works at Redis, Inc.",
    address=address,
)

Migrator().run()

andrew2.save()

# Find all customers who live in San Antonio, TX
x = MemberJson.find(MemberJson.address.city == "San Antonio",
              MemberJson.address.state == "TX")

print(x)
