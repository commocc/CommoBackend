import redis
import random

from redis.commands.graph import Edge, Node, Path, Graph, GraphCommands

from redis_om import get_redis_connection

redis_conn = get_redis_connection()

# Connect to Redis and Redis Graph
r = redis.Redis(host='localhost', port=6379, db=0)
# Define a graph called "social"
social_graph = r.graph("social")

# Function to generate a sample of 1000 users and connections
from tqdm import tqdm


# Function to generate a sample of 1000 users and connections
def generate_example(num_users=1000, num_communities=50, num_projects=100, num_tags=20):
    with tqdm(total=7, desc="Creating nodes") as pbar:
        create_community_nodes(num_communities)
        pbar.update(1)
        create_project_nodes(num_projects)
        pbar.update(1)
        create_member_nodes(num_users, num_communities)
        pbar.update(1)
        create_tag_nodes(num_tags, num_users)
        pbar.update(1)
    with tqdm(total=5, desc="Creating edges") as pbar:
        create_has_tag_edges(num_tags, num_users)
        pbar.update(1)
        create_has_project_edges(num_communities, num_projects)
        pbar.update(1)
        create_joins_project_edges(num_communities, num_projects, num_users)
        pbar.update(1)
        create_invited_by_edges(num_users)
        pbar.update(1)
        create_searched_by_edges(num_users, num_tags)
        pbar.update(1)
    with tqdm(total=3, desc="Creating higher-level groups") as pbar:
        create_federations(num_communities)
        pbar.update(1)
        create_super_communities(num_communities)
        pbar.update(1)
        create_social_voting(num_projects, num_users)
        pbar.update(1)


# Function to create Community nodes
def create_community_nodes(num_communities):
    for i in range(num_communities):
        community = Node(
            label="Community",
            node_id=f"community_{i}",
            alias=f"community_{i}",
            properties={"id": f"community_id_{i}", "name": f"Community_name_ {i}"}
        )
        social_graph.add_node(community)
    social_graph.commit()


# Function to create Project nodes
def create_project_nodes(num_projects):
    for i in range(num_projects):
        project = Node(
            label="Project",
            node_id=f"project_{i}",
            alias=f"project_{i}",
            properties={"id": f"project_id_{i}", "name": f"Project_name {i}"}
        )
        social_graph.add_node(project)
    social_graph.commit()


# Function to create Member nodes and BELONGS_TO edges to Community
def create_member_nodes(num_users, num_communities):
    # communities = social_graph.query(f"MATCH (c:Community) RETURN c LIMIT {num_communities}").result_set
    for i in range(num_users):
        community_id = random.randint(0, num_communities - 1)
        member = Node(
            label="Member",
            node_id=f"member_{i}",
            alias=f"member_{i}",
            properties={"id": f"member_{i}", "name": f"Member {i}"}
        )
        social_graph.add_node(member)
        belongs_to_edge = Edge(member, "BELONGS_TO", Node(alias=f"community_{community_id}"))
        social_graph.add_edge(belongs_to_edge)
    social_graph.commit()


# Function to create Tag nodes
def create_tag_nodes(num_tags, num_users):
    for i in range(num_tags):
        tag = Node(
            node_id=f'tag_{i}',
            label="Tag",
            alias=f'tag_{i}',
            properties={"id": f"tag_{i}", "name": f"Tag {i}"})
        social_graph.add_node(tag)
    social_graph.commit()


# Function to create HAS_TAG edges between Member and Tag
def create_has_tag_edges(num_tags, num_users):
    for i in range(num_tags):
        for j in range(num_users):
            if random.random() < 0.2:
                member_alias = f"member_{j}"
                tag_id = f"tag_{i}"
                has_tag_edge = Edge(
                    Node(alias=member_alias),
                    "HAS_TAG",
                    Node(alias=tag_id),
                )
                social_graph.add_edge(has_tag_edge)
    social_graph.commit()


