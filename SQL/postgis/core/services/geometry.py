from django.contrib.gis.geos import GEOSGeometry

from geopy.distance import distance


class GeometryService:

    @staticmethod
    def create_geometry(lat, lng):
        """
        :param lat: 緯度: [-90, 90]
        :param lng: 經度: [-180, 180]
        :return:
        """
        return GEOSGeometry(f'POINT({lat} {lng})', 4326)

    @staticmethod
    def distance(a, b):
        """
        :param a: object
        :param b: object
        :return: distance(km)
        """
        if isinstance(a, GEOSGeometry) and isinstance(b, GEOSGeometry):
            """
            a = GEOSGeometry(f'POINT(25.0338489 121.5645294)', 4326)
            b = GEOSGeometry(f'POINT(25.0477022 121.5173748)', 4326)
            """
            return str(round(distance(a, b).km, 4))
        elif isinstance(a, tuple) and isinstance(b, tuple):
            """
            a = (25.0338489, 121.5645294)
            b = (25.0477022, 121.5173748)
            """
            a = GEOSGeometry(f'POINT({a[0]} {a[1]})', 4326)
            b = GEOSGeometry(f'POINT({b[0]} {b[1]})', 4326)
            return str(round(distance(a, b).km, 4))
        elif isinstance(a, list) and isinstance(b, list):
            """
            a = [25.0338489, 121.5645294]
            b = [25.0477022, 121.5173748]
            """
            a = GEOSGeometry(f'POINT({a[0]} {a[1]})', 4326)
            b = GEOSGeometry(f'POINT({b[0]} {b[1]})', 4326)
            return str(round(distance(a, b).km, 4))
        else:
            return '0'


"""
from core.services.geo import *
"""