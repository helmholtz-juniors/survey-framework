import re
import warnings
from enum import StrEnum, auto
from pathlib import Path
from typing import Iterable, Optional, Union, cast

import pandas as pd

from .survey_structure import read_lime_questionnaire_structure


class QuestionType(StrEnum):
    FREE = auto()
    ARRAY = auto()
    SINGLE_CHOICE = "single-choice"
    MULTIPLE_CHOICE = "multiple-choice"


class LimeSurveyData:
    """Base LimeSurvey class"""

    # we probably want these kind of constants defined somewhere else in one place
    na_label: str = "No Answer"
    lime_system_info: pd.DataFrame
    responses: pd.DataFrame
    questions: pd.DataFrame
    sections: pd.DataFrame

    def __init__(
        self,
        structure_file: Path,
        responses_file: Path,
    ) -> None:
        """
        Initialize an instance of the Survey

        Args:
            structure_file: path to the structure XML file
            responses_file: path to the responses CVS file
        """

        # Store path to structure file
        self.read_structure(structure_file)
        self.read_responses(responses_file)

    def __str__(self) -> str:
        string = f"QUESTIONS\n{self.questions}\n"
        string += f"RESPONSES\n{self.responses}\n"
        string += f"SECTIONS\n{self.sections}\n"
        return string

    # partially copied from N2Framework
    def read_structure(self, structure_file: Path) -> None:
        """
        Read structure XML file

        Args:
            structure_file: path to the structure XML file

        Returns:

        """

        # Parse XML structure file
        structure_dict = read_lime_questionnaire_structure(structure_file)

        # Get pandas.DataFrame table for the structure
        section_df = pd.DataFrame(structure_dict["sections"])
        section_df = section_df.set_index("id")
        question_df = pd.DataFrame(structure_dict["questions"])
        question_df = question_df.set_index("name")
        question_df["is_contingent"] = question_df.contingent_of_name.notnull()
        self.sections = section_df
        self.questions = question_df

        # import hard-coded questions
        # for question, info in self.additional_questions.items():
        #     self.add_question(question, **info)

    # copied from N2Framework
    def read_responses(
        self,
        responses_file: Path,
        transformation_questions: Optional[dict[str, str]] = None,
    ) -> None:
        """Read responses CSV file

        Args:
            responses_file (str): Path to the responses CSV file
            transformation_questions (dict, optional): Dict of questions
                requiring transformation of raw data, e.g. {'depression': 'D3'}
                or {'supervision': ['E7a', 'E7b']}
        TODO: we do not currently support the transformation dict.
              - if unnecessary, remove
              - if not, move to data_analysis
        """

        # Read 1st line of the csv file
        response = pd.read_csv(responses_file, nrows=1, index_col=0)

        # Prepare dtype info
        columns = response.columns
        renamed_columns = (
            columns.str.replace("[", "_", regex=False)
            .str.replace("]", "", regex=False)
            .str.replace("_other", "other", regex=False)
        )
        dtype_dict, datetime_columns = self._get_dtype_info(columns, renamed_columns)

        # Read entire csv with optimal dtypes
        responses = pd.read_csv(
            responses_file,
            index_col=0,
            dtype=dtype_dict,
            parse_dates=datetime_columns,
            # infer_datetime_format=True,
        )
        responses = responses.rename(columns=dict(zip(columns, renamed_columns)))

        if "datestamp" in columns:
            # CSV file is unprocessed data
            raw_data = True

            # Identify columns for survey questions
            first_question = cast(int, columns.get_loc("datestamp")) + 1
            last_question = cast(int, columns.get_loc("interviewtime")) - 1
            question_columns = renamed_columns[first_question : last_question + 1]

            # Split df into question responses and timing info
            question_responses = responses.loc[:, question_columns]  # type: ignore  # the indexing works perfectly with the given slice, I think mypy got confused here?
            system_info = responses.iloc[:, ~renamed_columns.isin(question_columns)]

        else:
            # CSV file is previously processed data
            raw_data = False
            question_responses = responses
            system_info = pd.DataFrame()

        # Set correct categories for categorical fields
        # for column in self.questions.index:
        #     choices = self.questions.loc[column, "choices"]
        #     if (column in question_responses.columns) and pd.notnull(choices):
        #         question_responses.loc[:, column] = (
        #             question_responses.loc[:, column]
        #             # We expect all categorical column to be category dtype already
        #             #.astype("category")
        #             .cat.set_categories(choices.keys())
        #         )

        if raw_data:
            # Add missing columns for multiple-choice questions with contingent question
            # A contingent question of a multiple-choice question typically looks
            # like this:
            # <response varName="B1T">
            # <fixed>
            #  <category>
            #    <label>Other</label>
            #   <value>Y</value>
            #   <contingentQuestion varName="B1other">
            #    <text>Other</text>
            #     ...
            # For some reason, LimeSurvey does not export values for the parent
            # <response> (B1T in this case).
            # So, here we add those columns artificially based on the contingent
            # question values.
            multiple_choice_questions = self.questions.index[
                (self.questions["type"] == "multiple-choice")
                & self.questions["contingent_of_name"].notnull()
            ]
            for question in multiple_choice_questions:
                question_responses.insert(
                    cast(int, question_responses.columns.get_loc(question)),
                    self.questions.loc[question, "contingent_of_name"],
                    # Fill in new column based on "{question_id}other" column data
                    pd.Series(
                        question_responses[question].where(
                            question_responses[question].isnull(), "Y"
                        )
                    ),
                )

        # Validate data structure
        # Check for columns not listed in survey structure df
        not_in_structure = list(
            set(question_responses.columns) - set(self.questions.index)
        )
        if not_in_structure:
            warnings.warn(
                "The following columns in the data csv file are not found "
                f"in the survey structure and are dropped:\n{not_in_structure}",
                stacklevel=2,
            )
            question_responses = question_responses.drop(not_in_structure, axis=1)
        # Check for questions not listed in data csv
        not_in_data = list(set(self.questions.index) - set(question_responses.columns))
        if not_in_data:
            warnings.warn(
                "The following questions in the survey structure are not found "
                f"in the data csv file:\n{not_in_data}",
                stacklevel=2,
            )

        self.responses = question_responses
        self.lime_system_info = system_info

        if transformation_questions:
            for transform, questions in transformation_questions.items():
                for question in questions:
                    self.add_responses(self.transform_question(question, transform))

    def _get_dtype_info(
        self, columns: Iterable[str], renamed_columns: Iterable[str]
    ) -> tuple[
        dict[str, Union[str, pd.Int32Dtype, pd.UInt32Dtype, pd.Int16Dtype]], list[str]
    ]:
        """Get dtypes for columns in data csv

        Args:
            columns: Column names from data csv
            renamed_columns: Column names modified to match self.questions entries

        Returns:
            dict: Dictionary of column names and dtypes
            list: List of datetime columns
        """

        # Compile dict with dtype for each column
        dtype_dict: dict[
            str, Union[str, pd.Int32Dtype, pd.UInt32Dtype, pd.Int16Dtype]
        ] = {}
        # Compile list of datetime columns
        # (because pd.read_csv takes this as separate arg)
        datetime_columns = []

        for column, renamed_column in zip(columns, renamed_columns):
            # First try to infer dtype from XML structure information
            if renamed_column in self.questions.index:
                response_format = self.questions.loc[renamed_column, "format"]
                # Categorical dtype for all questions with answer options
                if pd.notnull(self.questions.loc[renamed_column, "choices"]):
                    dtype_dict[column] = "category"
                elif response_format == "date":
                    dtype_dict[column] = "str"
                    datetime_columns.append(column)
                elif response_format == "integer":
                    dtype_dict[column] = pd.Int32Dtype()
                elif response_format == "longtext":
                    dtype_dict[column] = "str"
                else:
                    # Do not include dtype
                    pass
            # Technical fields of limesurvey (Timing, Langueage, etc.)
            else:
                if column == "id":
                    dtype_dict[column] = pd.UInt32Dtype()
                elif column == "submitdate":
                    dtype_dict[column] = "str"
                    datetime_columns.append(column)
                elif column == "lastpage":
                    dtype_dict[column] = pd.Int16Dtype()
                elif column == "startlanguage":
                    dtype_dict[column] = "category"
                elif column == "seed":
                    dtype_dict[column] = pd.UInt32Dtype()
                elif column == "startdate" or column == "datestamp":
                    dtype_dict[column] = "str"
                    datetime_columns.append(column)
                # Float for all timing info
                elif re.search("[Tt]ime", column):
                    dtype_dict[column] = "float64"
                else:
                    # Do not include dtype
                    pass

        return dtype_dict, datetime_columns

    def export_Qs_to_CSV(self, output_path: Path) -> None:
        """
        export the question sheet from the survey to CSV

        Args:
            output_path (Path): output path to where CSV is saved
        """
        output_path.mkdir(parents=True, exist_ok=True)

        output = Path(output_path / "Q.csv")
        self.questions.to_csv(output)

    def get_question(self, question: str, drop_other: bool = False) -> pd.DataFrame:
        """Get question structure (i.e. subset from self.questions)

        Args:
            question: Name of question or subquestion
            drop_other: Whether to exclude contingent question (i.e. "other")
        Raises:
            ValueError: There is no such question or subquestion

        Returns:
            pd.DataFrame: Subset from `self.questions` with corresponding rows
        """

        questions_subdf = self.questions[
            (self.questions["question_group"] == question)
            | (self.questions.index == question)
        ]

        if questions_subdf.empty:
            raise ValueError(f"Unexpected question code '{question}'")

        if drop_other:
            questions_subdf = questions_subdf[~questions_subdf.is_contingent]

        return questions_subdf

    def get_choices(self, question: str) -> dict[str, str]:
        """Get choices of a question

        * For multiple-choice group, format is `<subquestion code: subquestion title>`,
          for example, {"C3_SQ001": "I do not like scientific work.", "C3_SQ002": ...}
        * For all other fixed questions (i.e. array, single choice, subquestion),
          returns choices of that question or column
        * For free and contingent, returns None

        Args:
            question (str): Name of question or subquestion to retrieve

        Returns:
            dict: dict of choices mappings
        """

        question_info = self.get_question(question)
        question_info = question_info[~question_info.is_contingent]
        question_type = self.get_question_type(question)

        # If set of multiple-choice questions
        if (question_info.shape[0] > 1) and (
            question_type == QuestionType.MULTIPLE_CHOICE
        ):
            # Flatten nested dict and get choice text directly for multiple-choice
            choices_dict = {
                cast(str, index): row.choices["Y"]
                for index, row in question_info.iterrows()
            }
        # If single-choice, free, individual subquestion, or array
        else:
            choices_dict = question_info.choices.iloc[0]

        return choices_dict

    def get_responses(
        self,
        question: str,
        drop_other: bool = False,
    ) -> pd.DataFrame:
        """Get responses for a given question with or without labels
        (and with or without contingent questions).

        Args:
            question: Question to get the responses for.
            drop_other: Whether to exclude contingent question (i.e. "other")

        Raises:
            ValueError: Inconsistent question types within question groups.
            ValueError: Unknown question types.

        Returns:
            [pd.DataFrame]: The response for the selected question.
        """
        question_group = self.get_question(question, drop_other=drop_other)
        question_type = self.get_question_type(question)

        responses = self.responses.loc[:, question_group.index]  # type:ignore  # see similar issue in read_responses; unclear if mypy is wrong or we actually misuse pandas here

        # convert multiple-choice responses
        if question_type == QuestionType.MULTIPLE_CHOICE:
            # ASSUME: question response consists of multiple columns with
            #         'Y' or NaN as entries.
            # Masked with boolean values the responses with nan only for
            # the columns where is_contingent is True.
            responses[question_group.index[~question_group.is_contingent]] = (
                responses.loc[:, ~question_group.is_contingent].notnull()
            )

        return responses

    def get_question_type(self, question: str) -> QuestionType:
        """Get question type and validate it

        Args:
            question (str): question or column code

        Raises:
            AssertionError: Unconsistent question types within question
            ValueError: Unexpected question type

        Returns:
            QuestionType: Question type like "single-choice", "array", etc.
        """

        question_group = self.get_question(question)
        question_types = question_group.type.unique()

        if len(question_types) > 1:
            raise AssertionError(
                f"Question {question} has multiple types {list(question_types)}."
            )

        question_type = QuestionType(question_types[0])

        return question_type

    def get_questions_by_type(self, type: QuestionType) -> list[str]:
        return list(
            self.questions.loc[self.questions["type"] == type.value]["question_group"]
            .unique()
            .tolist()
        )

    def query(self, expr: str) -> pd.DataFrame:
        """Filter responses DataFrame with a boolean expression

        Args:
            expr (str): Condition str for pd.DataFrame.query().
                E.g. "A6 == 'A3' & "B2 == 'A5'"

        Returns:
            pd.DataFrame: Filtered responses
        """

        return self.responses.query(expr)

    def add_responses(
        self,
        responses: pd.DataFrame,
        question: Optional[Union[str, tuple[tuple[str, str], tuple[str, str]]]] = None,
    ) -> None:
        """Add responses to specified question to self.responses DataFrame

        Args:
            responses (pd.Series or pd.DataFrame): responses to be added
                to self.responses
            question (list or str, optional): Name (id) of question to which
                the responses correspond. If not given, the column/Series name
                is taken as the name
        """
        raise NotImplementedError

    def transform_question(
        self,
        question: Union[str, tuple[tuple[str, str], tuple[str, str]]],
        transform: str,
    ) -> pd.DataFrame:
        """Perform transformation on responses to given question

        Args:
            question (str or tuple of str): Question(s) to transform
            transform (str): Type of transform to perform

        Returns:
            pd.DataFrame: Transformed DataFrame to be concatenated to self.responses
        """
        raise NotImplementedError


def main() -> None:
    pass
