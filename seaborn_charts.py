import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_iris_scatter():
    """
    使用 seaborn 绘制鸢尾花(iris)数据集的散点图矩阵 (pairplot)。
    展示如何使用 seaborn 生成统一风格的图表。
    """
    print("正在加载鸢尾花数据集并绘制散点图矩阵...")
    # 设置背景风格
    sns.set(style="darkgrid", color_codes=True)
    
    # 解决 matplotlib 在部分系统中中文显示乱码的问题
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    # 加载 seaborn 内置的鸢尾花数据集
    # 注意：如果网络问题导致加载失败，可以提前下载 iris.csv 并使用 pd.read_csv() 读取
    try:
        iris = sns.load_dataset('iris')
    except Exception as e:
        print(f"在线加载数据集失败: {e}，尝试使用本地模拟数据。")
        # 生成模拟的鸢尾花数据用于演示
        np.random.seed(0)
        iris = pd.DataFrame({
            'sepal_length': np.random.normal(5.8, 0.8, 150),
            'sepal_width': np.random.normal(3.0, 0.4, 150),
            'petal_length': np.random.normal(3.7, 1.7, 150),
            'petal_width': np.random.normal(1.2, 0.7, 150),
            'species': ['setosa']*50 + ['versicolor']*50 + ['virginica']*50
        })

    # 加载数据，使用散点图，设置点的颜色和样式
    # kind='scatter' (散点图), diag_kind='hist' (对角线为直方图)
    # hue='species' (按照品种进行分类着色)
    g = sns.pairplot(
        iris,
        kind='scatter',
        diag_kind='hist',
        hue='species',
        palette='husl',
        markers=['o', 's', 'D'],
        height=2
    )
    
    g.fig.suptitle("鸢尾花数据集特征分布散点图矩阵", y=1.02)
    
    # 保存图表到本地
    output_file = "iris_pairplot.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"图表已保存至: {output_file}")
    
    # 显示图表
    # plt.show() # 在无 GUI 环境下可能会阻塞，这里默认注释掉，用户可自行放开

def plot_house_price_trend():
    """
    思考题解答：展示当前地区的房价走势。
    走势图最适合使用折线图 (lineplot)。
    """
    print("\n正在绘制房价走势折线图(思考题解答)...")
    sns.set(style="whitegrid")
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 构造模拟的房价走势数据
    months = [f"2023-{str(i).zfill(2)}" for i in range(1, 13)]
    prices = [50000, 50500, 51200, 51000, 50800, 51500, 52000, 52500, 52300, 53000, 53500, 54000]
    
    df = pd.DataFrame({
        '月份': months,
        '均价(元/平米)': prices
    })
    
    plt.figure(figsize=(10, 6))
    
    # 绘制折线图
    ax = sns.lineplot(
        x='月份', 
        y='均价(元/平米)', 
        data=df, 
        marker='o', 
        linewidth=2, 
        color='b'
    )
    
    plt.title("2023年某地区房价走势图", fontsize=16)
    plt.xlabel("月份", fontsize=12)
    plt.ylabel("均价(元/平米)", fontsize=12)
    plt.xticks(rotation=45) # 旋转X轴标签，防止重叠
    
    # 保存图表到本地
    output_file = "house_price_trend.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"图表已保存至: {output_file}")
    
    # plt.show()

if __name__ == "__main__":
    # 1. 运行课程中的鸢尾花散点图示例
    plot_iris_scatter()
    
    # 2. 运行思考题的房价走势折线图示例
    plot_house_price_trend()
