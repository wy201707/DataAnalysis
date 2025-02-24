# 用代码实现错题自动分类（示例）
def mistake_analyzer(issue, emotion_level):
    patterns = {
        '人际关系': ['争吵','误解','拉黑'],
        '时间黑洞': ['闲鱼','小红书','刷手机'],
        '决策失误': ['冲动购物','反复比价','沉没成本','误判'],
        '情绪失控': ['生气','后悔','焦虑']
    }
    for category, keywords in patterns.items():
        if any(kw in issue for kw in keywords):
            return f"{category} | 情绪强度{emotion_level}/10"
    return "其他"

print(mistake_analyzer("和闲鱼卖家争吵", 8))
# 输出：人际关系 | 情绪强度8/10


