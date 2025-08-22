#!/usr/bin/env python3
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"
MAX_CONNECTIONS = int(os.getenv("MAX_CONNECTIONS", "10"))

# Bug: This will cause issues when MAX_CONNECTIONS is not a valid integer
CACHE_SIZE = MAX_CONNECTIONS * 2  # Problematic if MAX_CONNECTIONS is invalid
