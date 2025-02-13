import ee
import geemap


# Define the image collection
image_collection = ee.ImageCollection('GOOGLE/Research/open-buildings-temporal/v1')

# Define the scale in meters
SCALE_M = 1  # For larger AOIs, reduce at larger scale to avoid OOM issues.

# Define the Area of Interest (AOI)
# Replace with your own geometry or feature collection
aoi = ee.Geometry.Rectangle([xmin, ymin, xmax, ymax])  # Replace with your AOI coordinates

# Iterate over the years from 2016 to 2023
for year in range(2016, 2024):
    # Define the epoch time in seconds
    epoch_s = ee.Date.fromYMD(year, 6, 30).millis().divide(1000)
    
    # Filter the image collection for the specific year and mosaic the images
    mosaic = image_collection.filter(ee.Filter.eq('inference_time_epoch_s', epoch_s)).mosaic()
    
    # Calculate the building count for the AOI
    count = mosaic.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=aoi,
        scale=SCALE_M,
        crs=aoi.projection()
    ).getNumber('building_fractional_count') \
     .multiply(ee.Number(SCALE_M * 2).pow(2))
    
    # Add the mosaic layer to the map
    geemap.addLayer(mosaic.select('building_presence'), {'min': 0, 'max': 1}, str(year))
    
    # Print the building count for the year
    print(f'Building count for year {year}: {count.getInfo()}')