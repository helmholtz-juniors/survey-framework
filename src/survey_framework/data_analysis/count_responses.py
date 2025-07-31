import pandas as pd

# This file contains a family of functions that take raw survey dataframes
# and output a cleaned, sorted, counted dataframe ready for plotting.


def prepare_df_single(
    data: pd.DataFrame, q: str, ordering: dict[str, list[str]]
) -> tuple[pd.DataFrame, int]:
    """Count participants in the data. This function is for single-choice questions.

    The output dataframe contains the following columns:
    - q: The answer options
    - "count": number of participants (in this group) that gave this answer
    - "proportion": share of participants (relative to "total") that gave this answer

    Args:
        data: The main DataFrame of answers
        q (str): name of the output column for answer options
        ordering: Answer re-ordering dict, e.g. ORDER from `order/order2024.py`

    Returns:
        Tuple of [DataFrame, participant number]. The latter is used as N in plots.
    """
    N_question = data.count().iloc[0]
    if "id" not in data.columns:
        data.reset_index(inplace=True)
    data_q_counts = (
        data.groupby([q], observed=False).count().rename(columns={"id": "count"})
    )

    # sort the dataframe
    data_q_counts_sorted = data_q_counts.reset_index()
    orderlist = ordering.get(q)
    if orderlist:
        # sort with given order
        data_q_counts_sorted[q] = pd.Categorical(
            data_q_counts_sorted[q], categories=orderlist, ordered=True
        )
        data_q_counts_sorted = data_q_counts_sorted.sort_values(by=q)

    # add percentages column
    data_q_counts_sorted_percentages = data_q_counts_sorted
    data_q_counts_sorted_percentages["proportion"] = (
        data_q_counts_sorted_percentages["count"] / N_question
    )

    return data_q_counts_sorted_percentages, N_question


def prepare_df_multiple(
    data: pd.DataFrame, q: str, ordering: dict[str, list[str]]
) -> tuple[pd.DataFrame, int]:
    """Count participants in the data. This function is for multiple-choice questions.

    The output dataframe contains the following columns:
    - q: The answer options
    - "count": number of participants (in this group) that gave this answer
    - "proportion": share of participants (relative to "total") that gave this answer

    Args:
        data: The main DataFrame of answers
        q (str): name of the output column for answer options
        ordering: Answer re-ordering dict, e.g. ORDER from `order/order2024.py`

    Returns:
        Tuple of [DataFrame, participant number]. The latter is used as N in plots.
    """
    # boolean value: participants who answered anything (summed up later)
    data["total"] = data.sum(axis="columns").gt(0)
    # melt into long form
    responses_melted = pd.melt(data, id_vars=["total"], value_name="count", var_name=q)
    responses_counts = responses_melted.groupby(q).sum()

    # add percentages column
    responses_counts["proportion"] = (
        responses_counts["count"] / responses_counts["total"]
    )

    # re-index for sorting
    responses_clean = responses_counts.reset_index()
    # get number of participants
    participants = responses_clean["total"].drop_duplicates().iloc[0]

    # sort the DF
    orderlist = ordering.get(q)
    if orderlist:
        # sort with given order
        responses_clean[q] = pd.Categorical(
            responses_clean[q], categories=orderlist, ordered=True
        )
        responses_sorted = responses_clean.sort_values(by=q)
    else:
        # no order given, sort by descending values
        responses_sorted = responses_clean.sort_values(by="count", ascending=False)
        # TODO: sorting by value is unstable between centers. We probably want
        #       to define a fixed order for all questions.
        # print(q, responses_df_counts_sorted["variable"].to_list())

    return responses_sorted, participants


