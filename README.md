Corrupted Half
==============

## GeoSpatial Info

### Storing a point:

```python
from decimal import Decimal
from django.contrib.gis.geos import Point

latitude = Decimal(...)
longitude = Decimal(...)

point = Point(longitude, latitude)
```

### Query a point:

```python
from django.contrib.gis.db import models as geoModels
import django.contrib.gis.measure.D

max_distance = 25
ref_point = geoModels.Point({longitude}, {latitude}) # get from geopy

# Example querying for locations <= 25 miles of a lat/long
locations = Location.objects.filter(point__distance_lte=(ref_point, D(mi=max_distance)))
```

> https://speakerdeck.com/pyconslides/location-location-location-by-julia-grace

## Project Setup

## Database Settings

## Deploying to Heroku