import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
data = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 显示前几行数据，确认列名和格式
print("原始数据示例：")
print(data.head())


# 将性别列转换为字符串类型，避免数值和字符串混合
data['性别'] = data['性别'].astype(str)

# 标记初诊和复诊记录
data['就诊类型'] = data['性别'].apply(lambda x: '复诊' if x == '复诊' else '初诊')

# 为每个患者填充初诊性别到复诊记录中
# 步骤1：提取初诊患者的性别
baseline_gender = data[data['就诊类型'] == '初诊'][['姓名', '性别']].rename(columns={'性别': '初诊性别'})

# 步骤2：合并初诊性别到所有记录
data = pd.merge(data, baseline_gender, on='姓名', how='left')

# 步骤3：用初诊性别覆盖复诊记录的性别
data['性别'] = data.apply(lambda row: row['初诊性别'] if row['就诊类型'] == '复诊' else row['性别'], axis=1)
data = data.drop(columns='初诊性别')

# 映射性别编码为文字
data['性别'] = data['性别'].map({'1': '男性', '2': '女性'})

print("性别处理后的数据：")
print(data[['姓名', '性别', '就诊类型']].head())


# 统一转换为标准日期格式


# 按姓名和初诊时间生成唯一ID

# 按患者和就诊时间排序
data = data.sort_values(by=['patient_id', '就诊时间'])

# 计算每个患者的就诊次数
data['diagnosis_time'] = data.groupby('patient_id').cumcount() + 1

print("就诊次数示例：")
print(data[['patient_id', '姓名', '就诊时间', 'diagnosis_time']].head(10))

key_metrics = ['TCM_syndromes_score', 'indicator2', 'indicator3', 'indicator4']

# 总体描述性统计
print("总体描述性统计：")
print(data[key_metrics].describe())

# 按治疗阶段（初诊/复诊）分组统计
print("按治疗阶段分组统计：")
print(data.groupby('就诊类型')[key_metrics].describe())

# 设置绘图风格
sns.set_theme(style="whitegrid")

# 箱线图：治疗前后评分分布
plt.figure(figsize=(12, 8))
for i, metric in enumerate(key_metrics, 1):
    plt.subplot(2, 2, i)
    sns.boxplot(x='就诊类型', y=metric, data=data)
    plt.title(f'{metric} Distribution')
plt.tight_layout()
plt.show()

# 折线图：单个患者治疗变化示例（随机选3名患者）
sample_patients = data['patient_id'].drop_duplicates().sample(3)
plt.figure(figsize=(12, 6))
for pid in sample_patients:
    patient_data = data[data['patient_id'] == pid]
    plt.plot(patient_data['diagnosis_time'], patient_data['indicator2'], marker='o', label=f'Patient {pid}')
plt.xlabel('Diagnosis Time')
plt.ylabel('VAS Score')
plt.title('VAS Score Changes for Sampled Patients')
plt.legend()
plt.show()

# 提取用药组数据（假设用药组标记为'A组'）
treatment_group = data[data['组别'] == 'A组']

# 计算每个患者的初诊和复诊评分差值
baseline = treatment_group[treatment_group['diagnosis_time'] == 1][['patient_id'] + key_metrics].set_index('patient_id')
follow_up = treatment_group[treatment_group['diagnosis_time'] == 2][['patient_id'] + key_metrics].set_index('patient_id')

# 合并初诊和复诊数据
change = follow_up - baseline
change = change.dropna()

# 输出变化值统计
print("治疗前后评分变化统计：")
print(change.describe())

# 绘制变化值分布
plt.figure(figsize=(12, 6))
for i, metric in enumerate(key_metrics, 1):
    plt.subplot(2, 2, i)
    sns.histplot(change[metric], kde=True)
    plt.title(f'{metric} Change Distribution')
plt.tight_layout()
plt.show()

data.to_excel('cleaned_data.xlsx', index=False)