import json
import os

import pandas as pd


class OutputResolver:
    def __init__(self, path_to_save: str):
        self.path = path_to_save

    def create_json_result(self, col_row_data: list[list[str]], header_texts: list[str]):
        df = self.convert_from_list_to_df(col_row_data)
        df = dataframe_to_json(df)
        json_df = df.to_json(force_ascii=False)
        json_data = json.loads(json_df)
        if len(header_texts) > 0:
            json_data["headers"] = header_texts
        json_df_str = json.dumps(json_data, ensure_ascii=False)
        return json_df_str
        # self.write_json_str_to_file(json_df_str, self.path)

    def write_result(self, json_str: str):
        self.write_json_str_to_file(json_str, self.path)

    @staticmethod
    def convert_from_list_to_df(list_data: list[list[str]]) -> pd.DataFrame:
        first_row = list_data[0]
        df = pd.DataFrame(list_data[1:], columns=first_row)
        return df

    @staticmethod
    def write_json_str_to_file(json_str: str, file_path: str):
        with open(file_path, "w", encoding="utf8") as outfile:
            outfile.write(json_str)


def dataframe_to_json(df):
    # Check for non-unique columns
    non_unique_columns = df.columns.duplicated()
    names_columns = df.columns.to_list()
    if any(non_unique_columns):
        # If non-unique columns exist, rename them by appending a unique identifier
        for column_index, is_duplicate in enumerate(non_unique_columns):
            if is_duplicate:
                column_name = df.columns[column_index]

                new_column_name = f"{column_name}_{column_index}"
                names_columns[column_index] = new_column_name

        df.columns = names_columns
    return df
