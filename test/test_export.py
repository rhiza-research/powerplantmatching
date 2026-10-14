# SPDX-FileCopyrightText: Contributors to powerplantmatching <https://github.com/pypsa/powerplantmatching>
#
# SPDX-License-Identifier: MIT

import numpy as np
import pandas as pd

from powerplantmatching.export import to_pypsa_technology_data


def test_to_pypsa_technology_data():
    df = pd.DataFrame(
        {
            "Fueltype": [
                "Natural Gas",
                "Natural Gas",
                "Natural Gas",
                "Lignite",
                "Hydro",
                "Hydro",
                "Hydro",
                "Wind",
                "Wind",
                "Solar",
                "Biogas",
                "Other",
            ],
            "Technology": [
                "CCGT",
                "OCGT",
                "Steam Turbine",
                "Steam Turbine",
                "Reservoir",
                "Run-Of-River",
                "Pumped Storage",
                "Offshore",
                np.nan,
                "PV",
                np.nan,
                np.nan,
            ],
        }
    )
    res = to_pypsa_technology_data(df)
    assert res.tech.tolist()[:-1] == [
        "CCGT",
        "OCGT",
        "OCGT",
        "lignite",
        "hydro",
        "ror",
        "PHS",
        "offwind",
        "onwind",
        "solar-utility",
        "biomass",
    ]
    assert pd.isna(res.tech.iloc[-1])
    assert res.fuel.tolist()[:4] == ["gas", "gas", "gas", "lignite"]
    assert res.fuel.iloc[10] == "biogas"
    assert pd.isna(res.fuel.iloc[4])
