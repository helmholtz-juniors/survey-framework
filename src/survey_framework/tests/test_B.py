from pathlib import Path
from textwrap import wrap
from typing import cast

import matplotlib.pyplot as plt

from survey_framework.data_analysis.analysis import get_data_for_q
from survey_framework.data_import.data_import import LimeSurveyData


def test_swarm(survey: LimeSurveyData, output_path: Path) -> None:
    """
    WARNING: This is WIP, the generated plot does _not_ adhere to our style.
    """
    section = "B"
    q = "B14"

    output = output_path / section / (q + ".pdf")
    output.parent.mkdir(exist_ok=True, parents=True)

    data_df = get_data_for_q(survey, q)
    # data_df = data_df.drop("id", axis=1).floordiv(5)  # divide by 5
    fig, ax = plt.subplots(dpi=300, figsize=(16, 10), layout="constrained")

    import seaborn as sns

    ax = sns.boxenplot(
        data_df,
        ax=ax,
        orient="h",
        # jitter=0.2,
    )

    # tick labels (TODO re-use code!!!)
    new_labels = []
    for old_label in ax.get_yticklabels():
        label = cast(str, survey.questions.loc[old_label.get_text()]["label"])
        new_labels.append("\n".join(wrap(label, 30)))
    ax.set_yticks(ax.get_yticks())
    ax.set_yticklabels(new_labels)

    ax.set_xlabel("Time Allocated [%]")
    ax.set_ylabel("Task")

    fig.savefig(output)

    print(data_df)
