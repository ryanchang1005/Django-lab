# Django-PostGIS

#### 安裝

[官網教學](https://docs.djangoproject.com/en/3.1/ref/contrib/gis/install/postgis/#post-installation)
```
# PostgreSQL command
$ createdb  <db name>
$ psql <db name>
> CREATE EXTENSION postgis;

# Django
from django.contrib.postgres.operations import CreateExtension
from django.db import migrations

class Migration(migrations.Migration):

    operations = [
        CreateExtension('postgis'),
        ...
    ]
```

```python
# core/settings.py

INSTALLED_APPS = [
    'django.contrib.gis',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
    }
}
```
#### 目的
* 抓某個點附近N公里的點

#### 設計
```python
# places/models.py
class Place:
    name = CharField()
    position = GeometryField()
```

#### 範例
```
新增places表
create table places(
    name VARCHAR(100)
);

新增欄位
SELECT AddGeometryColumn ('public','places','geom',4326,'POINT',2);

新增資料
INSERT INTO places(name, geom)
VALUES 
('台北101', ST_GeomFromText('POINT(121.5645294 25.0338489)', 4326));

查詢格式(ST_AsKML)
select name, ST_AsKML(geom) from public.places;
台北101	<Point><coordinates>121.564529399999998,25.033848899999999</coordinates></Point>

查詢格式(ST_AsGML)
select name, ST_AsGML(geom) from public.places;
台北101	<gml:Point srsName="EPSG:4326"><gml:coordinates>121.5645294,25.0338489</gml:coordinates></gml:Point>

查詢格式(ST_AsGeoJSON)
select name, ST_AsGeoJSON(geom) from public.places;
台北101	{"type":"Point","coordinates":[121.5645294,25.0338489]}

計算距離(公里)
SELECT ST_Distance(
    ST_GeogFromText('POINT(121.5173748 25.0477022)'), --台北車站
    ST_GeogFromText('POINT(121.5645294 25.0338489)') --台北101
) / 1000;  --5.0000050618300005

根據某個點計算距離
select id, name,
    round(
        (ST_Distance(geom, ST_GeogFromText('POINT(121.539737 25.070699)')) / 1000)::numeric(8, 5),
        4
    ) as distance_km --算距離四捨到小數後4
from places
order by distance_km desc --依照距離遞增/減排序
limit 1; --最近的
========================
id  name        distance_km
1	台北101 	 4.7877
3	台北車站	  3.4031

```