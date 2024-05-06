#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:12:18 2024

@author: jenpopp
"""

import re
from datetime import datetime
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from plotting.helmholtzcolors import get_blues, helmholtzgreen

# from svgpathtools import svg2paths
# from svgpath2mpl import parse_path


# You just need the survey csv files and the csv file with the center numbers in one folder
# they are on sync and share in the Race to 50 plot folder

# --------------------Change stuff here ----------------------------------------
# path to the colors module because I just do not get how to properly use python modules
# and can't get the relative import to work
# FRAMEWORK_PATH = "."
# path to the survey data
INPUT_PATH = Path("../data/survey_2024")
# path where the plot is supposed to be saved
OUTPUT_PATH = Path("../figures_2024")
# The spreadsheet with the center numbers of DRs
CENTER_FILE_NAME = "center_numbers.csv"
# number of weeks the survey is running for
N_weeks = 6
# The end of the x-axis in percent
x_end = 85
# -----------------------------------------------------------------------------


# define a function that gets you all the survey csv files in a directory
# def get_survey_csv_files(directory: Path) -> list[Path]:
#     # list of all items in the specified directory
#     all_items = os.listdir(directory)
#     # filters out only the survey csv files
#     csv_files = [Path(item) for item in all_items if item.endswith("survey738345.csv")]

#     return csv_files


# function that extracts the date from the filename
def extract_date(filename: Path) -> datetime:
    match = re.search(r"\d{6}", filename.name)
    if match:
        return datetime.strptime(match.group(), "%y%m%d")
    else:
        raise ValueError("filenames are expected to contain a date string.")


# use seaborn style
sns.set_theme()

# use monospaced font
plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.monospace"] = "DejaVu Sans Mono"

# Get the total numbers of DRs from the centers
df_centers = pd.read_csv(INPUT_PATH / CENTER_FILE_NAME).dropna()

# Get the survey csv files
survey_files = INPUT_PATH.glob("*survey738345.csv")  # get_survey_csv_files(INPUT_PATH)
# We need to sort them by date
sorted_survey_files = sorted(survey_files, key=extract_date)

for i, CSV_FILE_NAME in enumerate(sorted_survey_files):
    # Get the survey data
    csv_file = pd.read_csv(CSV_FILE_NAME)

    # get the center question
    center_question = "Which institute/center are you associated with? In the comment section, please specify in which city your institute/center is located."
    responses = csv_file[center_question].dropna()

    # Get the counts for each individual center
    counts = responses.value_counts()

    df_centers[f"counts_week{i+1}"] = df_centers["Center"].map(counts)
    df_centers[f"percentages_week{i+1}"] = (
        df_centers[f"counts_week{i+1}"] / df_centers["N_drs"] * 100
    )

# put zeros instead of NaN so that sorting works properly
df_centers = df_centers.fillna(0)

# Sort the DataFrame in descending order by 'Center_short', so that it appears alphabetically
# df_centers_sorted = df_centers.sort_values(by="Center_short", ascending=False)
df_centers_sorted = df_centers.sort_values(
    by=f"percentages_week{len(sorted_survey_files)}"
)

# use the Center_short column as index
df_centers_sorted.set_index("Center_short", inplace=True)

# make a nice figure
fig, ax = plt.subplots(1, 1, figsize=(7.655, 4.275), dpi=300, layout="constrained")

# get the percentage columns
percentage_columns = [col for col in df_centers_sorted.columns if "percentage" in col]

# Get the difference between the weeks
df_diff = df_centers_sorted[percentage_columns]
for j in range(1, len(df_centers_sorted[percentage_columns].columns)):
    df_diff.iloc[:, j] = (
        df_centers_sorted[percentage_columns].iloc[:, j]
        - df_centers_sorted[percentage_columns].iloc[:, j - 1]
    )

# Get the colors for the bar plot
# The survey is running for 6 weeks
blues = get_blues(N_weeks)[0 : len(sorted_survey_files)]

# plot the bars
bars = df_diff.plot.barh(stacked=True, zorder=3, legend=False, color=blues, ax=ax)  # type: ignore[call-overload]

# add the line at 50%
plt.axvline(50, color=helmholtzgreen)


# Generate new y-tick labels with percentages in brackets
new_labels = []
for index, row in df_centers_sorted.iterrows():
    if index != "KIT":
        column_str = f"percentages_week{i+1}"
        new_labels.append(f"{index} | {row[column_str]:4.1f} %")
        # column_str = f"counts_week{i+1}"
        # new_labels.append(f"{index} | {row[column_str]:3.0f}")
    else:
        new_labels.append("KIT")


# Apply the new labels
ax.set_yticklabels(new_labels)

# and now some shenanigans with the KIT label
# Get the y-tick labels, again
tick_labels = ax.get_yticklabels()
# Check if there are any tick labels to modify
kit_index = df_centers_sorted.index.tolist().index("KIT")
specific_label = tick_labels[
    kit_index
]  # Adjust the index as needed for a different label
specific_label.set_color("lightgray")  # Change color

# set the axis labels (or remove them)
plt.xlabel(" participation rate / % ")
plt.ylabel(" ")

# set the range of the x-axis
ax.set_xlim([0, x_end])
# add a green patch to the area above 50 %
ax.axvspan(50, x_end, color=helmholtzgreen, alpha=0.3)

# Get the survey extraction date
date_obj = extract_date(CSV_FILE_NAME)

# Format the date as dd.mm.yy
formatted_date = date_obj.strftime("%d.%m.%y")

# Add a title to the plot
title_first_line = "#RaceTo50 - Participation rate per centre"
title_second_line = f"extraction date: {formatted_date}"

# Manually position the title using `text`. Adjust `y` for alignment.
ax.text(
    0.5,
    1.05,
    title_first_line,
    ha="center",
    va="bottom",
    fontsize=14,
    fontweight="bold",
    transform=ax.transAxes,
)
ax.text(
    0.5,
    1.01,
    title_second_line,
    ha="center",
    va="bottom",
    fontsize=11,
    transform=ax.transAxes,
)

#####Adding a legend
legend_labels = [f"Week {week + 1}" for week in range(len(sorted_survey_files))]
patches = [
    mpl.patches.Patch(color=color, label=label)
    for color, label in zip(blues, legend_labels)
]
plt.legend(handles=patches, loc="lower right")

# I wanted to use a crown marker for the center winning the race, but it looked somehow weird.
# Dunno if someone wants to further work on this

# crown_path, attributes = svg2paths('/home/jenpopp/Pictures/crown.svg')
# crown_marker = parse_path(attributes[0]['d'])
# crown_marker.vertices -= crown_marker.vertices.mean(axis=0)

# crown_marker = crown_marker.transformed(mpl.transforms.Affine2D().rotate_deg(180))
# crown_marker = crown_marker.transformed(mpl.transforms.Affine2D().scale(-1,1))

# Find the maximum value and its index
# max_value = df_centers_sorted[f"percentages_week{i+1}"].max()
# max_index =  df_centers_sorted[f"percentages_week{i+1}"].idxmax()
# crown_y = df_centers_sorted.index.get_loc(max_index)

# plt.plot(max_value, crown_y,'o',marker=crown_marker,markersize=20,zorder=4,color=helmholtzgreen)

plt.savefig(OUTPUT_PATH / f"RaceTo50_{formatted_date}.png")
# plt.savefig(OUTPUT_PATH / f"RaceTo50_{formatted_date}_absolute.png")
