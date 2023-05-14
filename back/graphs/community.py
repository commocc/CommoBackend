import datetime
import sys
from typing import Optional

from pydantic import EmailStr
sys.path.append('../')
sys.path.append('.')

from redis_om import (
    EmbeddedJsonModel,
    JsonModel,
    Field,
    HashModel,
    Migrator,

)

from back.schemas.community import Community


class CommunityNode(JsonModel, Community):
    pass


str = CommunityNode(
    name="Andrew",
    description="Andrew",
    phone="Andrew",
    email="Andrew",
    address="Andrew",
)

Migrator().run()


# The model generates a globally unique primary key automatically
# without needing to talk to Redis.
print(str.pk)

# We can save the model to Redis by calling `save()`:
str.save()

# Expire the model after 2 mins (120 seconds)
str.expire(120)

# To retrieve this customer with its primary key, we use `Customer.get()`:
# assert CommunityNode.get(str.pk) == str

