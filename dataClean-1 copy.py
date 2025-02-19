import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

# 加载初诊和复诊数据
baseline_data = pd.read_csv('baseline.csv')
follow_up_data = pd.read_csv('follow_up.csv')

# 添加时间标记
baseline_data['time'] = 'baseline'
follow_up_data['time'] = 'follow-up'

# 合并数据
data = pd.concat([baseline_data, follow_up_data], ignore_index=True)


# 检查缺失值并处理（如填充或删除）。
# 检查异常值（如年龄为负数或身高/体重不合理）。
# #####标记不合理（记录名字或患者编号）

########## ？？这里如何处理缺失值？
# # 检查缺失值
# print(data.isnull().sum())
# # 填充缺失值（如用中位数填充） 这步好像不合理
# data.fillna(data.median(), inplace=True)

# 2. 描述性统计
# 对两组患者的基本信息和关键指标进行描述性统计：
# 连续变量：均值、标准差、中位数、四分位距。
# 分类变量：频数和百分比。


# 连续变量
print(data[['age', 'BMI', 'indicator2', 'indicator3', 'indicator4']].describe())

# 分类变量
# ########print(data['gender'].value_counts(normalize=True))  这个没必要，但是需要补全 vlookup不全

# 3. 关键指标分析
# 3.1 计算指标变化
# 对每个患者，计算关键指标（如VAS评分、WOMAC评分、Lysholm评分）的变化值：

# 变化值 = 复诊值 - 初诊值


# 计算变化值
data_change = data.pivot(index='patient_id', columns='time', values=['indicator2', 'indicator3', 'indicator4'])
data_change = data_change.droplevel(0, axis=1).reset_index()
data_change['VAS_change'] = data_change['follow-up'] - data_change['baseline']
data_change['WOMAC_change'] = data_change['follow-up'] - data_change['baseline']
data_change['Lysholm_change'] = data_change['follow-up'] - data_change['baseline']


# 绘制VAS评分变化箱线图
sns.boxplot(x='treatment_group', y='VAS_change', data=data_change)
plt.title('VAS Score Change by Treatment Group')
plt.show()