def prepare_df_comparison(
    responses_df_all: pd.DataFrame,
    responses_df_comparison: "pd.Series[str]",
    q: str,
    q_comparison: str,
    ordering: dict[str, list[str]],
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Compare groups of participants (determined by comparison_series).
    This function is for single-choice questions.

    The output dataframe contains the following columns:
    - q: The answer options
    - q_comparison: The groups
    - "total": total number of participants in this group
    - "count": number of participants (in this group) that gave this answer
    - "proportion": share of participants (relative to "total") that gave this answer

    Args:
        responses_df: The main DataFrame of answers
        comparison_series: Participant group (shares index with the main DF)
        q (str): name of the output column for answer options
        q_comparison (str): name of the output column for groups
        ordering: Answer re-ordering dict, e.g. ORDER from `order/order2024.py`

    Returns:
        Tuple of [DataFrame, group size dict]. The latter is used as N in plots.
    """
    assert "id" not in responses_df_all.columns
    responses_joined = responses_df_all.join(responses_df_comparison)

    grouped_by_center = responses_joined.groupby(q_comparison)[q]
    responses_df_counts = pd.concat(
        [
            grouped_by_center.value_counts(normalize=True).rename("proportion"),
            grouped_by_center.value_counts().rename("count"),
        ],
        axis=1,
    ).reset_index()

    # sort DF
    order_left = ordering.get(q)
    if order_left:
        responses_df_counts[q] = pd.Categorical(
            responses_df_counts[q], categories=order_left, ordered=True
        )
    order_right = ordering.get(q_comparison)
    if order_right:
        responses_df_counts[q_comparison] = pd.Categorical(
            responses_df_counts[q_comparison], categories=order_right, ordered=True
        )
    responses_df_counts_sorted = responses_df_counts.sort_values(by=[q_comparison, q])

    return responses_df_counts_sorted, grouped_by_center.count().to_dict()


def prepare_df_comparison_multiple(
    responses_df: pd.DataFrame,
    comparison_series: "pd.Series[str]",
    q: str,
    q_comparison: str,
    ordering: dict[str, list[str]],
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Compare groups of participants (determined by comparison_series).
    This function is for multiple-choice questions.

    The output dataframe contains the following columns:
    - q: The answer options
    - q_comparison: The groups
    - "total": total number of participants in this group
    - "count": number of participants (in this group) that gave this answer
    - "proportion": share of participants (relative to "total") that gave this answer

    Args:
        responses_df: The main DataFrame of answers
        comparison_series: Participant group (shares index with the main DF)
        q (str): name of the output column for answer options
        q_comparison (str): name of the output column for groups
        ordering: Answer re-ordering dict, e.g. ORDER from `order/order2024.py`

    Returns:
        Tuple of [DataFrame, group size dict]. The latter is used as N in plots.
    """
    # boolean value: participants who answered anything (summed up per group later)
    responses_df["total"] = responses_df.sum(axis="columns").gt(0)
    # melt into long form, merge with comparison
    responses_melt = pd.melt(
        responses_df.reset_index(),
        id_vars=["id", "total"],
        var_name=q,
        value_name="count",
    ).join(comparison_series, on="id")

    # for each subquestion, count `True` values, and normalize per group
    responses_counts = (
        responses_melt.groupby([q_comparison, q]).sum().drop(columns=["id"])
    )
    responses_counts["proportion"] = (
        responses_counts["count"] / responses_counts["total"]
    )

    # re-index for sorting
    responses_clean = responses_counts.reset_index()

    # get the number of participants per group in q_comparison
    participants = responses_clean.set_index(q_comparison)["total"].drop_duplicates()

    # ordering (copied from `prepare_df_comparison` above)
    order_left = ordering.get(q)
    if order_left:
        responses_clean[q] = pd.Categorical(
            responses_clean[q], categories=order_left, ordered=True
        )
    order_right = ordering.get(q_comparison)
    if order_right:
        responses_clean[q_comparison] = pd.Categorical(
            responses_clean[q_comparison], categories=order_right, ordered=True
        )
    responses_sort = responses_clean.sort_values(by=[q_comparison, q])
    # print(responses_sort)

    return responses_sort, participants.to_dict()
