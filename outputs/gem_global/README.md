# Global GEM power plants

Global power plant dataset built from the Global Energy Monitor (GEM) trackers
only, using `analysis/build_global_gem.py`. Regenerate with:

```
python analysis/build_global_gem.py outputs/gem_global
```

## Files

- `gem_global_units.csv` -- one row per GEM unit/phase.
- `gem_global_plants.csv` -- units summed by GEM location ID, `tech`, `fuel`
  and `Status` (`n_units` counts the units in each row).

Columns follow powerplantmatching's standard columns, plus:

- `Status` -- GEM status: operating, construction, retired, and for coal,
  geothermal and nuclear also mothballed.
- `locationID` -- GEM location ID (one per plant site).
- `tech`, `fuel` -- names from PyPSA technology-data
  (https://github.com/PyPSA/technology-data), from `to_pypsa_technology_data`.
  Gas units other than combined cycle are `OCGT`.

Plants are assigned to the country in GEM's `Country/Area` column; hydropower
on a border is assigned entirely to the first country listed.

## Sources and license

Data: Global Energy Monitor, licensed CC BY 4.0
(https://creativecommons.org/licenses/by/4.0/). Tracker releases used:

| Tracker | Release |
|---|---|
| Global Coal Plant Tracker | July 2026 |
| Global Oil and Gas Plant Tracker | January 2026 |
| Global Solar Power Tracker | February 2026 |
| Global Wind Power Tracker | February 2026 |
| Global Hydropower Tracker | March 2026 |
| Geothermal Power Tracker | March 2026 |
| Global Nuclear Power Tracker | September 2025 |
| Global Bioenergy Power Tracker | V3 |

Cite as: Global Energy Monitor, Global Integrated Power Tracker (component
trackers, releases above), processed with powerplantmatching.
