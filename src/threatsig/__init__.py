"""
Threat vs. Signature Explorer.

Small toolkit to explore synthetic ship signatures versus
simplified radar and sonar threat models.
"""

from . import config
from . import data
from . import models
from . import reporting
from . import analysis
from . import cli

__all__ = ["config", "data", "models", "reporting", "analysis", "cli"]