
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from back.models.city import City
from back.schemas.city import CityGet, ListCities
from back.utils.exceptions import NotFound, NoData

router = APIRouter(tags=["city"], prefix="/city")


@router.get('/all', response_model=ListCities)
@cache(expire=360)
def get_all_cities():
    city_query = City.objects.all()
    result = []

    for row in city_query:
        city = CityGet.from_orm(row)
        result.append(city)

    return result


@router.get('/{city_id}/total')
@cache(expire=360)
def get_total(city_id: int):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        raise NotFound

