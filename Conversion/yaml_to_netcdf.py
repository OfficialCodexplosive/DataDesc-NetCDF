import os
import yaml
import netCDF4 as nc

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, '../2_netcdfAsYaml.yml')

# read OpenAPI schema from YAML file
with open(file_path, 'r') as f:
    schema = yaml.safe_load(f)

# create NetCDF file
with nc.Dataset('3_netcdfFromYaml.nc', 'w', format=schema['components']['schemas']['NetCDF']['properties']['format']['example']) as f:
    # create dimensions
    for dim_name, dim_props in schema['components']['schemas']['NetCDF']['properties']['dimensions']['properties'].items():
        f.createDimension(dim_name, dim_props['properties']['size']['example'])

    # create variables
    for var_name, var_props in schema['components']['schemas']['NetCDF']['properties']['variables']['items']['properties'].items():
        var_dims = var_props['properties']['dimensions']['items']['example']
        var_dtype = var_props['properties']['dtype']['example']
        var_data = var_props['properties']['data']['items']

        var = f.createVariable(var_name, var_dtype, var_dims)
        var = 0 #var[:] = var_data

        # add variable attributes
        if 'attributes' in var_props:
            for attr_name, attr_value in var_props['attributes']['properties'].items():
                setattr(var, attr_name, attr_value['example'])

    # add global attributes
    for attr_name, attr_value in schema['info'].items():
        setattr(f, attr_name, attr_value)

    # add compression settings
    if 'compression' in schema['components']['schemas']['NetCDF']['properties']:
        comp_props = schema['components']['schemas']['NetCDF']['properties']['compression']['properties']
        f.setncattr('zlib', comp_props['zlib']['example'])
        f.setncattr('shuffle', comp_props['shuffle']['example'])
        f.setncattr('complevel', comp_props['level']['example'])
