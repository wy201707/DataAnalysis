import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
################## 初步数据清理结束，开始统计  ##########################
data = pd.read_excel('cleaned_data.xlsx')


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

