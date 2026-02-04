"""
PaperAssist: Academic Paper Analysis Tool

Extract equations from PDF papers, assess citation value,
and automatically generate research logs for Claude Code agent.
"""

__version__ = "0.1.0"
__author__ = "PaperAssist Team"

from .extract_text import extract_text, extract_text_to_string
from .extract_equations import extract_equations
from .compare_papers import compare_papers
from .install import install_agent, uninstall_agent, check_status

__all__ = [
    "extract_text",
    "extract_text_to_string",
    "extract_equations",
    "compare_papers",
    "install_agent",
    "uninstall_agent",
    "check_status",
    "__version__",
]
