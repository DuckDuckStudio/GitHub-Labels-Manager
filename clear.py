import json
import requests
from colorama import init, Fore

init(autoreset=True)

flag = 0

# --- 读取配置文件 ---
with open('config.json', 'r') as file:
    data = json.load(file)
token = data.get('token')
# -------------------

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

# GitHub API URL
url = f'https://api.github.com/repos/{owner}/{repo}/labels'

# 请求头
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# 获取目标仓库的所有标签
response = requests.get(url, headers=headers)
labels = response.json()

# 删除每个标签
for label in labels:
    delete_url = f"{url}/{label['name']}"
    response = requests.delete(delete_url, headers=headers)
    
    if response.status_code == 204:
        print(f"{Fore.GREEN}✓{Fore.RESET} 标签 {Fore.BLUE}{label['name']}{Fore.RESET} 成功删除")
    else:
        print(f"{Fore.RED}✕{Fore.RESET} 删除标签 {Fore.BLUE}{label['name']}{Fore.RESET} 时失败: {Fore.YELLOW}{response.status_code}{Fore.RESET}\n{Fore.RED}{response.text}{Fore.RESET}")
        flag += 1

if flag:
    print(f"{Fore.YELLOW}⚠{Fore.RESET} 操作完成，共出现 {Fore.YELLOW}{flag}{Fore.RESET} 个失败项。")
else:
    print(f"{Fore.GREEN}✓{Fore.RESET} 成功清除所有标签！")
