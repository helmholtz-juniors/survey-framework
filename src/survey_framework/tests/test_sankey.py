from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

from survey_framework.data_analysis.analysis import get_data_for_q
from survey_framework.data_import.data_import import LimeSurveyData
from survey_framework.plotting.sankeyplots import plot_sankey


def test_sankey(survey: LimeSurveyData, output_path: Path) -> None:
    section = "E"
    q_left = "E10"
    q_right = "E11"
    cleaning_threashold = 5

    output = output_path / section / (f"{q_left}-{q_right}.pdf")
    output.parent.mkdir(exist_ok=True, parents=True)

    data_actual = get_data_for_q(survey, q_left)
    data_pref = get_data_for_q(survey, q_right)
    data_merged = data_actual.merge(data_pref, left_on="id", right_on="id")
    data_indexed = (
        data_merged.groupby([q_left, q_right])
        .size()
        .reset_index()
        .rename(columns={0: "count"})
    )

    d = list()
    for _, row in data_indexed.iterrows():
        q_l = survey.get_choices(q_left).get(row[q_left])
        q_r = survey.get_choices(q_right).get(row[q_right])

        if row["count"] <= cleaning_threashold:
            continue

        d.append((q_l, row["count"], q_r, row["count"]))

    data_df = pd.DataFrame(d)
    data_df = data_df.replace(regex={r".*don't want.*": "DWTA"})

    plot_sankey(
        data_df=data_df,
        titles=["Actual Frequency", "Preferred Frequency"],
    )

    plt.savefig(output)
