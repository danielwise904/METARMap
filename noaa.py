import numpy as np
import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

plt.figure()
grib='uv.t12z.grbf22.grib2';
grbs=pygrib.open(grib)
grb = grbs.select(name='Significant height of wind waves')[0]
data=grb.values
lat,lon = grb.latlons()