# SPDX-FileCopyrightText: Contributors to powerplantmatching <https://github.com/pypsa/powerplantmatching>
#
# SPDX-License-Identifier: MIT

"""
Build a global, standardized power plant dataset from the GEM trackers only.

The default config targets European countries and drops plants south of
30°N; this script widens both and runs each GEM tracker through the standard
cleaning, then names technologies and fuels after PyPSA technology-data
('tech', 'fuel'). Units are aggregated to plants by GEM location ID rather than by
duke (Java) fuzzy matching, since GEM already links units to plants.

Usage: python analysis/build_global_gem.py [out_dir]
"""

import sys
from pathlib import Path

import country_converter as coco
import pandas as pd

import powerplantmatching as pm

GEM_TRACKERS = ["GBPT", "GGPT", "GCPT", "GGTPT", "GNPT", "GSPT", "GWPT", "GHPT"]
EXTRA_COLUMNS = ["Status", "GEM location ID"]


def global_config():
    countries = sorted(coco.CountryConverter().data["name_short"].dropna().unique())
    target_columns = pm.get_config()["target_columns"] + EXTRA_COLUMNS
    return pm.get_config(
        target_countries=countries,
        target_columns=target_columns,
        main_query="Name != ''",
        matching_sources=["GEM"],
        fully_included_sources=["GEM"],
    )


def main(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    config = global_config()

    units = []
    for name in GEM_TRACKERS:
        df = getattr(pm.data, name)(config=config)
        print(f"{name}: {len(df)} units, {df.Capacity.sum() / 1e3:.0f} GW")
        units.append(df)
    units = (
        pd.concat(units, ignore_index=True)
        .rename(columns={"GEM location ID": "locationID"})
        .powerplant.to_pypsa_technology_data()
    )
    names = units.Country.dropna().unique()
    iso3 = coco.convert(list(names), to="ISO3", not_found=None)
    units.insert(units.columns.get_loc("Country") + 1, "ISO3", units.Country.map(dict(zip(names, iso3))))
    units.to_csv(out_dir / "gem_global_units.csv", index=False)

    plants = aggregate_by_location(units)
    plants.to_csv(out_dir / "gem_global_plants.csv", index=False)
    print(f"plants: {len(plants)}, {plants.Capacity.sum() / 1e3:.0f} GW")


def aggregate_by_location(units):
    """Sum units sharing a GEM location, technology, fuel and status."""
    keys = ["locationID", "Country", "ISO3", "Fueltype", "Technology", "tech", "fuel", "Set", "Status"]
    return (
        units.groupby(keys, dropna=False)
        .agg(
            Name=("Name", "first"),
            Capacity=("Capacity", "sum"),
            DateIn=("DateIn", "min"),
            DateOut=("DateOut", "max"),
            lat=("lat", "mean"),
            lon=("lon", "mean"),
            n_units=("Capacity", "size"),
        )
        .reset_index()
    )


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "outputs/gem_global")
