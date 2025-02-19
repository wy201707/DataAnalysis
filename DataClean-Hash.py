import pandas as pd
import hashlib

# 加载初诊和复诊数据
data_file = 'data2.17.xlsx'  # 假设数据存储在data.xlsx文件中
baseline_data = pd.read_excel(data_file, sheet_name='baseline')
follow_up_data = pd.read_excel(data_file, sheet_name='follow_up')

# 添加时间标记
baseline_data['time'] = 'baseline'
follow_up_data['time'] = 'follow-up'

# 合并数据
data = pd.concat([baseline_data, follow_up_data], ignore_index=True)

# 统一就诊时间格式
data['first_diagnosis_time'] = pd.to_datetime(data['first_diagnosis_time'], errors='coerce')

# 生成patient_id（使用姓名和手机号的哈希值）
def generate_patient_id(row):
    # 将姓名和手机号组合为字符串
    combined = f"{row['姓名']}_{row['手机号']}"
    # 生成哈希值
    return hashlib.md5(combined.encode()).hexdigest()[:8]  # 取前8位作为patient_id

# 应用函数生成patient_id
data['patient_id'] = data.apply(generate_patient_id, axis=1)

# 按patient_id和first_diagnosis_time排序
data = data.sort_values(by=['patient_id', 'first_diagnosis_time'])

# 记录复诊次数
data['visit_num'] = data.groupby('patient_id').cumcount() + 1  # 从1开始编号

# 生成唯一标识
def generate_unique_id(group):
    if len(group) == 1:
        group['unique_id'] = f"fd_{group['patient_id'].iloc[0]}"
    else:
        group['unique_id'] = [f"fd_{group['patient_id'].iloc[0]}"] + \
                             [f"fl_{i}_{group['patient_id'].iloc[0]}" for i in range(1, len(group))]
    return group

# 应用函数生成unique_id
data = data.groupby('patient_id').apply(generate_unique_id).reset_index(drop=True)

# 将数据拆分为baseline和follow_up
baseline_data = data[data['time'] == 'baseline']
follow_up_data = data[data['time'] == 'follow-up']

# 查看结果
print("Baseline Data:")
print(baseline_data[['姓名', '手机号', 'first_diagnosis_time', 'patient_id', 'unique_id', 'visit_num']].head(10))

print("Follow-up Data:")
print(follow_up_data[['姓名', '手机号', 'follow_up_time', 'patient_id', 'unique_id', 'visit_num']].head(10))