# Function to create JOINS_PROJECT edges between Member and Project
def create_joins_project_edges(num_communities, num_projects, num_users):
    for i in range(num_communities):
        community_id = f"community_{i}"
        for j in range(num_projects):
            project_id = f"project_{j}"
            for k in range(num_users):
                if random.random() < 0.1:
                    member_id = f"member_{k}"
                    joins_project_edge = Edge(
                        Node(alias=member_id),
                        "JOINS_PROJECT",
                        Node(alias=project_id),
                    )
                    social_graph.add_edge(joins_project_edge)
    social_graph.commit()



# Function to create INVITED_BY edges between Member and Member
def create_invited_by_edges(num_users):
    for i in range(num_users):
        for j in range(num_users):
            if i != j and random.random() < 0.05:
                invited_by_edge = Edge(
                    Node(alias=f"member_{j}"),
                    "INVITED_BY",
                    Node(alias=f"member_{i}"),
                )
                social_graph.add_edge(invited_by_edge)
    social_graph.commit()



# Function to create SEARCHED_BY edges between Member and Tag
def create_searched_by_edges(num_users, num_tags):
    for i in range(num_users):
        for j in range(num_tags):
            if random.random() < 0.1:
                searched_by_edge = Edge(
                    Node(alias=f"member_{i}"),
                    "SEARCHED_BY",
                    Node(alias=f"tag_{j}"),
                )
                social_graph.add_edge(searched_by_edge)
    social_graph.commit()



# Function to create Federation nodes and CONTAINS edges to Community
def create_federations(num_communities):
    for i in range(num_communities // 5):
        federation = Node(
            label="Federation",
            node_id=f"federation_{i}",
            alias=f"federation_{i}",
            properties={"id": f"federation_{i}", "name": f"Federation {i}"}
        )
        social_graph.add_node(federation)
        for j in range(5):
            community_id = f"community_{i*5+j}"
            contains_edge = Edge(
                Node(alias=f"federation_{i}"),
                "CONTAINS",
                Node(alias=community_id),
            )
            social_graph.add_edge(contains_edge)
    social_graph.commit()



# Function to create super-communities
def create_super_communities(num_communities):
    num_super_communities = num_communities // 5
    for i in range(num_super_communities):
        super_community = Node(
            label="SuperCommunity",
            alias=f"super_community_{i}",
            node_id=f"super_community_{i}",
            properties={"id": f"super_community_{i}", "name": f"SuperCommunity {i}"}
        )
        social_graph.add_node(super_community)
        for j in range(5):
            community_id = f"community_{5*i+j}"
            member_of_edge = Edge(Node(alias=community_id), "MEMBER_OF", super_community)
            social_graph.add_edge(member_of_edge)
    social_graph.commit()


# Function to create SocialVoting nodes and HAS_VOTED edges between Member and SocialVoting
def create_social_voting(num_projects, num_users):
    for i in range(num_projects):
        for j in range(num_users):
            if random.random() < 0.05:
                member_id = f"member_{j}"
                social_voting = Node(
                    label="SocialVoting",
                    alias=f"social_voting_{i}",
                    node_id=f"social_voting_{i}",
                    properties={"id": f"social_voting_{i}", "name": f"SocialVoting {i}"}
                )
                social_graph.add_node(social_voting)
                has_voted_edge = Edge(Node(alias=member_id), "HAS_VOTED", social_voting)
                social_graph.add_edge(has_voted_edge)
    social_graph.commit()


# Function to create HAS_PROJECT edges between Community and Project
def create_has_project_edges(num_communities, num_projects):
    for i in range(num_communities):
        community_id = f"community_{i}"
        for j in range(num_projects):
            if random.random() < 0.2:
                project_id = f"project_{j}"
                community_node = social_graph.nodes.get(community_id)
                project_node = social_graph.nodes.get(project_id)
                if community_node and project_node:
                    has_project_edge = Edge(community_node, "HAS_PROJECT", project_node)
                    social_graph.add_edge(has_project_edge)
    social_graph.commit()



if __name__ == "__main__":
    num_communities = 10
    num_projects = 10
    num_users = 10
    num_tags = 10

    generate_example(num_communities, num_projects, num_users, num_tags)
