from typing import Iterable, Optional, Union
import warnings
import re
import pandas as pd
from pathlib import Path

from .survey_structure import read_lime_questionnaire_structure


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
        transformation_questions: dict[str, str] = {},
    ) -> None:
        """Read responses CSV file

        Args:
            responses_file (str): Path to the responses CSV file
            transformation_questions (dict, optional): Dict of questions
                requiring transformation of raw data, e.g. {'depression': 'D3'}
                or {'supervision': ['E7a', 'E7b']}
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
            first_question = columns.get_loc("datestamp") + 1
            last_question = columns.get_loc("interviewtime") - 1
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
            # A contingent question of a multiple-choice question typically looks like this:
            # <response varName="B1T">
            # <fixed>
            #  <category>
            #    <label>Other</label>
            #   <value>Y</value>
            #   <contingentQuestion varName="B1other">
            #    <text>Other</text>
            #     ...
            # For some reason, LimeSurvey does not export values for the parent <response> (B1T in this case).
            # So, here we add those columns artificially based on the contingent question values.
            multiple_choice_questions = self.questions.index[
                (self.questions["type"] == "multiple-choice")
                & self.questions["contingent_of_name"].notnull()
            ]
            for question in multiple_choice_questions:
                question_responses.insert(
                    question_responses.columns.get_loc(question),
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
                f"The following columns in the data csv file are not found in the survey structure and are dropped:\n{not_in_structure}"
            )
            question_responses = question_responses.drop(not_in_structure, axis=1)
        # Ceheck for questions not listed in data csv
        not_in_data = list(set(self.questions.index) - set(question_responses.columns))
        if not_in_structure:
            warnings.warn(
                f"The following questions in the survey structure are not found in the data csv file:\n{not_in_data}"
            )

        self.responses = question_responses
        self.lime_system_info = system_info

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
            columns (list): List of column names from data csv
            renamed_columns (list): List of column names modified to match self.questions entries

        Returns:
            dict: Dictionary of column names and dtypes
            list: List of datetime columns
        """

        # Compile dict with dtype for each column
        dtype_dict: dict[
            str, Union[str, pd.Int32Dtype, pd.UInt32Dtype, pd.Int16Dtype]
        ] = {}
        # Compile list of datetime columns (because pd.read_csv takes this as separate arg)
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
                elif column == "startdate":
                    dtype_dict[column] = "str"
                    datetime_columns.append(column)
                elif column == "datestamp":
                    dtype_dict[column] = "str"
                    datetime_columns.append(column)
                # Float for all timing info
                elif re.search("[Tt]ime", column):
                    dtype_dict[column] = "float64"
                else:
                    # Do not include dtype
                    pass

        return dtype_dict, datetime_columns

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
