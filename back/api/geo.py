import json
from typing import Optional, Dict, List

from fastapi import APIRouter
from geojson_pydantic import Feature, FeatureCollection, Point, MultiPolygon

from back.models.factory import Factory
from back.schemas.factory import FactoryGet
from back.schemas.signal import SignalGet
from back.utils.exceptions import NotFound
from datetime import datetime, timedelta
from back.models.signal import Signal, SignalToInstance, SignalProperties

router = APIRouter(tags=["geo"], prefix="/geo")
from fastapi_cache.decorator import cache


def get_geomap_features(city_id=None) -> FeatureCollection:
    time_threshold = datetime.now() - timedelta(hours=24)

    try:
        if city_id:
            factories = Factory.objects.filter(city_id=city_id).select_related('city')
            signals = Signal.objects.filter(created__gte=time_threshold, city_id=city_id).select_related('city')
        else:
            factories = Factory.objects.all().select_related('city')
            signals = Signal.objects.filter(created__gte=time_threshold).select_related('city')
    except Factory.DoesNotExist:
        raise NotFound

    features = []

    for factory in factories:
        feature = Feature(
            geometry=MultiPolygon(coordinates=factory.polygon.coords),
            id=f'factory_{factory.id}'
        )

        factory_model = FactoryGet(**factory.__dict__)

        feature.properties = factory_model.dict()

        features.append(feature)

    for signal in signals:
        feature = Feature(
            geometry=Point(coordinates=signal.point.coords),
            id=f'signal_{signal.id}'
        )

        signal_point = SignalGet(**signal.__dict__)

        feature.properties = signal_point.dict()

        features.append(feature)

    return FeatureCollection(features=features)


@router.get('', response_model=FeatureCollection)
@cache(expire=60)
def get_geomap(city_id: Optional[int] = None):
    return get_geomap_features(city_id)





