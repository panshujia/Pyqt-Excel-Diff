import os
import random
import string
import pandas as pd

# 生成随机单词
def generate_random_word(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# 随机修改 DataFrame 中的一些单元格
def modify_random_cells(df, num_changes=10):
    rows, cols = df.shape
    for _ in range(num_changes):
        row_idx = random.randint(0, rows - 1)
        col_idx = random.randint(0, cols - 1)
        df.iloc[row_idx, col_idx] = generate_random_word()  # 修改为随机单词
    return df

# 扫描当前目录下的所有 .xlsx 文件并随机修改内容
def modify_excel_files_in_directory():
    current_dir = os.getcwd()
    xlsx_files = [f for f in os.listdir(current_dir) if f.endswith('.xlsx')]

    for file_name in xlsx_files:
        print(f"正在处理文件: {file_name}")
        
        # 读取 Excel 文件
        xl = pd.ExcelFile(file_name, engine='openpyxl')
        
        # 创建一个新的 ExcelWriter 写入器
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            # 遍历所有工作表
            for sheet_name in xl.sheet_names:
                df = xl.parse(sheet_name, header=None)
                
                # 随机修改表格中的单元格
                modified_df = modify_random_cells(df)
                
                # 将修改后的 DataFrame 写入 Excel 文件
                modified_df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

            # 获取工作簿对象
            workbook = writer.book
            for sheet_name in xl.sheet_names:
                sheet = workbook[sheet_name]
                # 确保至少一个工作表是可见的
                sheet.sheet_state = 'visible'
        
        print(f"文件 '{file_name}' 修改完成！")

# 调用修改 Excel 文件的函数
modify_excel_files_in_directory()
