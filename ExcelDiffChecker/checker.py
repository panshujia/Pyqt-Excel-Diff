import pandas as pd
import hashlib
import datetime

class MyAlg:
    statueSignal = None
    YZ = 0.5  # 匹配成功的阈值 0~1 越高精准度越高
    PP = 0.8  # 用于不需要跑完全部行，加速比较，PP >= YZ

    # 最长公共子串
    def lcsub(self, s1, s2):
        m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
        mmax = 0  # 最长匹配的长度
        p = 0  # 最长匹配对应在 s1 中的最后一位
        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]:
                    m[i + 1][j + 1] = m[i][j] + 1
                    if m[i + 1][j + 1] > mmax:
                        mmax = m[i + 1][j + 1]
                        p = i + 1
        return s1[p - mmax:p], mmax, p - mmax  # 返回最长子串及其长度，和起始位置

    def lcs(self, a, b, lena, lenb):
        c = [[0 for i in range(lenb + 1)] for j in range(lena + 1)]
        for i in range(lena):
            for j in range(lenb):
                if a[i] == b[j]:
                    c[i + 1][j + 1] = c[i][j] + 1
                elif c[i + 1][j] > c[i][j + 1]:
                    c[i + 1][j + 1] = c[i + 1][j]
                else:
                    c[i + 1][j + 1] = c[i][j + 1]
        return c[lena][lenb]

    def binary_search(self, num):
        start = 0
        end = len(self.LIS) - 1

        if self.LIS[0] > num:
            return 0

        while end - start > 1:
            middle = (start + end) // 2

            if self.LIS[middle] > num:
                end = middle
            elif self.LIS[middle] < num:
                start = middle
            else:
                return middle

        return end

    def lis(self, nums):
        if len(nums) == 0:
            return 0
        self.LIS = [nums[0]]
        for i in range(1, len(nums)):
            num = nums[i]
            if num > self.LIS[-1]:
                self.LIS.append(num)
            else:
                index = self.binary_search(num)
                self.LIS[index] = num
        return self.LIS

    def intToABC(self, n):
        d = {}
        r = []
        a = ''
        for i in range(1, 27):
            d[i] = chr(64 + i)
        if n <= 26:
            return d[n]
        if n % 26 == 0:
            n = n // 26 - 1
            a = 'Z'
        while n > 26:
            s = n % 26
            n = n // 26
            r.append(s)
        result = d[n]
        for i in r[::-1]:
            result += d[i]
        return result + a

    def hashlist(self, li):
        ans = "!@#$%$"
        for data in li:
            ans = ans + str(data)
            ans = hashlib.md5(ans.encode(encoding='UTF-8')).hexdigest()[0:16]
        return ans
    def compare_with_nan(self, val1, val2):
        # 使用 pd.isna() 判断 NaN 值，并将它们视为相等
        return (pd.isna(val1) & pd.isna(val2)) | (val1 == val2)

    # 计算最长公共子串 (LCSub) 相似度
    def lcsub(self, s1, s2):
        m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
        mmax = 0  # 最长匹配的长度
        p = 0  # 最长匹配对应在 s1 中的最后一位
        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]:
                    m[i + 1][j + 1] = m[i][j] + 1
                    if m[i + 1][j + 1] > mmax:
                        mmax = m[i + 1][j + 1]
                        p = i + 1
        return mmax  # 返回最长子串的长度

    # 比较两行的相似度，如果相似度小于阈值，则判定为不相似
    def compare_rows(self, row1, row2, threshold=0.8):
        # 将行转换为字符串进行比较
        row1_str = ''.join(str(x) for x in row1)
        row2_str = ''.join(str(x) for x in row2)
        
        # 计算最长公共子串的相似度
        similarity = self.lcsub(row1_str, row2_str) / max(len(row1_str), len(row2_str))
        
        # 如果相似度小于阈值，认为两行不相似
        return similarity >= threshold
    
    def getSheetsdiff(self, old_file, new_file, n=3):
        """
        比较多个 Sheet 的差异
        """
        print("开始分析...")

        lt = datetime.datetime.now()
        diff = dict()

        # 读取 Excel 文件中的所有 Sheets（对于 pd.ExcelFile 对象，使用 .parse() 获取数据）
        if isinstance(old_file, pd.ExcelFile):
            old_sheets = {sheet: old_file.parse(sheet, header=None) for sheet in old_file.sheet_names}
        else:
            old_sheets = old_file  # Assuming it's already a dictionary of DataFrames

        if isinstance(new_file, pd.ExcelFile):
            new_sheets = {sheet: new_file.parse(sheet, header=None) for sheet in new_file.sheet_names}
        else:
            new_sheets = new_file  # Assuming it's already a dictionary of DataFrames

        # 对比每个 sheet
        for sheet_name, old_df in old_sheets.items():
            if sheet_name in new_sheets:
                new_df = new_sheets[sheet_name]
                print(f"比较Sheet：{sheet_name}")
                diff[sheet_name] = self.__getSheetdiff(old_df, new_df, n)
            else:
                diff[sheet_name] = {"error": "新文件中没有该Sheet"}

        ct = datetime.datetime.now()
        print("比较完成!", (ct - lt).seconds)

        return diff

    def __getSheetdiff(self, old_df, new_df, n=3):
        """
        使用 pandas 计算旧表和新表的差异
        """
        print("开始分析...")

        lt = datetime.datetime.now()
        diff = dict()

        # 重置索引，确保两个 DataFrame 的索引一致
        old_df = old_df.reset_index(drop=True)
        new_df = new_df.reset_index(drop=True)

        # 计算数据变更
        diff["data_changes"] = []
        for idx, row in old_df.iterrows():
            if idx < len(new_df):  # 确保 idx 在 new_df 中有效
                for col in old_df.columns:
                    if not self.compare_with_nan(old_df.at[idx, col], new_df.at[idx, col]):
                        diff["data_changes"].append({
                                "row": idx,
                                "column": col,
                                "old_value": old_df.at[idx, col],
                                "new_value": new_df.at[idx, col]
                         })

        # # 检查是否删除了某些行
        # diff["deleted_rows"] = []
        # for old_idx, old_row in old_df.iterrows():
        #     # 判断是否有对应的行在新表中（检查上下n行的相似度）
        #     matched = False
        #     for new_idx in range(max(0, old_idx - n), min(len(new_df), old_idx + n + 1)):
        #         new_row = new_df.iloc[new_idx]
        #         if self.compare_rows(old_row, new_row):
        #             matched = True
        #             break
        #     if not matched:
        #         diff["deleted_rows"].append({
        #             "row": old_idx,
        #             "old_data": old_row.tolist()
        #         })

        ct = datetime.datetime.now()
        print("cal_data_changes_done!", (ct - lt).seconds)
        print("cal_deleted_rows_done!", (ct - lt).seconds)

        return diff 


# 测试
def main():
    # 创建 MyAlg 对象
    my_alg = MyAlg()

    # 读取 Excel 文件 - 旧数据和新数据
    old_file_path = 'test_1.xlsx'  # 这里是旧文件的路径
    new_file_path = 'test_2.xlsx'  # 这里是新文件的路径

    # 获取差异
    diff = my_alg.getSheetsdiff(old_file_path, new_file_path)

    # 输出差异
    print("表格差异:", diff)


if __name__ == "__main__":
    main()
