import netCDF4 as nc
import yaml
import os


base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, '../output/passion.nc')

# Open the NetCDF file
nc_file = nc.Dataset(file_path, 'r')

# Get the dimension names and sizes
dimensions = {}
for dim_name, dim in nc_file.dimensions.items():
    dimensions[dim_name] = {'size': dim.size}

# Get the variable names, types, dimensions, and attributes
variables = []
for var_name, var in nc_file.variables.items():
    variable = {'name': var_name, 'dtype': str(var.dtype)}
    variable['dimensions'] = [dim_name for dim_name in var.dimensions]
    variable['attributes'] = {}
    for attr_name in var.ncattrs():
        variable['attributes'][attr_name] = str(var.getncattr(attr_name))
    variables.append(variable)

# Create the OpenAPI schema dictionary
schema = {
    'openapi': '3.0.0',
    'info': {
        'title': 'NetCDF File Schema',
        'version': '1.0.0'
    },
    'components': {
        'schemas': {
            'NetCDF': {
                'type': 'object',
                'properties': {
                    'format': {'type': 'string', 'description': 'The format of the NetCDF file.', 'example': 'NETCDF4'},
                    'dimensions': {'type': 'object', 'description': 'The dimensions of the NetCDF file.', 'properties' : {}},
                    'variables': {'type': 'array', 'description': 'The variables of the NetCDF file.', 'items' : { 'properties' : {} } }
                }
            }
        }
    }
}

# Add the dimension information to the schema
for dim_name, dim_info in dimensions.items():
    schema['components']['schemas']['NetCDF']['properties']['dimensions']['properties'][dim_name] = {
        'type': 'object',
        'properties': {
            'size': {'type': 'integer', 'description': 'The size of the ' + dim_name + ' dimension.', 'example': dim_info['size']}
        }
    }
    #schema['components']['schemas']['NetCDF']['properties']['dimensions']['properties'][dim_name].update(dim_info)

# Add the variable information to the schema
for variable in variables:
    print(variable)
    schema['components']['schemas']['NetCDF']['properties']['variables']['items']['properties'][variable['name']] = {
        'type': 'object',
        'properties': {
            'dtype': {'type': 'string', 'description': 'The data type of the ' + variable['name'] + ' variable.', 'example': variable['dtype']},
            'dimensions': {'type': 'array', 'description': 'The dimensions of the ' + variable['name'] + ' variable.'},
            'attributes': {'type': 'object', 'description': 'The attributes of the ' + variable['name'] + ' variable.'},
            'data': {'type': 'array', 'description': 'The data of the ' + variable['name'] + ' variable.', 'items' : {} }
        }
    }
    schema['components']['schemas']['NetCDF']['properties']['variables']['items']['properties'][variable['name']]['properties']['dimensions']['items'] = {'type': 'string', 'example': variable['dimensions']}
    schema['components']['schemas']['NetCDF']['properties']['variables']['items']['properties'][variable['name']]['properties']['attributes']['properties'] = {'example': variable['attributes']}

    # Fill example field with NetCDF data
    if("data" in variable.keys()):
        schema['components']['schemas']['NetCDF']['properties']['variables']['items']['properties'][variable['name']]['properties']['data']['items'] = {'type': 'number', 'example': variable['data'].tolist()}

with open('2_netcdfAsYaml.yml', 'w') as yaml_file:
    yaml.dump(schema, yaml_file, default_flow_style=False)
