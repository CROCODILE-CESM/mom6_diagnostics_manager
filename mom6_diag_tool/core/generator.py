"""Generator for MOM6 diag_table files."""

from pathlib import Path
from typing import List, Dict, Optional


class DiagTableGenerator:
    """Generator for MOM6 diag_table files.

    This class constructs a properly formatted diag_table file
    for MOM6 that specifies which diagnostic fields to output
    and at what frequency.

    Attributes:
        title: Title for the diag_table
        base_year: Base year for time axis
        base_month: Base month for time axis
        base_day: Base day for time axis
        files: List of file definitions
        fields: List of field definitions
    """

    def __init__(self, title: str = "MOM6 Simulation",
                 base_year: int = 1900, base_month: int = 1, base_day: int = 1):
        """Initialize the generator.

        Args:
            title: Title for the diag_table
            base_year: Base year for time axis (default: 1900)
            base_month: Base month for time axis (default: 1)
            base_day: Base day for time axis (default: 1)
        """
        self.title = title
        self.base_year = base_year
        self.base_month = base_month
        self.base_day = base_day
        self.files: List[Dict] = []
        self.fields: List[Dict] = []

    def clear(self):
        """Clear all files and fields."""
        self.files = []
        self.fields = []

    def add_file(self, file_name: str, output_freq: int, output_freq_units: str = "days",
                 file_format: int = 1, time_axis_units: str = "days",
                 time_axis_name: str = "time", new_file_freq: Optional[int] = None,
                 new_file_freq_units: Optional[str] = None) -> Dict:
        """Add file definition.

        Args:
            file_name: Name of output file (can include date formatting like %4yr-%2mo-%2dy)
            output_freq: Frequency of output
            output_freq_units: Units for output frequency ('hours', 'days', 'months', 'years')
            file_format: Output file format (1=netCDF)
            time_axis_units: Units for time axis
            time_axis_name: Name of time axis variable
            new_file_freq: Optional frequency to create new files (for date formatting)
            new_file_freq_units: Optional units for new file frequency

        Returns:
            Dictionary containing the file definition
        """
        # Check if file already exists
        for f in self.files:
            if f['file_name'] == file_name:
                return f

        file_def = {
            'file_name': file_name,
            'output_freq': output_freq,
            'output_freq_units': output_freq_units,
            'file_format': file_format,
            'time_axis_units': time_axis_units,
            'time_axis_name': time_axis_name,
            'new_file_freq': new_file_freq,
            'new_file_freq_units': new_file_freq_units
        }
        self.files.append(file_def)
        return file_def

    def add_field(self, module_name: str, field_name: str, file_name: str,
                  output_name: Optional[str] = None, time_sampling: str = "all",
                  reduction_method: str = "none", regional_section: str = "none",
                  packing: int = 2) -> Dict:
        """Add field definition.

        Args:
            module_name: Name of the module ('ocean_model', 'ocean_model_z', etc.)
            field_name: Name of the diagnostic field
            file_name: Name of output file to write to
            output_name: Name in output file (defaults to field_name)
            time_sampling: Time sampling method ('all', 'snapshot')
            reduction_method: Reduction method ('none', 'mean', 'min', 'max', 'sum', '.false.')
            regional_section: Regional section coordinates or 'none'
            packing: Packing precision (1=double, 2=float, 4=short, 8=byte)

        Returns:
            Dictionary containing the field definition
        """
        if output_name is None:
            output_name = field_name

        # Check if field already exists in this file
        for f in self.fields:
            if f['field_name'] == field_name and f['file_name'] == file_name:
                return f

        field_def = {
            'module_name': module_name,
            'field_name': field_name,
            'output_name': output_name,
            'file_name': file_name,
            'time_sampling': time_sampling,
            'reduction_method': reduction_method,
            'regional_section': regional_section,
            'packing': packing
        }
        self.fields.append(field_def)
        return field_def

    def remove_field(self, field_name: str, file_name: str):
        """Remove a field from a specific file.

        Args:
            field_name: Name of the diagnostic field
            file_name: Name of the file to remove it from
        """
        self.fields = [f for f in self.fields
                       if not (f['field_name'] == field_name and f['file_name'] == file_name)]

    def get_fields_for_file(self, file_name: str) -> List[Dict]:
        """Get all fields for a specific file.

        Args:
            file_name: Name of the file

        Returns:
            List of field definitions for this file
        """
        return [f for f in self.fields if f['file_name'] == file_name]

    def generate(self) -> str:
        """Generate diag_table content.

        Returns:
            String containing the complete diag_table file content
        """
        lines = []

        # Title section
        lines.append(self.title)
        lines.append(f'{self.base_year}  {self.base_month}  {self.base_day}  0  0  0')

        # File section header
        lines.append('### Section-1: File List')
        lines.append('#========================')

        # File sections
        for file_def in self.files:
            file_line = f'"{file_def["file_name"]}", {file_def["output_freq"]}, "{file_def["output_freq_units"]}", {file_def["file_format"]}, "{file_def["time_axis_units"]}", "{file_def["time_axis_name"]}"'

            if file_def['new_file_freq'] is not None:
                file_line += f', {file_def["new_file_freq"]}, "{file_def["new_file_freq_units"]}"'

            lines.append(file_line)

        lines.append('')

        # Field section header
        lines.append('### Section-2: Fields List')
        lines.append('#=========================')

        # Group fields by file for better organization
        files_with_fields = {}
        for field_def in self.fields:
            fname = field_def['file_name']
            if fname not in files_with_fields:
                files_with_fields[fname] = []
            files_with_fields[fname].append(field_def)

        # Field sections (organized by file)
        for fname, fields in files_with_fields.items():
            lines.append(f'# "{fname}"')
            for field_def in fields:
                field_line = f'"{field_def["module_name"]}", "{field_def["field_name"]}", "{field_def["output_name"]}", "{field_def["file_name"]}", "{field_def["time_sampling"]}", "{field_def["reduction_method"]}", "{field_def["regional_section"]}", {field_def["packing"]}'
                lines.append(field_line)
            lines.append('')

        return '\n'.join(lines)

    def save(self, filepath: str) -> str:
        """Save diag_table to file.

        Args:
            filepath: Path where to save the diag_table file

        Returns:
            Path to the saved file
        """
        content = self.generate()
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
