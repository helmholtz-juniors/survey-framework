# questions

sectionA = "A"  # GENERAL
a1 = "A1"  # participation in last N2 survey
a2 = "A2"  # institute/section/center association
a3 = "A3"  # field of work (subject)
a4 = "A4"  # type of work
a5 = "A5"  # year of birth
a6 = "A6"  # gender representation
a7 = "A7"  # sexual orientation
a8a = "A8a"  # start of PhD - month
a8 = "A8"  # start of PhD - year
a9a = "A9a"  # expected submission date PhD - month
a9 = "A9"  # expected submission date PhD - year
a10 = "A10"  # ethnicity - MULTI
a11 = "A11"  # citizenship
a12a = "A12a"  # parents born in Germany
a12b = "A12b"  # participant born in Gerany
a13 = "A13"  # disability present

sectionB = "B"  # WORKING CONDITIONS
b1 = "B1"  # financing of doctorate
b1a = "B1a"
b1b = "B1b"
b1c = "B1c"  # MULTI
b1d = "B1d"
b2 = "B2"
b2a = "B2a"
b3 = "B3"
b4a = "B4a"  # ARRAY --> special array
b4b = "B4b"  # ARRAY --> special array
b5 = "B5"  # ARRAY
b6 = "B6"
b7 = "B7"  # MULTI
b8 = "B8"
b9 = "B9"
b9a = "B9a"  # MULTI
b10 = "B10"
b11 = "B11"
b12 = "B12"
b13 = "B13"  # MULTI
b14 = "B14"  # ARRAY
b15 = "B15"
b16 = "B16"
b17 = "B17"
b18 = "B18"  # MULTI
b19 = "B19"

sectionC = "C"  # SATISFACTION
c1 = "C1"  # ARRAY
c2 = "C2"
c3 = "C3"  # MULTI
c4 = "C4"  # ARRAY
c5 = "C5"  # ARRAY

sectionE = "E"  # SUPERVISION
e1 = "E1"  # MULTI
e2 = "E2"
e3 = "E3"
e4 = "E4"  # MULTI
e5 = "E5"
e6 = "E6"  # MULTI
e7 = "E7"
e8 = "E8"
e9 = "E9"
e10 = "E10"
e11 = "E11"
e12 = "E12"  # ARRAY
e13 = "E13"  # ARRAY
e14 = "E14"  # MULTI
e15 = "E15"

sectionH = "H"  # INTEGRATION
h1a = "H1a"  # MULTI
h1b = "H1b"  # MULTI
h2 = "H2"
h3 = "H3"
h4 = "H4"
h5 = "H5"  # MULTI


sectionI = "I"  # CAREER DEVELOPMENT
i1 = "I1"
i2 = "I2"  # ARRAY
i3 = "I3"  # MULTI
i4 = "I4"  # ARRAY
i5 = "I5"
i6 = "I6"
i7 = "I7"
i8 = "I8"

sectionJ = "J"  # FAMILY
j1 = "J1"
j1b = "J1b"
j2 = "J2"  # MULTI
j3 = "J3"  # MULTI
j4 = "J4"
j5 = "J5"
j6 = "J6"
j7 = "J7"

sectionF = "F"  # POWER ABUSE
f1 = "F1"  # MULTI
f2 = "F2"
f2a = "F2a"  # MULTI
f3 = "F3"
f4 = "F4"  # MULTI
f4a = "F4a"
f5 = "F5"
f5a = "F5a"
f6 = "F6"  # MULTI
f6a = "F6a"  # MULTI
f6b = "F6b"
f7 = "F7"  # MULTI
f7a = "F7a"
f8 = "F8"  # MULTI
f8a = "F8a"
f8c = "F8c"  # MULTI
f9 = "F9"
f9a = "F9a"
f9c = "F9c"  # MULTI
f10 = "F10"

sectionD = "D"  # MENTAL HEALTH
d0 = "D0"
d1 = "D1"  # ARRAY
d2 = "D2"  # ARRAY
d3 = "D3"  # ARRAY
d3a = "D3a"
d3b = "D3b"
d3c = "D3c"
d3d = "D3d"  # ARRAY
d4 = "D4"  # ARRAY
d5 = "D5"
d6 = "D6"
d7 = "D7"
d8 = "D8"
d9 = "D9"

l1 = "L1"

# list of questions

