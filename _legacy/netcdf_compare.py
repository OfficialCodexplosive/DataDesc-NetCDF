import yaml
from netCDF4 import Dataset

# Load the YAML schema
with open('result.yml') as f:
    schema = yaml.safe_load(f)

# Open the NetCDF file
nc_file = Dataset('example.nc', 'r')

# Check if the dimensions in the YAML schema match the dimensions in the NetCDF file
for dim_name, dim_props in schema["components"]["schemas"]["NetCDF"]["properties"]['dimensions'].items():
    if dim_name in nc_file.dimensions:
        nc_dim = nc_file.dimensions[dim_name]
        if nc_dim.size != dim_props['size']:
            print(f"ERROR: Dimension '{dim_name}' size mismatch: schema size={dim_props['size']}, NetCDF size={nc_dim.size}")
    else:
        print(f"ERROR: Dimension '{dim_name}' not found in NetCDF file")

# Check if the variables in the YAML schema match the variables in the NetCDF file
for var_name, var_props in schema["components"]["schemas"]["NetCDF"]["properties"]['variables']['items']['properties'].items():
    if var_name in nc_file.variables:
        nc_var = nc_file.variables[var_name]
        if nc_var.dtype.str != var_props['type']:
            print(f"ERROR: Variable '{var_name}' data type mismatch: schema dtype={var_props['type']}, NetCDF dtype={nc_var.dtype.str}")
        if len(nc_var.dimensions) != len(var_props['dimensions']):
            print(f"ERROR: Variable '{var_name}' dimensions mismatch: schema dimensions={var_props['dimensions']}, NetCDF dimensions={nc_var.dimensions}")
        else:
            for i, dim_name in enumerate(var_props['dimensions']):
                nc_dim_name = nc_var.dimensions[i]
                if dim_name != nc_dim_name:
                    print(f"ERROR: Variable '{var_name}' dimensions mismatch: schema dimensions={var_props['dimensions']}, NetCDF dimensions={nc_var.dimensions}")
    else:
        print(f"ERROR: Variable '{var_name}' not found in NetCDF file")

# Close the NetCDF file
nc_file.close()
