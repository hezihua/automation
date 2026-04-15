import os
import requests
import json
import time
from pyecharts.charts import Map
from pyecharts import options as opts

def fetch_data():
    """
    尝试从接口获取疫情数据。
    注意：由于原课程中的腾讯疫情接口可能已下线或结构变更，
    这里加入了异常处理。如果获取失败，将使用模拟数据。
    """
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if 'data' in data:
            alldata = json.loads(data['data'])
            return alldata
    except Exception as e:
        print(f"获取实时数据失败: {e}，将使用模拟数据生成图表。")
    
    # 模拟数据 (Mock Data)
    return {
        'lastUpdateTime': time.strftime('%Y-%m-%d %H:%M:%S'),
        'areaTree': [{
            'children': [
                {'name': '湖北', 'total': {'nowConfirm': 120}},
                {'name': '广东', 'total': {'nowConfirm': 55}},
                {'name': '北京', 'total': {'nowConfirm': 800}},
                {'name': '上海', 'total': {'nowConfirm': 1500}},
                {'name': '浙江', 'total': {'nowConfirm': 12000}},
                {'name': '四川', 'total': {'nowConfirm': 8}},
                {'name': '河南', 'total': {'nowConfirm': 300}},
                {'name': '江苏', 'total': {'nowConfirm': 600}},
                {'name': '山东', 'total': {'nowConfirm': 45}},
                {'name': '湖南', 'total': {'nowConfirm': 0}}
            ]
        }]
    }

def generate_map_chart(output_html="covid19_map.html"):
    """
    使用 pyecharts 绘制全国疫情分布动态地图
    """
    # 1. 思考题解答：如何自动删除上一个生成的文件？
    # 其实 pyecharts 的 render() 方法默认会覆盖同名文件。
    # 但如果需要显式删除，可以使用 os.remove()：
    if os.path.exists(output_html):
        print(f"发现旧的图表文件 {output_html}，正在删除...")
        os.remove(output_html)

    alldata = fetch_data()

    chinadata = []
    for province in alldata['areaTree'][0]['children']:
        provincedata = (
            province['name'],
            province['total']['nowConfirm']
        )
        chinadata.append(provincedata)

    # 实例化 Map 类
    map_chart = Map()
    
    # 添加数据
    map_chart.add(
        series_name="全国确诊病例分布图",
        data_pair=tuple(chinadata),
        maptype="china",
        is_map_symbol_show=False
    )

    # 设置全局样式
    map_chart.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"全国疫情地图( {alldata['lastUpdateTime']} )"
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_piecewise=True,
            pieces=[
                {"min": 1, "max": 9, "label": "1-9人", "color": "#FFE6BE"},
                {"min": 10, "max": 99, "label": "10-99人", "color": "#FFB769"},
                {"min": 100, "max": 499, "label": "100-499人", "color": "#FF8F66"},
                {"min": 500, "max": 999, "label": "500-999人", "color": "#ED514E"},
                {"min": 1000, "max": 9999, "label": "1000-9999人", "color": "#CA0D11"},
                {"min": 10000, "max": 100000, "label": "10000人以上", "color": "#A52A2A"}
            ]
        )
    )

    # 渲染生成 HTML 文件
    map_chart.render(output_html)
    print(f"动态图表已生成并保存至: {output_html}")
    
    # 2. 思考题解答：有没有办法让网页自动更新呢？
    # 方案：可以在生成的 HTML 文件的 <head> 标签中注入一段自动刷新的 meta 标签或 JS 代码。
    # 下面演示如何通过修改生成的 HTML 文件来实现每隔 60 秒自动刷新：
    with open(output_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # 在 <head> 标签后插入自动刷新的 meta 标签
    refresh_tag = '<meta http-equiv="refresh" content="60">\n'
    if '<head>' in html_content and refresh_tag not in html_content:
        html_content = html_content.replace('<head>', f'<head>\n    {refresh_tag}')
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("已为生成的网页添加自动刷新功能（每60秒刷新一次）。")

if __name__ == "__main__":
    generate_map_chart()
