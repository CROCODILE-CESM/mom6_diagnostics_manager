# Installation Guide

This guide provides detailed installation instructions for the MOM6 Diagnostic Table Generator, designed for NCAR scientists and climate modelers working with MOM6 ocean model diagnostics.

## Quick Installation

### Option 1: Install from source (Development)

```bash
# Clone the repository
cd /path/to/CESM-diags-generator

# Create and activate conda environment
conda env create -f environment.yml
conda activate mom6-diag-tool

# Install the package in editable mode
pip install -e .
```

### Option 2: Build and install conda package

```bash
# Build the conda package
conda build conda-recipe/

# Install the built package
conda install --use-local mom6-diag-tool
```

### Option 3: Install with pip only

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .

# Or with optional dependencies
pip install -e ".[notebook,dev]"
```

## Verify Installation

After installation, verify everything works:

```bash
# Check the CLI tool
mom6-diag-tool --help

# Test import in Python
python -c "from mom6_diag_tool import DiagnosticsParser; print('Success!')"

# Run tests (if dev dependencies installed)
pytest tests/
```

## Using the Package

### In Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook examples/interactive_diag_table.ipynb
```

### From Python

```python
from mom6_diag_tool import DiagnosticsParser, DiagTableGenerator

parser = DiagnosticsParser('available_diags.000000')
generator = DiagTableGenerator(title="My Case")
```

### From Command Line

```bash
mom6-diag-tool -i available_diags.000000 -o diag_table --case-name MyCase --static-only
```

## Troubleshooting

### Issue: Import errors

**Solution:** Make sure you've activated the correct environment:
```bash
conda activate mom6-diag-tool
```

### Issue: `mom6-diag-tool` command not found

**Solution:** Reinstall the package with pip:
```bash
pip install -e .
```

### Issue: Jupyter widgets not displaying

**Solution:** Enable the widgets extension:
```bash
jupyter nbextension enable --py widgetsnbextension
```

### Issue: Module not found errors

**Solution:** Install missing dependencies:
```bash
pip install pandas ipywidgets IPython
```

## Development Installation

For contributing to the package:

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install

# Run tests
pytest tests/ -v

# Check code style
black mom6_diag_tool/
flake8 mom6_diag_tool/
mypy mom6_diag_tool/
```

## Uninstallation

### If installed with pip

```bash
pip uninstall mom6-diag-tool
```

### If installed with conda

```bash
conda remove mom6-diag-tool
```

### Remove environment

```bash
conda deactivate
conda env remove -n mom6-diag-tool
```

## System Requirements

- Python 3.8 or higher
- 100 MB disk space
- Jupyter notebook (optional, for interactive use)

### Supported Platforms

- Linux (tested on Ubuntu 20.04+)
- macOS (tested on macOS 11+)
- Windows (tested on Windows 10+)

## Dependencies

### Required
- pandas >= 1.3.0
- ipywidgets >= 7.6.0
- IPython >= 7.16.0

### Optional
- jupyter >= 1.0.0 (for notebook interface)
- pytest >= 6.0 (for running tests)
- black >= 21.0 (for code formatting)

## Next Steps

After installation, see:
- [README.md](README.md) for usage examples
- [examples/interactive_diag_table.ipynb](examples/interactive_diag_table.ipynb) for interactive tutorial
- Command-line help: `mom6-diag-tool --help`
