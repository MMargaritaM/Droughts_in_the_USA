"""
geotools.py
Spring 2022 PJW

A few tools for working with geopandas objects.
"""

import shapely
import shutil
import time

def make_valid(geodata,quiet=False):
    """
    Correct invalid geometries in a GeoSeries or GeoDataFrame. Revisions
    are done in place.

    Parameters
    ----------
    geodata : GeoSeries or GeoDataFrame
        Object to be made valid

    quiet: bool
        When True, suppress message giving number of fixed geometries.

    Returns
    -------
       Returns the revised object for convenience.
    """

    #  Find invalid geometries

    is_ok = geodata.is_valid

    if is_ok.all():
        return geodata

    is_bad = is_ok == False

    #  Correct them

    n = is_bad.sum()
    print(f'Correcting {n} invalid geometries')

    def fix(geom):
        return shapely.validation.make_valid(geom)

    geodata.geometry[is_bad] = geodata.geometry[is_bad].apply(fix)

    return geodata

def to_shapefile(geodata,zipname):
    """
    Write a GeoDataFrame out as shapefile and then zip the result.

    Parameters
    ----------
        geodata : GeoSeries or GeoDataFrame
            Object to be saved

        zipname : str
            Name to use for the resulting zip file.
    """

    #  Get the stem of the zip name

    stem = zipname.replace('.zip','')

    #  Create the shapefile in a subdirectory named by the stem

    geodata.to_file( stem )

    #  Zip it

    shutil.make_archive(stem,'zip',stem)

    #  Wait for a second to make sure file is closed, then delete
    #  the directory

    time.sleep(1)
    shutil.rmtree(stem)
