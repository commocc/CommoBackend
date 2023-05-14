import redis
import random

from redis.commands.graph import Edge, Node, Path, Graph, GraphCommands

from redis_om import get_redis_connection

redis_conn = get_redis_connection()

# Connect to Redis and Redis Graph
r = redis.Redis(host='localhost', port=6379, db=0)
# Define a graph called "social"
social_graph = r.graph("social")


result = social_graph.query("MATCH (u:Human)<-[:INVITED {community: 'Bashkortostan'}]-(m:Human) RETURN u.name, m.name")
print(result.result_set)

result = social_graph.query("CALL algo.pageRank('Human', 'GIVE_PASSPORT', {iterations:20, dampingFactor:0.85, write: true})")
result = social_graph.query("MATCH (n:Human) RETURN n.name, n.pagerank ORDER BY n.pagerank DESC")
print(result.result_set)
