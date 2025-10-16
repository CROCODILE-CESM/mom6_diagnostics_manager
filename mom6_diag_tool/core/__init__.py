"""Core functionality for MOM6 diagnostic table generation."""

from .diagnostic import Diagnostic
from .parser import DiagnosticsParser
from .generator import DiagTableGenerator

__all__ = ['Diagnostic', 'DiagnosticsParser', 'DiagTableGenerator']
