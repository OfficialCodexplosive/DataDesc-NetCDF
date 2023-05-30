import os
import yaml
import netCDF4 as nc

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, '../input/passion.yml')
out_path = os.path.join(base_path, '../output/passion.nc')

def get_value_from_json(json, key):
    if isinstance(json, dict):
        if key in json:
            return json[key]
        for val in json.values():
            res = get_value_from_json(val, key)
            if res is not None:
                return res
    elif isinstance(json, list):
        for item in json:
            res = get_value_from_json(item, key)
            if res is not None:
                return res

# read OpenAPI schema from YAML file
with open(file_path, 'r') as f:
    schema = yaml.safe_load(f)
            
# create NetCDF file
with nc.Dataset(out_path, 'w', format="NETCDF4") as f:
    # check if file contains a NetCDF schema
    netcdf_schema = get_value_from_json(schema, 'x-NetCDFStructure')

    # create dimensions
    for dim_name, dim_props in netcdf_schema['Coordinates'].items():
        f.createDimension(dim_name, None)

    # create variables
    for var_name, var_props in netcdf_schema['Variables'].items():
        var_dims = var_props['Dimensions']
        var_dtype = var_props['DataType']
        #var_data = var_props['Data']

        var = f.createVariable(var_name, var_dtype, var_dims)
        #var = 0 #var[:] = var_data

        # add variable attributes
        if 'Attributes' in var_props:
            for attr_name, attr_value in var_props['Attributes'].items():
                setattr(var, attr_name, attr_value)

    # add global attributes
    for attr_name, attr_value in schema['info'].items():
        setattr(f, attr_name, attr_value)

    # add compression settings
    if 'Compression' in netcdf_schema:
        comp_props = netcdf_schema['Compression']
        f.setncattr('zlib', comp_props['zlib']['example'])
        f.setncattr('shuffle', comp_props['shuffle']['example'])
        f.setncattr('complevel', comp_props['level']['example'])