### DEPRECATED ### use LimeSurveyData.get_questions_by_type() instead.
# single_choice = [
#     a1,
#     a2,
#     a3,
#     a4,
#     a5,
#     a6,
#     a7,
#     a8,
#     a9,
#     a11,
#     a12a,
#     a12b,
#     a13,
#     b1,
#     b1a,
#     b1b,
#     b1d,
#     b2,
#     b2a,
#     b3,
#     b6,
#     b8,
#     b9,
#     b10,
#     b11,
#     b12,
#     b15,
#     b16,
#     b17,
#     b19,
#     c2,
#     e2,
#     e3,
#     e5,
#     e7,
#     e8,
#     e9,
#     e10,
#     e11,
#     e15,
#     h2,
#     h3,
#     h4,
#     i1,
#     i5,
#     i6,
#     i7,
#     i8,
#     j1,
#     j1b,
#     j4,
#     j5,
#     j6,
#     j7,
#     f2,
#     f3,
#     f4a,
#     f5,
#     f5a,
#     f6b,
#     f7a,
#     f8a,
#     f9,
#     f9a,
#     f10,
#     d0,
#     d3a,
#     d3b,
#     d3c,
#     d5,
#     d6,
#     d7,
#     d8,
#     d9,
#     l1,
# ]
# multiple_choice = [
#     a10,
#     b1c,
#     b7,
#     b9a,
#     b13,
#     b18,
#     c3,
#     e1,
#     e4,
#     e6,
#     e14,
#     h1a,
#     h1b,
#     h5,
#     i3,
#     j2,
#     j3,
#     f1,
#     f2a,
#     f4,
#     f6,
#     f6a,
#     f7,
#     f8,
#     f8c,
#     f9c,
# ]
# array = [
#     b4a,
#     b4b,
#     b5,
#     b14,
#     c1,
#     c4,
#     c5,
#     e12,
#     e13,
#     i2,
#     i4,
#     d1,
#     d2,
#     d3,
#     d3d,
#     d4,
# ]


# ordering dictionary for answers.
# Keys are the question codes, values are lists of answer codes.
order = {
    "A1": ["A1", "A2", "A3", "A4"],
    "A2": [
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
    "A3": [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A11",
        "A12",
        "A13",
        "A14",
        "A15",
        "A16",
        "A17",
        "A18",
        "A10",
        "-oth-",
    ],
    "A4": ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "-oth-"],
    # order2024_A5 = [""]
    "A6": ["A1", "A3", "A4", "A5", "A2", "-oth-"],
    "A10": [
        "A10_SQ001",
        "A10_SQ002",
        "A10_SQ003",
        "A10_SQ004",
        "A10_SQ005",
        "A10_SQ006",
        "A10_SQ007",
        "A10_SQ008",
        "A10_SQ009",
        "A10_SQ010",
        "A10T",
    ],
    # array questions below (likert ordering)
    "B5": ["A1", "A3", "A2"],
    "C1": ["A5", "A4", "A3", "A6", "A2", "A1"],
    "C4": ["A5", "A4", "A3", "A6", "A2", "A1"],
    "D4": ["A4", "A3", "A5", "A2"],
    "E12": ["A5", "A4", "A3", "A6", "A2", "A1"],
    "E13": ["A5", "A4", "A3", "A6", "A2", "A1"],
    "I2": ["A1", "A2", "A3", "A6", "A4", "A5"],
    "I4": ["A3", "A4", "A5", "A2", "A1"],
}


# bar labels

bar_label_a1 = "Participated in N2 survey 2019"
bar_label_a2 = "Centers"
bar_label_a3 = "Field"
bar_label_a4 = "Predominant Type of Work"
bar_label_a5 = "Year of Birth"
bar_label_a6 = "Gender"
bar_label_a7 = "Sexual Orientation"
bar_label_a8 = "Start of PhD"
bar_label_a9 = "Expected Submission Date of PhD Thesis"
bar_label_a10 = "Ethnicity"
bar_label_a11 = "Citizenship"
bar_label_a12a = "Parents of Participants born in Germany"
bar_label_a12b = "Participants born in Germany"
bar_label_a13 = "Disability"

bar_label_b1 = "Financing of Doctoral Research"
bar_label_b1a = "Top-Up Contracts to Stipends at Centers/Institutes"
bar_label_b1b = "Time worked on PhD without Pay"
bar_label_b1c = "Reasons for Non-Payment"
bar_label_b1d = 'Unemployment Benefits ("Arbeitslosengeld")'
bar_label_b2 = "Monthy Income"
bar_label_b3 = "Monthly Living Expenses"
