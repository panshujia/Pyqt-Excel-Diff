import pandas as pd

id = 'ID'

class ExcelDiffChecker:
    def __init__(self, left_file, right_file):
        # 读取 Excel 文件
        self.left_df = pd.read_excel(left_file)
        self.right_df = pd.read_excel(right_file)

    def compare_by_id(self):
        # 获取 id 列
        left_ids = set(self.left_df[id])
        right_ids = set(self.right_df[id])

        # 找出新增和删除的 id
        added_ids = right_ids - left_ids
        removed_ids = left_ids - right_ids

        return added_ids, removed_ids

    def get_added_rows(self, added_ids):
        # 返回新增的行
        return self.right_df[self.right_df[id].isin(added_ids)]

    def get_removed_rows(self, removed_ids):
        # 返回删除的行
        return self.left_df[self.left_df[id].isin(removed_ids)]

    def compare_columns(self):
        # 比较列名，检查是否有新增的列
        left_columns = set(self.left_df.columns)
        right_columns = set(self.right_df.columns)

        added_columns = right_columns - left_columns
        removed_columns = left_columns - right_columns

        return added_columns, removed_columns

    def compare_values(self):
        # 检查相同 ID 的行对应的列值是否有变化
        changes = []
        for idx, left_row in self.left_df.iterrows():
            id_value = left_row[id]
            if id_value in self.right_df[id].values:
                right_row = self.right_df[self.right_df[id] == id_value].iloc[0]
                for col in self.left_df.columns:
                    if col in self.right_df.columns and left_row[col] != right_row[col]:
                        changes.append({
                            'ID': id_value,
                            'Column': col,
                            'Left Value': left_row[col],
                            'Right Value': right_row[col]
                        })
        return changes

    def print_diff(self):
        # 比较并输出差异
        added_ids, removed_ids = self.compare_by_id()

        # 输出新增的行
        if added_ids:
            print("新增的行 (Added rows):")
            added_rows = self.get_added_rows(added_ids)
            print(added_rows)
        else:
            print("没有新增的行。")

        # 输出删除的行
        if removed_ids:
            print("删除的行 (Removed rows):")
            removed_rows = self.get_removed_rows(removed_ids)
            print(removed_rows)
        else:
            print("没有删除的行。")

        # 输出新增的列
        added_columns, removed_columns = self.compare_columns()
        if added_columns:
            print("新增的列 (Added columns):")
            print(added_columns)
        else:
            print("没有新增的列。")

        if removed_columns:
            print("删除的列 (Removed columns):")
            print(removed_columns)
        else:
            print("没有删除的列。")

        # 输出值变化
        changes = self.compare_values()
        if changes:
            print("值变化 (Value changes):")
            for change in changes:
                print(f"ID: {change['ID']}, 列: {change['Column']}, 左侧值: {change['Left Value']}, 右侧值: {change['Right Value']}")
        else:
            print("没有值变化。")


if __name__ == "__main__":
    # 这里假设传入的是两个 Excel 文件的路径
    left_file = "test_2.xlsx"  # 左侧文件
    right_file = "test_1.xlsx"  # 右侧文件

    # 创建 ExcelDiffChecker 实例
    checker = ExcelDiffChecker(left_file, right_file)

    # 打印出差异
    checker.print_diff()
