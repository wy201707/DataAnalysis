import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import hashlib
import pandas as pd
import re

# 加载数据
data = pd.read_excel('data2.17.xlsx', sheet_name='Sheet1')
# 显示前几行数据
print("原始数据示例：")
print(data[['姓名',  '就诊时间']].head(6))

# 统一转换为标准日期格式
print(data['就诊时间'].dtype)  # 检查列类型
print(data['就诊时间'].apply(type).value_counts())  # 查看实际存储类型


# # 方法1：严格类型检查（查找非Timestamp类型）
# non_datetime_mask = data['就诊时间'].apply(lambda x: not isinstance(x, pd.Timestamp))
# non_datetime_indices = data[non_datetime_mask].index.tolist()

# # 方法2：综合有效性检查（包含NaT和类型异常）
# invalid_dates_mask = (data['就诊时间'].isna()) | (data['就诊时间'].apply(
#     lambda x: not isinstance(x, pd.Timestamp)))
# invalid_indices = data[invalid_dates_mask].index.tolist()

# print(f"严格类型异常行号：{non_datetime_indices}")
# print(f"综合无效日期行号：{invalid_indices}")

# 统一转换日期格式（增强版）
def convert_date(x):
    # 处理浮点型Excel日期
    if isinstance(x, float):
        return pd.Timestamp('1899-12-30') + pd.Timedelta(days=x)
    
    # 处理字符串日期
    if isinstance(x, str):
        # 清洗非常规字符
        x = re.sub(r'[^0-9/]', '', x)
        # 尝试多种日期格式
        for fmt in ['%Y/%m/%d', '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
            try:
                return pd.to_datetime(x, format=fmt)
            except:
                continue
    return pd.NaT

data['就诊时间'] = data['就诊时间'].apply(convert_date)

# 有效性验证
invalid_dates = data[data['就诊时间'].isna()]
print(f"无效日期记录数：{len(invalid_dates)}")
print(invalid_dates[['姓名', '就诊时间']].head())

# 生成可视化报告
plt.figure(figsize=(10,6))
data['就诊时间'].dt.year.value_counts().sort_index().plot(kind='bar')
plt.title('就诊年份分布')
plt.show()
