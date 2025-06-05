import re

# 定义文件路径
file_path = '/www/server/panel/data/plugin.json'

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 执行第一个替换操作，将 "endtime": -1 替换为 "endtime": 999999999999
content = re.sub(r'"endtime": -1', r'"endtime": 999999999999', content)

# 执行第二个替换操作，将 "ltd": -1, "pro": -1, "recommend" 替换为 "ltd": 0, "pro": 0, "recommend"
content = re.sub(r'"ltd": -1, "pro": -1, "recommend"', r'"ltd": 0, "pro": 0, "recommend"', content)

# 将替换后的内容写回文件
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

print("替换完成")
