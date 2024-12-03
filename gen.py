import pandas as pd
import random
from datetime import datetime, timedelta

def generate_excel(file_name, num_rows=10):
    # 创建数据
    data = {
        'ID': [i for i in range(1, num_rows + 1)],  # ID 列从 1 到 num_rows
        'Name': ['Name' + str(i) for i in range(1, num_rows + 1)],  # 填充名字列
        'Age': [20 + (i % 10) for i in range(num_rows)],  # 填充年龄列，20 到 29 岁
        'Gender': [random.choice(['Male', 'Female']) for _ in range(num_rows)],  # 随机选择性别
        'Score': [round(random.uniform(50, 100), 2) for _ in range(num_rows)],  # 随机生成成绩
        'Date': [(datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(num_rows)]  # 随机日期
    }
    
    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 将 DataFrame 写入 Excel 文件
    df.to_excel(file_name, index=False)

    print(f"Excel 文件 {file_name} 已生成！")

# 使用示例
if __name__ == "__main__":
    generate_excel("test_1.xlsx", num_rows=100)  # 生成 10 行的数据
    # generate_excel("test_2.xlsx", num_rows=100)  # 生成 10 行的数据
    # generate_excel("test_3.xlsx", num_rows=100)  # 生成 10 行的数据
