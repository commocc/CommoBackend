from fastapi import APIRouter

from back.api import ping, instance, signal, city, community, auth, geo, factory, graph, invites

app_router = APIRouter()

app_router.include_router(instance.router)
app_router.include_router(signal.router)
app_router.include_router(community.router)
app_router.include_router(city.router)
app_router.include_router(auth.router)
app_router.include_router(ping.router)
app_router.include_router(factory.router)
app_router.include_router(geo.router)
app_router.include_router(graph.router)
app_router.include_router(invites.router)
