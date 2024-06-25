import requests
import json
import os
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore

init(autoreset=True)

# --- init ---
repo_url = input(f"{Fore.BLUE}?{Fore.RESET} 指定仓库的链接为: ")
# 去除协议部分
if repo_url.startswith('https://'):
    url = repo_url[len('https://'):]
elif repo_url.startswith('http://'):
    url = repo_url[len('http://'):]

# 检查是否是GitHub地址
if not url.startswith('github.com/'):
    raise ValueError(f"{Fore.RED}✕{Fore.RESET} 无效的链接")

# 去除主机名部分
url = url[len('github.com/'):]

# 拆分所有者和仓库名
parts = url.split('/')
if len(parts) >= 2:
    owner = parts[0]
    repo = parts[1]
else:
    raise ValueError(f"{Fore.RED}✕{Fore.RESET} 无效的GitHub链接")
# ---
print("请选择保存到的文件夹:", end=" ")

root = tk.Tk()
root.withdraw()

output_dir = filedialog.askdirectory()

print(f"\r{Fore.GREEN}✓{Fore.RESET} 已选择保存到的文件夹: {Fore.BLUE}{output_dir}{Fore.RESET}")
output = os.path.join(output_dir, "labels.json")
output = os.path.normpath(output)
# ------------

# GitHub API URL
url = f'https://api.github.com/repos/{owner}/{repo}/labels'

# 发送请求获取所有labels
response = requests.get(url)

# 检查响应状态码
if response.status_code == 200:
    labels = response.json()
    
    # 提取需要的信息
    label_info = []
    for label in labels:
        label_data = {
            'name': label['name'],
            'description': label.get('description', ''),
            'color': label['color']
        }
        label_info.append(label_data)
    
    # 将信息写入JSON文件
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(label_info, f, ensure_ascii=False, indent=4)
    
    print(f"{Fore.GREEN}✓{Fore.RESET} 标签信息已写入 {Fore.BLUE}{output}{Fore.BLUE}")
else:
    print(f"{Fore.RED}✕{Fore.RESET} 无法获取标签，状态码: {Fore.YELLOW}{response.status_code}{Fore.RESET}")
