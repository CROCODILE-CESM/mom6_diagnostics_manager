"""Parser for MOM6 available_diags files."""

import re
import pickle
import os
from typing import Dict, List
from .diagnostic import Diagnostic


class DiagnosticsParser:
    """Parser for available_diags files from MOM6.

    This class parses the text output from MOM6's available_diags file
    which lists all available diagnostic fields and their metadata.

    Attributes:
        filepath: Path to the available_diags file
        diagnostics: Dictionary mapping diagnostic names to Diagnostic objects
    """

    def __init__(self, filepath: str, use_cache: bool = True):
        """Initialize parser and parse the file.

        Args:
            filepath: Path to the available_diags file
            use_cache: If True, use pickle cache for faster loading
        """
        self.filepath = filepath
        self.diagnostics: Dict[str, Diagnostic] = {}
        self.use_cache = use_cache
        self._cache_path = filepath + '.cache'

        # Try to load from cache first
        if use_cache and self._load_from_cache():
            return

        # Otherwise parse the file
        self._parse()

        # Save to cache for next time
        if use_cache:
            self._save_to_cache()

    def _parse(self):
        """Parse the available_diags file."""
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        current_diag = None

        for line in lines:
            line = line.strip()

            # Check for diagnostic name
            if line.startswith('"') and '[' in line:
                match = re.match(r'"([^"]+)"\s+\[(Used|Unused)\]', line)
                if match:
                    name = match.group(1)
                    used = match.group(2) == "Used"
                    current_diag = Diagnostic(name=name, used=used)
                    self.diagnostics[name] = current_diag

            # Parse metadata
            elif line.startswith('!') and current_diag:
                self._parse_metadata(line, current_diag)

    def _parse_metadata(self, line: str, diag: Diagnostic):
        """Parse metadata line.

        Args:
            line: Metadata line starting with '!'
            diag: Diagnostic object to update
        """
        line = line.lstrip('! ').strip()

        if line.startswith('modules:'):
            modules_str = line.split(':', 1)[1].strip()
            match = re.search(r'\{([^}]+)\}', modules_str)
            if match:
                diag.modules = [m.strip() for m in match.group(1).split(',')]
            else:
                diag.modules = [modules_str.strip()]
        elif line.startswith('dimensions:'):
            diag.dimensions = line.split(':', 1)[1].strip()
        elif line.startswith('long_name:'):
            diag.long_name = line.split(':', 1)[1].strip()
        elif line.startswith('units:'):
            diag.units = line.split(':', 1)[1].strip()
        elif line.startswith('standard_name:'):
            diag.standard_name = line.split(':', 1)[1].strip()
        elif line.startswith('cell_methods:'):
            diag.cell_methods = line.split(':', 1)[1].strip()
        elif line.startswith('variants:'):
            variants_str = line.split(':', 1)[1].strip()
            match = re.search(r'\{([^}]+)\}', variants_str)
            if match:
                diag.variants = [v.strip() for v in match.group(1).split(',')]

    def _load_from_cache(self) -> bool:
        """Load diagnostics from pickle cache if available and valid.

        Returns:
            True if cache was loaded successfully, False otherwise
        """
        try:
            # Check if cache exists
            if not os.path.exists(self._cache_path):
                return False

            # Check if cache is newer than source file
            cache_mtime = os.path.getmtime(self._cache_path)
            source_mtime = os.path.getmtime(self.filepath)

            if cache_mtime < source_mtime:
                # Cache is outdated
                return False

            # Load from cache
            with open(self._cache_path, 'rb') as f:
                self.diagnostics = pickle.load(f)

            return True

        except Exception:
            # If anything goes wrong, just parse normally
            return False

    def _save_to_cache(self):
        """Save diagnostics to pickle cache."""
        try:
            with open(self._cache_path, 'wb') as f:
                pickle.dump(self.diagnostics, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:
            # Silently ignore cache save errors
            pass

    def get_by_category(self) -> Dict[str, List[Diagnostic]]:
        """Organize diagnostics by common categories.

        Returns:
            Dictionary mapping category names to lists of Diagnostic objects
        """
        categories = {
            'Temperature & Salinity': [],
            'Velocity & Transport': [],
            'Surface Properties': [],
            'Mixing & Diffusion': [],
            'Sea Ice': [],
            'Tracers': [],
            'Grid & Static': [],
            'Other': []
        }

        for diag in self.diagnostics.values():
            name_lower = diag.name.lower()
            long_name_lower = diag.long_name.lower()

            if any(x in name_lower for x in ['temp', 'thetao', 'theta', 'salt', 'so', 'ptemp']):
                categories['Temperature & Salinity'].append(diag)
            elif any(x in name_lower for x in ['vel', 'uo', 'vo', 'wo', 'umo', 'vmo', 'speed']):
                categories['Velocity & Transport'].append(diag)
            elif any(x in name_lower for x in ['ssh', 'tos', 'sos', 'sst', 'sss', 'mld', 'mlotst']):
                categories['Surface Properties'].append(diag)
            elif any(x in name_lower for x in ['kd', 'kv', 'mix', 'diff', 'visc']):
                categories['Mixing & Diffusion'].append(diag)
            elif any(x in name_lower for x in ['ice', 'frazil']):
                categories['Sea Ice'].append(diag)
            elif any(x in name_lower for x in ['tracer', 'age', 'dye']):
                categories['Tracers'].append(diag)
            elif any(x in name_lower for x in ['geo', 'depth', 'area', 'wet', 'mask', 'grid']):
                categories['Grid & Static'].append(diag)
            else:
                categories['Other'].append(diag)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
