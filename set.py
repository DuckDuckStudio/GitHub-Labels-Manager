import json
import sys
import requests
from tkinter import filedialog
from colorama import init, Fore

init(autoreset=True)

# --- 读取配置文件 ---
with open('config.json', 'r') as file:
    data = json.load(file)
token = data.get('token')

json_file = filedialog.askopenfilename(filetypes=[
    ("标签数据json文件", "*.json"),
    ("All files", "*.*")
])
if not json_file:
    print(f"{Fore.RED}✕{Fore.RESET} 未选择标签数据json文件")
# -------------------

# --- init ---
repo_url = input(f"{Fore.BLUE}?{Fore.RESET} 目标仓库的链接为: ")
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

# GitHub API URL
url = f'https://api.github.com/repos/{owner}/{repo}/labels'

# 请求头
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# 从JSON文件读取标签信息
with open(json_file, 'r', encoding='utf-8') as f:
    labels = json.load(f)

# 遍历标签和发送请求创建或更新标签
for label in labels:
    payload = {
        'name': label['name'],
        'description': label['description'],
        'color': label['color']
    }

    # 尝试创建标签
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print(f"{Fore.GREEN}✓{Fore.RESET} 成功添加 {Fore.BLUE}{label['name']}{Fore.RESET} 标签")
    elif response.status_code == 422 and 'already_exists' in response.json().get('errors', [{}])[0].get('message', ''):
        print(f"{Fore.YELLOW}⚠{Fore.RESET} 标签 {Fore.BLUE}{label['name']}{Fore.RESET} 已经存在！是否使用json中的数据覆盖?")
        t = input("[Y]是 [N]否: ").lower()
        if t in ["y", "yes", "是", "更新", "覆盖"]:
            # 如果标签已存在，尝试更新标签
            update_url = f"{url}/{label['name']}"
            response = requests.patch(update_url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f"{Fore.GREEN}✓{Fore.RESET} 成功更新标签 {Fore.BLUE}{label['name']}{Fore.RESET}")
            else:
                print(f"{Fore.RED}✕{Fore.RESET} 更新标签 {Fore.BLUE}{label['name']}{Fore.RESET} 失败: {Fore.YELLOW}{response.status_code}{Fore.RESET}\n{Fore.RED}{response.text}{Fore.RESET}")
    else:
        print(f"{Fore.RED}✕{Fore.RESET} 创建标签 {Fore.BLUE}{label['name']}{Fore.RESET} 失败: {Fore.YELLOW}{response.status_code}{Fore.RESET}\n{Fore.RED}{response.text}{Fore.RESET}")

input(f"{Fore.BLUE}[!]{Fore.RESET} 按 {Fore.BLUE}Enter{Fore.RESET} 键退出...")
