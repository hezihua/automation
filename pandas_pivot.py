import pandas as pd
import numpy as np
import os

def create_mock_data():
    """
    创建模拟数据，用于演示数据透视表。
    这里我们模拟课程思考题中的场景：一个学校有多个班级，每个班级有多个学生，
    每个学生有语文、数学、外语三门成绩。
    """
    np.random.seed(42)
    
    classes = [f"{i}班" for i in range(1, 4)] # 模拟3个班级
    subjects = ["语文", "数学", "外语"]
    
    data = []
    student_id = 1
    for cls in classes:
        for _ in range(5): # 每个班级模拟5个学生
            student_name = f"学生{student_id}"
            for subject in subjects:
                # 随机生成成绩 60-100
                score = np.random.randint(60, 101)
                data.append({
                    "班级": cls,
                    "姓名": student_name,
                    "科目": subject,
                    "成绩": score
                })
            student_id += 1
            
    df = pd.DataFrame(data)
    return df

def generate_pivot_tables(df, output_excel):
    """
    使用 Pandas 的 pivot_table 函数生成不同的数据透视表，
    并保存到 Excel 文件的不同 Sheet 中。
    """
    print("原始数据前5行：")
    print(df.head())
    print("-" * 50)
    
    # 创建一个 Excel 写入器
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        # 1. 写入原始数据
        df.to_excel(writer, sheet_name="原始数据", index=False)
        
        # 2. 透视表 1：分析每个班级各科的平均成绩
        # index: 行索引 (班级)
        # columns: 列索引 (科目)
        # values: 要计算的值 (成绩)
        # aggfunc: 聚合函数，默认是 'mean' (平均值)
        pivot1 = pd.pivot_table(
            df, 
            index="班级", 
            columns="科目", 
            values="成绩", 
            aggfunc="mean"
        )
        # 将结果保留两位小数
        pivot1 = pivot1.round(2)
        print("透视表 1：每个班级各科的平均成绩")
        print(pivot1)
        print("-" * 50)
        pivot1.to_excel(writer, sheet_name="班级各科平均分")
        
        # 3. 透视表 2：分析每个学生的总分和平均分
        # 可以向 aggfunc 传入多个函数列表
        pivot2 = pd.pivot_table(
            df,
            index=["班级", "姓名"], # 多级索引
            values="成绩",
            aggfunc=["sum", "mean"]
        )
        pivot2 = pivot2.round(2)
        # 重命名列名使其更易读
        pivot2.columns = ['总分', '平均分']
        print("透视表 2：每个学生的总分和平均分")
        print(pivot2)
        print("-" * 50)
        pivot2.to_excel(writer, sheet_name="学生成绩汇总")
        
        # 4. 透视表 3：带有汇总行/列的透视表 (margins=True)
        # 统计每个班级的最高分，并显示所有班级的全局最高分
        pivot3 = pd.pivot_table(
            df,
            index="班级",
            columns="科目",
            values="成绩",
            aggfunc="max",
            margins=True,          # 开启汇总
            margins_name="全局最高分" # 汇总行/列的名称
        )
        print("透视表 3：每个班级各科最高分及全局最高分")
        print(pivot3)
        print("-" * 50)
        pivot3.to_excel(writer, sheet_name="班级最高分统计")

if __name__ == "__main__":
    # 输出的 Excel 文件名
    OUTPUT_FILE = "student_scores_pivot.xlsx"
    
    # 如果文件已存在，先删除
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        
    print("正在生成模拟数据...")
    df = create_mock_data()
    
    print(f"正在生成数据透视表并保存至 {OUTPUT_FILE} ...\n")
    generate_pivot_tables(df, OUTPUT_FILE)
    
    print(f"处理完成！请打开 {OUTPUT_FILE} 查看结果。")
