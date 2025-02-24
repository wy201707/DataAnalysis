
# 自动生成技术向爆款标题
import random

tech_keywords = ['程序员重生计划', '代码遗产', '硅谷永生算法']
pain_points = ['刷手机', '焦虑', '拖延']

title = f"{random.choice(tech_keywords)}:\
我是如何用{random.choice(['Python','AI'])}\
戒掉{random.choice(pain_points)}的"
print(title)
# 示例输出：代码遗产：我是如何用Python戒掉刷手机的