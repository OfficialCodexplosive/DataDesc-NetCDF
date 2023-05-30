import netCDF4 as nc
import numpy as np

# Define the dimensions of the NetCDF file
lat_size = 180
lon_size = 360

# Create a NetCDF4 file
dataset = nc.Dataset('1_netcdf.nc', mode='w', format='NETCDF4')

# Define the lat and lon dimensions
dataset.createDimension('lat', lat_size)
dataset.createDimension('lon', lon_size)

# Define the lat and lon variables
lat = dataset.createVariable('lat', 'f4', ('lat',))
lon = dataset.createVariable('lon', 'f4', ('lon',))

# Set the attributes of the lat and lon variables
lat.units = 'degrees_north'
lat.long_name = 'latitude'
lon.units = 'degrees_east'
lon.long_name = 'longitude'

# Set the values of the lat and lon variables
lat_values = np.arange(-90.0, 90.0, 1.0)
lon_values = np.arange(-180.0, 180.0, 1.0)
lat[:] = lat_values
lon[:] = lon_values

# Define the Temperature variable
temp = dataset.createVariable('Temperature', 'f4', ('lat', 'lon',))

# Set the attributes of the Temperature variable
temp.units = 'Celsius'
temp.description = 'Surface temperature'

# Set the values of the Temperature variable
temp_values = np.random.uniform(low=0.0, high=40.0, size=(lat_size, lon_size))
temp[:] = temp_values

# Close the NetCDF4 file
dataset.close()
