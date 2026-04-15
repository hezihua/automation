# ==============================================================================
# 注意：本脚本包含 jieba 分词与 snownlp 情感分析的实现代码。
# 运行本脚本前，需要安装相应的依赖（本环境未安装，仅提供代码实现）：
# pip install jieba snownlp
# ==============================================================================

def sentiment_analysis_demo():
    """
    演示基于 jieba 分词和 snownlp 的情感色彩单词数量统计
    """
    try:
        import jieba
        import jieba.posseg as psg
        from snownlp import SnowNLP
    except ImportError:
        print("未安装 jieba 或 snownlp 库。请执行: pip install jieba snownlp")
        return

    # 待分析的商品评论文本
    words1 = "速度快，包装好，看着特别好，喝着肯定不错！价廉物美"
    print(f"原始文本: {words1}\n")

    # --------------------------------------------------------------------------
    # 1. 基础分词
    # --------------------------------------------------------------------------
    words2 = jieba.cut(words1)
    words3 = list(words2)
    print("1. 基础分词结果:")
    print("/".join(words3))
    print("-" * 50)

    # --------------------------------------------------------------------------
    # 2. 优化分词结果 (移除标点符号、停用词)
    # --------------------------------------------------------------------------
    # 方法A: 使用停用词列表过滤
    stop_words = ["，", "！"]
    words4 = [x for x in words3 if x not in stop_words]
    print("2A. 过滤停用词后的结果:")
    print(words4)
    
    # 方法B: 基于词性过滤 (提取特定词性的词，如形容词 'a')
    # psg.cut 会返回 (word, flag) 的元组，flag 代表词性
    words5_raw = [(w.word, w.flag) for w in psg.cut(words1)]
    saved_flags = ['a'] # 保留形容词
    words5 = [x for x in words5_raw if x[1] in saved_flags]
    print("\n2B. 基于词性过滤(仅保留形容词)的结果:")
    print(words5)
    print("-" * 50)

    # --------------------------------------------------------------------------
    # 3. 语义情感分析 (基于 snownlp)
    # --------------------------------------------------------------------------
    # 提取出过滤后的纯词语列表
    words6 = [x[0] for x in words5]
    
    # 3A. 对整句话进行情感分析
    # 注意：为了避免 snownlp 对否定词切分不准，通常将 jieba 分好的词用空格拼接后再传给 snownlp
    s1 = SnowNLP(" ".join(words3))
    print("3A. 整句情感倾向得分 (越接近1越正向，越接近0越负向):")
    print(s1.sentiments)
    
    # 3B. 对提取出的关键词(形容词)逐个进行情感色彩统计
    print("\n3B. 关键词情感色彩统计:")
    positive = 0
    negtive = 0
    for word in words6:
        s2 = SnowNLP(word)
        # 设定阈值，大于0.7认为是正向评价
        if s2.sentiments > 0.7:
            positive += 1
        else:
            negtive += 1
        print(f"  词语: '{word}', 情感得分: {s2.sentiments:.4f}")
        
    print(f"\n统计结果 -> 正向评价数量: {positive}, 负向评价数量: {negtive}")
    print("=" * 50)


def count_word_types(text):
    """
    思考题解答：统计一段文字中包含了多少个动词、多少个名词和多少个形容词
    """
    try:
        import jieba.posseg as psg
    except ImportError:
        return

    print("\n--- 思考题解答：统计词性数量 ---")
    print(f"分析文本: {text}")
    
    # 使用 jieba.posseg 进行词性标注分词
    words = psg.cut(text)
    
    # 初始化计数器
    verb_count = 0      # 动词 (v)
    noun_count = 0      # 名词 (n)
    adj_count = 0       # 形容词 (a)
    
    # 记录具体的词，方便查看
    verbs, nouns, adjs = [], [], []
    
    for w in words:
        # 判断词性标志 (flag)
        if w.flag.startswith('v'): # 动词 (包括 v, vn, vd 等)
            verb_count += 1
            verbs.append(w.word)
        elif w.flag.startswith('n'): # 名词 (包括 n, nr, ns 等)
            noun_count += 1
            nouns.append(w.word)
        elif w.flag.startswith('a'): # 形容词 (包括 a, ad, an 等)
            adj_count += 1
            adjs.append(w.word)
            
    print(f"动词数量: {verb_count} -> {verbs}")
    print(f"名词数量: {noun_count} -> {nouns}")
    print(f"形容词数量: {adj_count} -> {adjs}")


if __name__ == "__main__":
    # 执行课程示例代码
    sentiment_analysis_demo()
    
    # 执行思考题代码
    test_text = "我非常喜欢这款手机，它的屏幕很大，运行速度也特别快，真的是物超所值！"
    count_word_types(test_text)
