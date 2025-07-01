#!/usr/bin/env python3
"""
Meta Content Manager - Vercel Entry Point
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app

# This is the entry point for Vercel
if __name__ == "__main__":
    app.run()