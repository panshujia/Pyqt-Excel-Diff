import pandas as pd

id = 'ID'

class DiffAlg:
    def __init__(self, left_excel: pd.ExcelFile, right_excel: pd.ExcelFile):
        self.left_excel = right_excel
        self.right_excel = left_excel

    def compare_by_id(self, left_df, right_df):
        left_ids = set(left_df[id])
        right_ids = set(right_df[id])
        added_ids = right_ids - left_ids
        removed_ids = left_ids - right_ids
        return added_ids, removed_ids

    def get_added_rows(self, added_ids, right_df):
        added_rows = right_df[right_df[id].isin(added_ids)]
        return added_rows

    def get_removed_rows(self, removed_ids, left_df):
        removed_rows = left_df[left_df[id].isin(removed_ids)]
        return removed_rows

    def compare_columns(self, left_df, right_df):
        left_columns = set(left_df.columns)
        right_columns = set(right_df.columns)
        added_columns = right_columns - left_columns
        removed_columns = left_columns - right_columns
        return added_columns, removed_columns

    def compare_values(self, left_df, right_df):
        changes = []
        for idx, left_row in left_df.iterrows():
            id_value = left_row[id]
            if id_value in right_df[id].values:
                right_row = right_df[right_df[id] == id_value].iloc[0]
                for col in left_df.columns:
                    if col in right_df.columns and left_row[col] != right_row[col]:
                        left_row_idx = left_df.index.get_loc(idx)
                        right_row_idx = right_df[right_df[id] == id_value].index[0]
                        col_idx = left_df.columns.get_loc(col)
                        changes.append({
                            'ID': id_value,
                            'row_idx': left_row_idx,
                            'col_name': col,
                            'l_value': left_row[col],
                            'r_value': right_row[col],
                            'l_row_idx': left_row_idx,
                            'r_row_idx': right_row_idx,
                            'col_idx': col_idx
                        })
        return changes

    def get_diff_for_sheet(self, left_df, right_df):
        diff_dict = {}
        added_ids, removed_ids = self.compare_by_id(left_df, right_df)

        if added_ids:
            added_rows = self.get_added_rows(added_ids, right_df)
            diff_dict['added_rows'] = added_rows

        if removed_ids:
            removed_rows = self.get_removed_rows(removed_ids, left_df)
            diff_dict['removed_rows'] = removed_rows

        added_columns, removed_columns = self.compare_columns(left_df, right_df)
        if added_columns:
            diff_dict['added_columns'] = added_columns

        if removed_columns:
            diff_dict['removed_columns'] = removed_columns

        changes = self.compare_values(left_df, right_df)
        if changes:
            diff_dict['data_changes'] = changes

        return diff_dict

    def get_all_diff(self):
        diff_results = {}
        left_sheets = set(self.left_excel.sheet_names)
        right_sheets = set(self.right_excel.sheet_names)

        added_sheets = right_sheets - left_sheets
        removed_sheets = left_sheets - right_sheets

        if added_sheets:
            diff_results['added_sheets'] = list(added_sheets)
        if removed_sheets:
            diff_results['removed_sheets'] = list(removed_sheets)

        for sheet_name in self.left_excel.sheet_names:
            if sheet_name in self.right_excel.sheet_names:
                left_df = self.left_excel.parse(sheet_name)
                right_df = self.right_excel.parse(sheet_name)
                diff_results[sheet_name] = self.get_diff_for_sheet(left_df, right_df)

        return diff_results

    def print_diff(self):
        diff_results = self.get_all_diff()
        if 'added_sheets' in diff_results:
            print("新增的工作表 (Added sheets):", diff_results['added_sheets'])

        if 'removed_sheets' in diff_results:
            print("删除的工作表 (Removed sheets):", diff_results['removed_sheets'])

        for sheet_name, sheet_diff in diff_results.items():
            if sheet_name not in ['added_sheets', 'removed_sheets']:
                print(f"\n工作表 '{sheet_name}' 的差异:")
                if 'added_rows' in sheet_diff:
                    print("新增的行 (Added rows):", sheet_diff['added_rows'])

                if 'removed_rows' in sheet_diff:
                    print("删除的行 (Removed rows):", sheet_diff['removed_rows'])

                if 'added_columns' in sheet_diff:
                    print("新增的列 (Added columns):", sheet_diff['added_columns'])

                if 'removed_columns' in sheet_diff:
                    print("删除的列 (Removed columns):", sheet_diff['removed_columns'])

                if 'data_changes' in sheet_diff:
                    print("值变化 (Value changes):", sheet_diff['data_changes'])
                else:
                    print("没有值变化。")



if __name__ == "__main__":
    left_excel = pd.ExcelFile("test_1.xlsx", engine="openpyxl")
    right_excel = pd.ExcelFile("test_2.xlsx", engine="openpyxl")

    checker = DiffAlg(left_excel, right_excel)

    checker.print_diff()
