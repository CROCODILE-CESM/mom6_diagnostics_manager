# Examples

This directory contains example notebooks and data files to help you get started with the MOM6 Diagnostic Table Generator.

## Interactive Notebook

### `interactive_diag_table.ipynb`

The main interactive notebook for creating and configuring MOM6 `diag_table` files.

**Features:**
- Modern, user-friendly interface
- Search and filter diagnostics
- Category-based organization
- Live preview of output
- One-click export

**How to use:**
```bash
# Navigate to examples directory
cd examples

# Launch Jupyter
jupyter notebook interactive_diag_table.ipynb

# Follow the in-notebook instructions
```

**Workflow:**
1. **Load Data** - The notebook uses `data/sample_available_diags.000000` by default
2. **Set Case Name** - Enter your CESM case identifier
3. **Add Output Files** - Create files for different frequencies (daily, monthly, etc.)
4. **Select Diagnostics** - Use checkboxes to add fields to each file
5. **Preview** - Review your configuration
6. **Export** - Save your `diag_table`

## Data Directory

### `data/sample_available_diags.000000`

A sample `available_diags` file from MOM6 containing ~788 diagnostic fields.

This file is automatically used by the example notebook, but you can replace the path in the notebook with your own `available_diags` file.

**To use your own data:**
1. Locate your `available_diags.000000` file from a MOM6 run
2. Update the `DIAG_FILE` path in cell 3 of the notebook
3. Re-run the data loading cell

## Quick Start Example

Here's a minimal Python example without the notebook:

```python
from mom6_diag_tool import DiagnosticsParser, DiagTableGenerator

# Parse your available_diags file
parser = DiagnosticsParser('data/sample_available_diags.000000')

# Create generator
generator = DiagTableGenerator(
    title="MOM6 diagnostic fields table for CESM case: MyCase",
    base_year=1900
)

# Add a static file
generator.add_file('ocean_static', -1, 'days')

# Add some diagnostics
for field_name in ['geolon', 'geolat', 'deptho']:
    generator.add_field(
        module_name='ocean_model',
        field_name=field_name,
        file_name='ocean_static',
        reduction_method='.false.'
    )

# Add a daily output file
generator.add_file(
    'ocean_daily',
    output_freq=1,
    output_freq_units='days',
    new_file_freq=1,
    new_file_freq_units='months'
)

# Add time-varying diagnostics
for field_name in ['SSH', 'SST', 'SSS']:
    generator.add_field(
        module_name='ocean_model',
        field_name=field_name,
        file_name='ocean_daily',
        reduction_method='mean'
    )

# Save the diag_table
generator.save('my_diag_table')
print("diag_table created!")
```

## More Examples

### Example 1: Static Fields Only

```python
from mom6_diag_tool import DiagnosticsParser, DiagTableGenerator

parser = DiagnosticsParser('data/sample_available_diags.000000')
generator = DiagTableGenerator(title="Static Fields Only")

generator.add_file('ocean_static', -1, 'days')

# Get all static/grid diagnostics
categories = parser.get_by_category()
for diag in categories.get('Grid & Static', []):
    generator.add_field(
        'ocean_model',
        diag.name,
        'ocean_static',
        reduction_method='.false.'
    )

generator.save('diag_table_static')
```

### Example 2: Surface Properties

```python
from mom6_diag_tool import DiagnosticsParser, DiagTableGenerator

parser = DiagnosticsParser('data/sample_available_diags.000000')
generator = DiagTableGenerator(title="Surface Diagnostics")

# Daily surface output
generator.add_file('ocean_daily', 1, 'days', new_file_freq=1, new_file_freq_units='months')

# Get all surface property diagnostics
categories = parser.get_by_category()
for diag in categories.get('Surface Properties', []):
    if diag.is_2d():  # Only 2D fields
        generator.add_field(
            'ocean_model',
            diag.name,
            'ocean_daily',
            reduction_method='mean'
        )

generator.save('diag_table_surface')
```

### Example 3: Multi-File Configuration

```python
from mom6_diag_tool import DiagnosticsParser, DiagTableGenerator

parser = DiagnosticsParser('data/sample_available_diags.000000')
generator = DiagTableGenerator(title="Complete Configuration")

# Add multiple output files
files_config = [
    ('ocean_static', -1, 'days', None, None),
    ('ocean_daily', 1, 'days', 1, 'months'),
    ('ocean_monthly', 1, 'months', 1, 'years'),
]

for file_name, freq, units, new_freq, new_units in files_config:
    generator.add_file(file_name, freq, units, new_file_freq=new_freq, new_file_freq_units=new_units)

# Add diagnostics to appropriate files
static_fields = ['geolon', 'geolat', 'deptho']
daily_fields = ['SSH', 'SST', 'SSS']
monthly_fields = ['temp', 'salt', 'u', 'v']

for field in static_fields:
    generator.add_field('ocean_model', field, 'ocean_static', reduction_method='.false.')

for field in daily_fields:
    generator.add_field('ocean_model', field, 'ocean_daily', reduction_method='mean')

for field in monthly_fields:
    generator.add_field('ocean_model', field, 'ocean_monthly', reduction_method='mean')

generator.save('diag_table_complete')
```

## Customization

You can customize the notebook interface by modifying:
- Case name and base year
- Default module names
- Reduction methods
- File naming conventions
- Search/filter defaults

## Tips

1. **Use the search**: Type keywords to quickly find diagnostics
2. **Filter by dimension**: Use 2D/3D filter to narrow down options
3. **Categories are smart**: Diagnostics are automatically categorized
4. **Preview before export**: Always check your configuration
5. **Static files**: Files with 'static' in the name auto-configure to freq=-1
6. **Date formatting**: Use `%4yr-%2mo-%2dy` in filenames for automatic date stamping

## Troubleshooting

**Issue: Notebook doesn't display widgets**
```bash
jupyter nbextension enable --py widgetsnbextension
```

**Issue: Can't find the data file**
- Make sure you're running from the `examples/` directory
- Or update the `DIAG_FILE` path to an absolute path

**Issue: Import errors**
```bash
# Make sure package is installed
pip install -e ..
```

## Further Reading

- [Main README](../README.md) - Full package documentation
- [Installation Guide](../INSTALL.md) - Detailed installation instructions
- [CHANGELOG](../CHANGELOG.md) - Version history and updates

## Contributing

Found a bug or have an idea for improvement? Please open an issue or submit a pull request!

---

**Happy diagnostic configuring!**
