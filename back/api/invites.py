import redis
import random

from redis.commands.graph import Edge, Node, Path, Graph, GraphCommands

from redis_om import get_redis_connection

redis_conn = get_redis_connection()

# Connect to Redis and Redis Graph
r = redis.Redis(host='localhost', port=6379, db=0)
# Define a graph called "social"
social_graph = r.graph("social")


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router = APIRouter(tags=["graph"], prefix="/graph")


class User(BaseModel):
    slug: str


@router.post("/users/{user_id}")
def users(user: User):

    Node(label="Human", properties=user.dict())
    social_graph.add_node(Node)


@router.get("/users/{user_id}")
def users(user: User):

    query = f"MATCH (n:Human) WHERE n.slug = '{user.slug}' RETURN n"

    result = social_graph.query(query)
    if result.result_set:
        return {"error": f"User with user_id {user.slug} already exists"}

    return result


@router.get("/invites/{user_id}")
def add_user(user: User):

    Node(label="Human", properties=user.dict())
    social_graph.add_node(Node)

