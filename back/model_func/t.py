import os

# 获取上一级目录作为项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(project_root)
# 定义model和data的路径
model_path = os.path.join(project_root, 'model', 'shoes')
data_path = os.path.join(project_root, 'data')

# 检查model路径是否存在
if os.path.exists(model_path) and os.path.isdir(model_path):
    print(f"Model path '{model_path}' is available.")
else:
    print(f"Model path '{model_path}' is NOT available.")

# 检查data路径是否存在
if os.path.exists(data_path) and os.path.isdir(data_path):
    print(f"Data path '{data_path}' is available.")
else:
    print(f"Data path '{data_path}' is NOT available.")

with open(r"F:\BS\code\back\data\shoes\..\..\uploads\description_8652df7b754c486eb03d4d48e12d1f68.txt", 'r') as file:
            caption = file.read()  # 读取文件的全部内容
print(caption)