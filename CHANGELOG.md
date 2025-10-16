# Changelog

All notable changes to the MOM6 Diagnostic Table Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-XX

### Added
- Initial release of MOM6 Diagnostic Table Generator
- Interactive Jupyter notebook interface with modern UI
- Command-line tools for automation
- Core functionality:
  - Parse `available_diags` files from MOM6
  - Generate `diag_table` configuration files
  - Smart categorization of diagnostics (Temperature, Velocity, Surface, etc.)
  - 2D/3D filtering capabilities
  - Search and filter diagnostics
  - Live preview of diag_table output
  - Multiple output file support (static, daily, monthly, etc.)
- Comprehensive test suite with pytest
- Documentation:
  - README with usage examples
  - INSTALL guide for various platforms
  - Example notebook with step-by-step instructions
- Package distribution:
  - PyPI-ready setup
  - Conda package recipe
  - Development installation support

### Features
- **Interactive UI**:
  - Modern gradient-based styling
  - Responsive layout with left/right panels
  - Real-time diagnostic selection
  - Built-in help documentation
  - Case name configuration
  - File frequency management

- **Diagnostic Management**:
  - Automatic parsing of MOM6 available_diags format
  - Category-based organization
  - Dimension-based filtering (2D/3D)
  - Search by name or description
  - Bulk selection/deselection

- **Configuration Options**:
  - Multiple output files with different frequencies
  - Customizable reduction methods (mean, max, min, etc.)
  - Regional output support
  - Module selection (ocean_model, ocean_model_z, etc.)
  - Date formatting for file names

- **Export & Preview**:
  - Live preview of diag_table
  - One-click save functionality
  - Standard MOM6 diag_table format
  - Organized by file sections

### Target Audience
- NCAR scientists working with MOM6
- Climate modelers using CESM
- Ocean model developers
- Research scientists configuring diagnostic outputs

### System Requirements
- Python 3.8+
- pandas >= 1.3.0
- ipywidgets >= 7.6.0
- IPython >= 7.16.0
- Jupyter Notebook (optional, for interactive use)

### Tested Platforms
- macOS 11+
- Linux (Ubuntu 20.04+, CentOS 7+)
- NCAR Casper/Derecho (planned)

## [Unreleased]

### Planned Features
- Template system for common diagnostic configurations
- Export to other formats (YAML, JSON)
- Integration with MOM6 parameter files
- Validation of diagnostic combinations
- Web-based interface option
- Pre-configured diagnostic bundles (e.g., "Standard Ocean", "Biogeochemistry")
- Comparison tool for different diag_table configurations
- Performance estimation based on selected diagnostics

### Known Issues
- Large available_diags files (>1000 diagnostics) may slow down the UI
- Preview in Jupyter sometimes requires running cell twice
- Date formatting validation not yet implemented

## Contributing

See [README.md](README.md#contributing) for contribution guidelines.

## Authors

- Anthony Meza - Initial work and maintenance

## Acknowledgments

- MOM6 Development Team at GFDL/NOAA
- CESM Community
- NCAR Scientists for feedback and testing
