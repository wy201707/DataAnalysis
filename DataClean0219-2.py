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
print(data[['姓名', '性别', '手机号', '就诊时间']].head(6))

# 标记复诊记录
data['就诊类型'] = data['性别'].apply(lambda x: '复诊' if x == '复诊' else '初诊')




# 提取初诊患者的手机号映射
baseline_data = data[data['性别'].isin(['1', '2', 1, 2])]  # 初诊记录
phone_mapping = baseline_data.set_index('姓名')['手机号'].to_dict()

# 填充复诊记录的手机号
data['手机号'] = data.apply(
    lambda row: phone_mapping.get(row['姓名'], None) if row['就诊类型'] == '复诊' else row['手机号'],
    axis=1
)


# 按姓名和手机号（或者初诊时间）生成唯一ID
def generate_patient_id(row):
    # 清洗姓名和手机号
    name = str(row['姓名']).strip().lower()  # 统一小写并去除空格
    phone = str(row['手机号']).strip() if pd.notnull(row['手机号']) else ''
    
    # 合并为字符串
    combined = f"{name}_{phone}"
    
    # 生成MD5哈希并取前8位
    return hashlib.md5(combined.encode()).hexdigest()[:8]

# 应用函数生成patient_id
data['patient_id'] = data.apply(generate_patient_id, axis=1)

# 检查是否有空值
if data['patient_id'].isnull().any():
    print("警告：存在无法生成patient_id的记录！")
    print(data[data['patient_id'].isnull()])

print("手机号+姓名生成patientID后的数据：")
print(data[['patient_id','姓名', '手机号', '就诊类型']].head())


# print("性别处理1后的数据：")
# print(data[['姓名', '性别', '就诊类型']].head())

baseline_gender = data[data['就诊类型'] == '初诊'][['姓名', '性别']].rename(columns={'性别': '初诊性别'})

# 步骤2：合并初诊性别到所有记录
data = pd.merge(data, baseline_gender, on='姓名', how='left')

# 步骤3：用初诊性别覆盖复诊记录的性别
data['性别'] = data.apply(lambda row: row['初诊性别'] if row['就诊类型'] == '复诊' else row['性别'], axis=1)
data = data.drop(columns='初诊性别')
# print("性别处理2后的数据：")
# print(data[['姓名', '性别', '就诊类型']].head())

# 映射性别编码为文字  这里再覆盖复诊未填写个人信息时候需要排除 姓名 就诊时间 性别三列
data['性别'] = data['性别'].map({1: '男性', 2: '女性'})

print("性别处理3后的数据：")
print(data[['姓名', '性别', '就诊类型']].head())

# 统一转换为标准日期格式
# 定义日期转换函数
def convert_date(date_val):
    """
    支持以下格式的日期转换：
    1. Excel日期序列号（如 45366 → 2024/03/15）
    2. 字符串格式 DD/MM/YYYY（如 20/09/2024 → 2024/09/20）
    3. 字符串格式 YYYY/MM/DD（直接保留）
    """
    try:
        # 处理数值型Excel日期序列号
        if isinstance(date_val, (int, float)):
            return pd.to_datetime(date_val, unit='d', origin='1899-12-30').strftime('%Y/%m/%d')
        
        # 转换为字符串并清理空格
        date_str = str(date_val).strip()
        
        # 处理空值
        if date_str in ["", "nan", "NaT"]:
            return "Invalid Date"
        
        # 尝试匹配 DD/MM/YYYY 格式
        match_ddmmyyyy = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', date_str)
        if match_ddmmyyyy:
            day, month, year = match_ddmmyyyy.groups()
            return f"{year}/{month.zfill(2)}/{day.zfill(2)}"  # 统一补零
        
        # 尝试匹配 YYYY/MM/DD 格式
        match_yyyymmdd = re.match(r'^(\d{4})/(\d{1,2})/(\d{1,2})$', date_str)
        if match_yyyymmdd:
            year, month, day = match_yyyymmdd.groups()
            return f"{year}/{month.zfill(2)}/{day.zfill(2)}"  # 统一补零
        
        # 处理其他可能的格式（如YYYY-MM-DD）
        return pd.to_datetime(date_str, errors='coerce').strftime('%Y/%m/%d')
    
    except:
        return "Invalid Date"

# 统一处理日期列
data['就诊时间'] = (
    data['就诊时间']
    .astype(str)  # 强制转换为字符串
    .str.strip()   # 去除首尾空格
    .replace({'nan': '', 'NaT': ''}, regex=False)  # 清理缺失值标记
    .apply(convert_date)
)

# 检查无效日期
invalid_dates = data[data['就诊时间'] == 'Invalid Date']
if not invalid_dates.empty:
    print("发现以下无效日期记录，请手动检查：")
    print(invalid_dates[['patient_id', '姓名', '就诊时间']])
else:
    print("所有日期已成功转换！")



# 显示结果
print("\n转换后的日期示例：")
print(data[['patient_id', '姓名', '就诊时间']].head(10))

'''
# 确保就诊时间为日期类型
data['就诊时间'] = pd.to_datetime(data['就诊时间'], errors='coerce')

# 按患者和就诊时间排序
data = data.sort_values(by=['patient_id', '就诊时间'])

# 计算每个患者的就诊次数
data['diagnosis_num'] = data.groupby('patient_id').cumcount() + 1

print("就诊次数示例：")
print(data[['patient_id', '姓名', '就诊时间', 'diagnosis_num']].head(10))

'''
'''
# 假设未来新增复诊记录（示例）
new_data = pd.DataFrame({
    '姓名': ['张三'],
    '性别': ['复诊'],
    '手机号': [None],  # 未来复诊可能不填手机号
    '就诊时间': ['2023-05-01']
})


# 合并新数据并填充手机号
new_data = pd.concat([data, new_data], ignore_index=True)
new_data['手机号'] = new_data.apply(
    lambda row: phone_mapping.get(row['姓名'], None) if row['就诊类型'] == '复诊' else row['手机号'],
    axis=1
)

# 重新生成patient_id和就诊次数
new_data['patient_id'] = new_data.apply(generate_patient_id, axis=1)
new_data = new_data.sort_values(by=['patient_id', '就诊时间'])
new_data['diagnosis_num'] = new_data.groupby('patient_id').cumcount() + 1

print("新增复诊后的示例：")
print(new_data[['patient_id', '姓名', '就诊时间', 'diagnosis_num']].tail(3))

'''
data.to_excel('cleaned_data2.xlsx', index=False)
