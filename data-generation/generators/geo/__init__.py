"""
GeoAnalytics Data Generators

This module provides synthetic data generators for geospatial analytics
in the casino/gaming industry, including:

- Casino locations (US and global markets)
- Player demographics with home locations
- Market analysis and catchment areas

Usage:
    from generators.geo import casino_locations, player_demographics

    # Generate 100 US casino locations
    casinos = casino_locations.generate_us_casino_locations(100)

    # Generate 50 international casino locations
    global_casinos = casino_locations.generate_global_casino_locations(50)

    # Generate 10,000 player demographics linked to casinos
    players = player_demographics.generate_player_demographics(10000, casinos)

    # Export to GeoJSON for visualization
    geojson = casino_locations.create_geojson(casinos)
"""

from .casino_locations import (
    generate_us_casino_locations,
    generate_global_casino_locations,
    create_geojson,
    US_GAMING_MARKETS,
    GLOBAL_GAMING_MARKETS,
    CasinoLocation
)

from .player_demographics import (
    generate_player_demographics,
    create_player_geojson,
    generate_market_summary,
    haversine_distance,
    POPULATION_CENTERS
)

__all__ = [
    # Casino locations
    "generate_us_casino_locations",
    "generate_global_casino_locations",
    "create_geojson",
    "US_GAMING_MARKETS",
    "GLOBAL_GAMING_MARKETS",
    "CasinoLocation",

    # Player demographics
    "generate_player_demographics",
    "create_player_geojson",
    "generate_market_summary",
    "haversine_distance",
    "POPULATION_CENTERS"
]
