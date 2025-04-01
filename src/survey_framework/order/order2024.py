# order2024.py
# LimeSurvey assigns answer labels in non-ascending order to some questions,
# which we manually sort as intended here.
#
# Note: A previous version of this file also included lists of all questions
# by their question type; for this, use LimeSurveyData.get_questions_by_type().


ORDER = {
    ### SECTION A: General
    "A1": [  # participation in last N2 survey
        "A1",
        "A2",
        "A3",
        "A4",
    ],
    "A2": [  # institute/section/center association
        "A01",
        "A18",
        "A02",
        "A03",
        "A04",
        "A05",
        "A06",
        "A07",
        "A08",
        "A09",
        "A10",
        "A11",
        "A12",
        "A13",
        "A14",
        "A15",
        "A17",
        "A19",  # other
    ],
    "A3": [  # field of work (subject)
        "A15",  # Agriculture
        "A5",  # Biology
        "A1",  # Chemistry
        "A13",  # Comp. Sc.
        "A12",  # Engineering
        "A3",  # Geosciences
        "A14",  # Health Sciences
        "A11",  # Humanities
        "A7",  # Law / Econ
        "A4",  # Mathematics
        "A6",  # Medicine
        "A2",  # Physics
        "A8",  # Social Sciences
        "A10",  # IDWA
        "-oth-",
    ],
    "A4": [  # type of work
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "-oth-",
    ],
    "A5": [  # year of birth, sorted chronologically
        "A1",
        "A20",
        "A21",
        "A38",
        "A22",
        "A23",
        "A24",
        "A25",
        "A26",
        "A27",
        "A28",
        "A29",
        "A30",
        "A31",
        "A32",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "A11",
        "A12",
        "A13",
        "A14",
        "A15",
        "A16",
        "A17",
        "A33",
        "A34",
        "A35",
        "A36",
        "A18",
        "A19",
        "-oth-",
    ],
    "A6": [  # gender representation
        "A1",  # Woman
        "A3",  # Man
        "A4",  # Gender-diverse
        "A5",  # Non-binary
        "A6",  # IDK
        "-oth-",
        "A2",  # IDWA
    ],
    "A7": [  # sexual orientation
        "A1",  # Hetero
        "A2",  # Homo
        "-oth-",  # Queer
        "A8",  # IDK
        "A6",  # IDWA
    ],
    "A8": [  # start of PhD - years, sorted chronologically
        "A8",
        "A6",
        "A5",
        "A4",
        "A3",
        "A2",
        "A1",
        "A10",
        "A11",
        "A12",
        "A9",  # IDK
        "A13",  # IDWA
    ],
    "A8a": [  # start of PhD - month, sorted chronologically
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "A11",
        "A12",
        "A13",  # IDK
        "A14",  # IDWA
    ],
    "A9": [  # expected submission date PhD - years, sorted chronologically
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "A11",
        "A12",  # submitted
        "A15",  # unable to
        "A13",  # IDK
        "A14",  # IDWA
    ],
    "A9a": [  # expected submission date PhD - month, sorted chronologically
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "A11",
        "A12",
        "A13",  # unable to
        "A14",  # IDK
        "A15",  # IDWA
    ],
    "A10": [  # ethnicity
        "A10_SQ09",  # Central America and Carribean
        "A10_SQ06",  # East / Central Asia
        "A10_SQ01",  # Europe
        "A10_SQ08",  # North America
        "A10_SQ02",  # North and sub-Saharan Africa
        "A10_SQ07",  # Pacific / Oceania
        "A10_SQ03",  # South Africa
        "A10_SQ010",  # South America
        "A10_SQ05",  # South / Southeast Asia
        "A10_SQ04",  # West Asia / Middle East
        "A10_SQ011",  # IDK
        "A10_SQ012",  # IDWA
    ],
    "A12a": [  # parents born in Germany
        "A2",
        "A3",
        "A4",
        "A5",
        "A1",
    ],
    "A12b": [  # participant born in Germany
        "A3",
        "A2",
        "A1",
    ],
    ### SECTION B: Working Conditions
    "B5": ["A1", "A3", "A2"],  # Likert
    ### SECTION C: Satisfaction
    "C1": ["A5", "A4", "A3", "A6", "A2", "A1"],  # Likert
    "C4": ["A5", "A4", "A3", "A6", "A2", "A1"],  # Likert
    "C5": ["A2", "A3", "A6", "A4", "A5"],  # Likert
    ### SECTION D: Mental Health
    "D4": ["A4", "A3", "A5", "A2"],  # Likert
    "D9": ["A1", "A2", "-oth-", "A3"],
    ### SECTION E: Supervision
    "E2": ["A1", "A2", "A3", "A4", "A7", "A5", "A6"],
    "E8": ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11"],
    "E9": ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11"],
    "E10": ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11"],
    "E11": ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11"],
    "E12": ["A5", "A4", "A3", "A6", "A2", "A1"],  # Likert
    "E13": ["A5", "A4", "A3", "A6", "A2", "A1"],  # Likert
    ### SECTION F: Power Abuse
    "F1": [
        "F1_SQ001",
        "F1_SQ018",
        "F1_SQ003",
        "F1_SQ004",
        "F1_SQ015",
        "F1_SQ006",
        "F1_SQ007",
        "F1_SQ008",
        "F1_SQ014",
        "F1_SQ021",
        "F1_SQ020",  # Other
        "F1_SQ009",  # Not aware of any
        "F1_SQ011",  # IDWA
    ],
    "F2a": [
        "F2a_SQ001",
        "F2a_SQ002",
        "F2a_SQ009",
        "F2a_SQ003",
        "F2a_SQ004",
        "F2a_SQ005",
        "F2a_SQ006",
        "F2a_SQ010",  # Other
        "F2a_SQ007",  # IDK
        "F2a_SQ008",  # IDWA
    ],
    "F4": [
        "F4_SQ009",  # No
        "F4_SQ001",
        "F4_SQ002",
        "F4_SQ003",
        "F4_SQ004",
        "F4_SQ005",
        "F4_SQ006",
        "F4_SQ007",
        "F4_SQ008",
        "F4_SQ012",  # Other
        "F4_SQ010",  # IDK
        "F4_SQ011",  # IDWA
    ],
    "F6": [
        "F6_SQ011",  # No
        "F6_SQ002",
        "F6_SQ003",
        "F6_SQ004",
        "F6_SQ005",
        "F6_SQ006",
        "F6_SQ007",
        "F6_SQ008",
        "F6_SQ009",
        "F6_SQ010",
        "F6_SQ014",  # Other
        "F6_SQ012",  # IDK
        "F6_SQ013",  # IDWA
    ],
    "F6a": [
        "F6a_SQ001",  # Gender
        "F6a_SQ002",  # Nationality
        "F6a_SQ003",  # Ethnicity
        "F6a_SQ004",  # Age
        "F6a_SQ005",  # Sexual orientation
        "F6a_SQ006",  # Gender identity
        "F6a_SQ007",  # Religion
        "F6a_SQ012",  # Physical appearance
        "F6a_SQ008",  # Disability
        "F6a_SQ013",  # Position of power
        "F6a_SQ011",  # Mental health
        "F6a_SQ009",  # Pregnancy
        "F6a_SQ017",  # Other
        "F6a_SQ015",  # IDK
        "F6a_SQ016",  # IDWA
    ],
    "F7": [
        "F7_SQ014",  # No
        "F7_SQ002",  # Gender
        "F7_SQ003",  # Nationality
        "F7_SQ004",  # Ethnicity
        "F7_SQ005",  # Age
        "F7_SQ006",  # Sexual orientation
        "F7_SQ007",  # Gender identity
        "F7_SQ008",  # Religion
        "F7_SQ009",  # Physical appearance
        "F7_SQ010",  # Disability
        "F7_SQ011",  # Position of Power
        "F7_SQ012",  # Mental health
        "F7_SQ013",  # Pregnancy
        "F7_SQ017",  # Other
        "F7_SQ015",  # IDK
        "F7_SQ016",  # IDWA
    ],
    "F8": [
        "F8_SQ008",  # No
        "F8_SQ001",
        "F8_SQ002",
        "F8_SQ003",
        "F8_SQ004",
        "F8_SQ005",
        "F8_SQ006",
        "F8_SQ007",
        "F8_SQ011",  # Other
        "F8_SQ009",  # IDK
        "F8_SQ010",  # IDWA
    ],
    "F8c": [
        "F8c_SQ001",  # Gender
        "F8c_SQ002",  # Nationality
        "F8c_SQ003",  # Ethnicity
        "F8c_SQ004",  # Age
        "F8c_SQ005",  # Sexual orientation
        "F8c_SQ006",  # Gender identity
        "F8c_SQ007",  # Religion
        "F8c_SQ008",  # Physical appearance
        "F8c_SQ009",  # Disability
        "F8c_SQ010",  # Position of power
        "F8c_SQ011",  # Mental health
        "F8c_SQ012",  # Pregnancy
        "F8c_SQ013",  # Other
        "F8c_SQ014",  # IDK
        "F8c_SQ015",  # IDWA
    ],
    "F9c": [
        "F9c_SQ001",  # Gender
        "F9c_SQ002",  # Nationality
        "F9c_SQ003",  # Ethnicity
        "F9c_SQ004",  # Age
        "F9c_SQ005",  # Sexual orientation
        "F9c_SQ006",  # Gender identity
        "F9c_SQ007",  # Religion
        "F9c_SQ008",  # Physical appearance
        "F9c_SQ009",  # Disability
        "F9c_SQ010",  # Position of power
        "F9c_SQ011",  # Mental health
        "F9c_SQ012",  # Pregnancy
        "F9c_SQ013",  # Other
        "F9c_SQ015",  # IDK
        "F9c_SQ014",  # IDWA
    ],
    "F10": ["A2", "A3", "A7", "A4", "A5", "A6"],
    ### SECTION H: Integration
    ### SECTION I: Career Development
    "I2": ["A1", "A2", "A3", "A6", "A4", "A5"],  # Likert
    "I4": ["A3", "A4", "A5", "A2", "A1"],  # Likert
    ### SECTION J: Family
}
"""
Ordering dictionary for answers.
Keys are the question codes, values are lists of answer codes.

Note, only questions that need to be re-ordered are present.
### Usage example
```python
orderlist = ORDER.get(question)
if orderlist:
    do_stuff(orderlist)
```
"""
