from typing import Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from redis_om import get_redis_connection

redis_conn = get_redis_connection()

router = APIRouter(tags=["graph"], prefix="/graph")
social_graph = redis_conn.graph("social")


# Define the request body schema
class RedisGraphQuery(BaseModel):
    command: str
    limit: int = 10


# Define the RedisGraph API endpoint
@router.post('/query')
def query_redisgraph(query: RedisGraphQuery):
    # Add the LIMIT clause to the query if a limit is specified
    print(query.dict())
    if query.limit:
        query.command += f" LIMIT {query.limit}"

    result = social_graph.query(query.command)

    # Check if the query was successful
    if not result:
        raise HTTPException(status_code=404, detail="Query not found")

    return result.result_set

