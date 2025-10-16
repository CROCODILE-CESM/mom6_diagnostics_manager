<div align="center">

# MOM6 Diagnostic Table Generator

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**An interactive tool for creating `diag_table` files from MOM6's `available_diags` output**

*Designed for NCAR scientists and climate modelers*

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#usage-examples) • [Contributing](#contributing)

</div>

---

## Overview

This package provides both a user-friendly Jupyter notebook interface and command-line tools for configuring MOM6 diagnostic outputs. Say goodbye to manually editing `diag_table` files and hello to an intuitive, visual workflow!

## Features

- **Interactive Jupyter Interface**: Visual interface for selecting and configuring diagnostics
- **Smart Organization**: Diagnostics automatically categorized by type (Temperature, Velocity, Surface Properties, etc.)
- **Search & Filter**: Quickly find diagnostics by name, category, or dimension (2D/3D)
- **Multiple Output Files**: Configure different output frequencies (daily, monthly, static, etc.)
- **Preview & Export**: Preview your diag_table before exporting
- **Command-Line Tools**: Scriptable CLI for automation and batch processing

## Installation

### Using conda (recommended)

```bash
# Create a new conda environment
conda env create -f environment.yml
conda activate mom6-diag-tool

# Install the package
pip install -e .
```

### Using pip

```bash
# Install from source
pip install -e .

# Or with optional dependencies
pip install -e ".[notebook,dev]"
```

### Building conda package

```bash
# Build the conda package
conda build conda-recipe/

# Install the built package
conda install --use-local mom6-diag-tool
```

## Quick Start

### Interactive Jupyter Notebook

1. Start Jupyter:
   ```bash
   jupyter notebook examples/interactive_diag_table.ipynb
   ```

2. Follow the notebook workflow:
   - Load your `available_diags` file
   - Set your CESM case name
   - Add output files (daily, monthly, static, etc.)
   - Select diagnostics using checkboxes
   - Preview and export your `diag_table`

### Command-Line Interface

```bash
# Generate a diag_table with static fields only
mom6-diag-tool -i available_diags.000000 -o diag_table --case-name NWA12 --static-only

# List all available diagnostics
mom6-diag-tool -i available_diags.000000 --list-diagnostics

# List diagnostics by category
mom6-diag-tool -i available_diags.000000 --list-categories
```

## Usage Examples

### Python API

```python
from mom6_diag_tool import DiagnosticsParser, DiagTableGenerator

# Parse available_diags file
parser = DiagnosticsParser('available_diags.000000')

# Create generator
generator = DiagTableGenerator(
    title="MOM6 diagnostic fields table for CESM case: NWA12",
    base_year=1900
)

# Add output files
generator.add_file('ocean_static', -1, 'days')
generator.add_file('ocean_daily', 1, 'days', new_file_freq=1, new_file_freq_units='months')

# Add diagnostic fields
generator.add_field(
    module_name='ocean_model',
    field_name='SSH',
    file_name='ocean_daily',
    reduction_method='mean'
)

# Generate and save
generator.save('diag_table')
```

### Interactive UI

```python
from mom6_diag_tool import DiagnosticsParser, DiagTableGenerator, DiagTableUI

# Parse diagnostics
parser = DiagnosticsParser('available_diags.000000')

# Create generator
generator = DiagTableGenerator(
    title="MOM6 diagnostic fields table for CESM case: NWA12"
)

# Create and display UI
ui = DiagTableUI(parser, generator)
ui.create_ui()
```

## Project Structure

```
CESM-diags-generator/
├── mom6_diag_tool/           # Main package
│   ├── __init__.py
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── diagnostic.py     # Diagnostic data structures
│   │   ├── parser.py         # Parser for available_diags
│   │   └── generator.py      # diag_table generator
│   ├── ui/                   # User interface
│   │   ├── __init__.py
│   │   └── interactive.py    # Jupyter widget interface
│   └── cli/                  # Command-line interface
│       ├── __init__.py
│       └── main.py           # CLI entry point
├── examples/                 # Example notebooks
│   └── interactive_diag_table.ipynb
├── tests/                    # Unit tests
├── conda-recipe/             # Conda package recipe
│   ├── meta.yaml
│   ├── build.sh
│   └── bld.bat
├── setup.py                  # Package setup
├── pyproject.toml            # Modern Python packaging config
├── environment.yml           # Conda environment
└── README.md                 # This file
```

## MOM6 diag_table Format

The `diag_table` file has two main sections:

1. **File Section**: Defines output files and their frequencies
   ```
   "ocean_daily", 1, "days", 1, "days", "time", 1, "months"
   ```

2. **Field Section**: Specifies which diagnostics to output
   ```
   "ocean_model", "SSH", "SSH", "ocean_daily", "all", "mean", "none", 2
   ```

## Diagnostic Categories

The tool organizes diagnostics into categories:
- **Temperature & Salinity**: Ocean T/S fields
- **Velocity & Transport**: Current velocities and transports
- **Surface Properties**: SSH, SST, SSS, mixed layer depth
- **Mixing & Diffusion**: Mixing coefficients and diffusion
- **Sea Ice**: Ice-related diagnostics
- **Tracers**: Passive tracers, age, dyes
- **Grid & Static**: Grid geometry, bathymetry, masks
- **Other**: Miscellaneous diagnostics

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black mom6_diag_tool/
flake8 mom6_diag_tool/
mypy mom6_diag_tool/
```

### Building Documentation

```bash
# TODO: Add sphinx documentation
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Citation

If you use this tool in your research, please cite:

```
@software{mom6_diag_tool,
  author = {Meza, Anthony},
  title = {MOM6 Diagnostic Table Generator},
  year = {2025},
  note = {Tool for NCAR scientists and MOM6 modelers},
  url = {https://github.com/anthonymeza/CESM-diags-generator}
}
```

## Acknowledgments

- MOM6 Development Team
- CESM Community
- NOAA/GFDL

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/anthonymeza/CESM-diags-generator/issues
- Email: Anthony Meza (author/maintainer)

## Changelog

### Version 0.1.0 (Initial Release)
- Interactive Jupyter notebook interface
- Command-line tools
- Support for all MOM6 diagnostic types
- Category-based organization
- Search and filtering capabilities
- Preview and export functionality
