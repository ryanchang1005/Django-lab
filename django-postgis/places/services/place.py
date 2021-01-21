from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from core.services.geometry import GeometryService
from places.models import Place


class PlaceService:

    @staticmethod
    def create(
            name,
            lat,
            lng
    ):
        position = GeometryService.create_geometry(lat, lng)

        place = Place()
        place.name = name
        place.position = position
        place.save()

        return place

    @staticmethod
    def filter(
            pk=None
    ):
        qs = Place.objects.all()
        return qs

    @staticmethod
    def filter_around_place(
            center_position,
            distance
    ):
        """
        取出position周遭distance公里的景點, 並算出距離, 距離遞增
        :param center_position: GEOSGeometry: 中心點
        :param distance: str | float: 範圍N公里
        :return: list
        """

        qs = Place.objects.filter(position__distance_lte=(center_position, D(km=distance))) \
            .annotate(distance=Distance('center_position', center_position)) \
            .order_by('distance')

        place_list = []
        for place in qs:
            place_list.append({
                'name': place.name,
                'lat': str(place.position.coords[0]),
                'lng': str(place.position.coords[1]),
                'distance_km': str(round(place.distance.m / 1000, 4)),
            })

        return place_list


"""
from places.services.place import *
PlaceService.create('台北車站', 25.0477022, 121.5173748)
PlaceService.create('台北101', 25.0338489, 121.5645294)
PlaceService.create('行天宮', 25.0630708, 121.5339026)
PlaceService.create('大安森林公園', 25.0324362, 121.5349057)
"""
