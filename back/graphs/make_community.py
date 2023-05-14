import redis
import random

from redis.commands.graph import Edge, Node, Path, Graph, GraphCommands

from redis_om import get_redis_connection

redis_conn = get_redis_connection()

# Connect to Redis and Redis Graph
r = redis.Redis(host='localhost', port=6379, db=0)
# Define a graph called "social"
social_graph = r.graph("social")

# try:
#     # Delete the entire graph
#     social_graph.delete()
# except Exception as e:
#     pass

# Function to generate a sample of 1000 users and connections
from tqdm import tqdm

# Create nodes that represent users
users = {
    "SalavatNakamoto": Node(label="Human", properties={"name": "SalavatNakamoto", "age": 39}),
    "Ural": Node(label="Human", properties={"name": "Ural", "age": 36}),
    "Shulman": Node(label="Human", properties={"name": "Shulman", "age": 37}),
    "Akbuzat": Node(label="Human", properties={"name": "Akbuzat", "age": 33}),
    "Putin": Node(label="Human", properties={"name": "Akbuzat", "age": 33}),
    "AnisaGPT": Node(label="Bot", properties={"name": "AnisaGPT", "age": 1}),
    "Ahmet": Node(label="Human", properties={"name": "Ahmet", "age": 1}),
}

# Add users to the graph as nodes
for key in users.keys():
    social_graph.add_node(users[key])

# Create nodes that represent users
communitys = {
    "Bashkortostan": Node(label="Community", properties={"name": "Bashkortostan", "language": 'bashkir'}),
    "Tatarstan": Node(label="Community", properties={"name": "Tatarstan", "language": 'tatar'}),
    "Russian": Node(label="Community", properties={"name": "Russia", "language": 'russian'}),
}

# Add users to the graph as nodes
for key in communitys.keys():
    social_graph.add_node(communitys[key])

# Create nodes that represent users, NFT tokens
achievment = {
    "Tamga": Node(label="Stamp", properties={"name": "Tamga", "score": 1}),
    "Z-war": Node(label="Stamp", properties={"name": "Antiwar", "score": 1}),

    "Antiwar": Node(label="Achievement", properties={"name": "Antiwar", "score": 1}),
    "Kushtaw": Node(label="Achievement", properties={"name": "Kushtaw", "score": 1}),
    "Bashkir Language": Node(label="Achievement", properties={"name": "Tamga", "score": 1}),
}

# Add users to the graph as nodes
for key in achievment.keys():
    social_graph.add_node(achievment[key])

# inveted
# должен 2 связи получить, от сообщества и от человека минимум 3

# SalavatNakamoto
social_graph.add_edge(Edge(users["SalavatNakamoto"], "JOIN", communitys["Bashkortostan"]))

# social_graph.add_edge(Edge(users["SalavatNakamoto"], "INVITED", users["Shulman"]))
social_graph.add_edge(Edge(users["Ural"], "INVITED", users["Akbuzat"], properties={'community': "Bashkortostan"}))
social_graph.add_edge(Edge(users["Ural"], "INVITED", users["Shulman"], properties={'community': "Bashkortostan"}))
social_graph.add_edge(Edge(users["Ural"], "INVITED", users["SalavatNakamoto"], properties={'community': "Bashkortostan"}))

# Add relationships between user nodes
# social_graph.add_edge(Edge(communitys["Bashkortostan"], "VERIFIED", users["SalavatNakamoto"]))
social_graph.add_edge(Edge(communitys["Bashkortostan"], "VERIFIED", users["Ural"]))
social_graph.add_edge(Edge(communitys["Bashkortostan"], "VERIFIED", users["Akbuzat"]))

social_graph.add_edge(Edge(communitys["Tatarstan"], "VERIFIED", users["Ural"]))
social_graph.add_edge(Edge(communitys["Tatarstan"], "VERIFIED", users["Akbuzat"]))

# stamps archivemnts
social_graph.add_edge(Edge(communitys["Bashkortostan"], "EMISSION", achievment["Kushtaw"]))
social_graph.add_edge(Edge(achievment["Kushtaw"], "GIVE", users["Ural"]))

# Create the graph in the database
social_graph.commit()
