# 模拟代码仓库存活周期
import datetime

def code_legacy(years):
    today = datetime.date.today()
    legacy_date = today + datetime.timedelta(days=years*365)
    print(f"▲ 你的代码将在{legacy_date.year}年帮助{years*10}个开发者")
    print(f"★ 需完成至少{years*20}个优质仓库")

code_legacy(5)
# 输出：▲ 你的代码将在2028年帮助50个开发者
#      ★ 需完成至少100个优质仓库
