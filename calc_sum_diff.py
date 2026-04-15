import argparse

def calc(num1, num2):
    """计算两个整数的和与差"""
    print(f"输入的两个整数为: {num1} 和 {num2}")
    print(f"它们的和: {num1} + {num2} = {num1 + num2}")
    print(f"它们的差: {num1} - {num2} = {num1 - num2}")

def args_opt():
    """获取命令行参数函数"""
    parser = argparse.ArgumentParser(description="计算两个整数的和与差")
    
    # 增加参数选项，并指定类型为 int
    parser.add_argument("-a", "--num1", type=int, required=True, help="第一个整数")
    parser.add_argument("-b", "--num2", type=int, required=True, help="第二个整数")
    
    return parser.parse_args()

if __name__ == "__main__":
    # 解析命令行参数
    args = args_opt()
    
    # 调用计算函数
    calc(args.num1, args.num2)
