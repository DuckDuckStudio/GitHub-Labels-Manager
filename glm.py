import os
import sys
import json
import argparse
import requests
import webbrowser
from tkinter import filedialog
from colorama import init, Fore

init(autoreset=True)

version = "1.1"
script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
config_path = os.path.join(script_path, "config.json")

# -----------------------------------------------------------------------------------------------------

def read_token():
    try:
        with open(config_path, 'r') as file:
            data = json.load(file)
            token = data.get('token')
            if not token.startswith('ghp_'):
                print(f"{Fore.YELLOW}⚠{Fore.RESET} 请确认Token是否正确")
                try:
                    input(f"按{Fore.BLUE}Enter{Fore.RESET}键确认，按{Fore.BLUE}Ctrl + C{Fore.RESET}键取消...")
                except KeyboardInterrupt:
                    print(f"{Fore.BLUE}[!]{Fore.RESET} 已取消操作")
                    return "token error"
            return token
    except Exception as e:
        print(f"{Fore.RED}✕{Fore.RESET} 读取配置文件时出错")
        return "error"

def set_token(token):
    try:
        # --- Token 检查 ---
        if not token.startswith('ghp_'):
            print(f"{Fore.YELLOW}⚠{Fore.RESET} 请确认Token是否正确")
            try:
                input(f"按{Fore.BLUE}Enter{Fore.RESET}键确认，按{Fore.BLUE}Ctrl + C{Fore.RESET}键取消...")
            except KeyboardInterrupt:
                print(f"{Fore.BLUE}[!]{Fore.RESET} 已取消操作")
                return "error"
        # -----------------

        # 读取现有的 JSON 文件
        with open(config_path, 'r') as file:
            data = json.load(file)
        
        # 更新 token 字段
        data['token'] = token
        
        # 将更新后的 JSON 写回文件
        with open(config_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"{Fore.GREEN}✓{Fore.RESET} 成功更新Token")
        return "successful"
    except Exception as e:
        print(f"{Fore.RED}✕{Fore.RESET} 处理配置文件时出错:\n{Fore.RED}{e}{Fore.RESET}\n")
        return "error"

def formatting_url(url):
    # 本函数有以下行为:
    # 正常返回仓库所有者与仓库名，错误时输出原因并返回url error

    # 去除协议部分
    if url.startswith('https://'):
        url = url[len('https://'):]
    elif url.startswith('http://'):
        url = url[len('http://'):]
    # 检查是否是GitHub地址并去除主机名部分
    if url.startswith('github.com/'):
        url = url[len('github.com/'):]
    elif url.startswith('www.github.com/'):
        url = url[len('www.github.com/'):]
    else:
        print(f"{Fore.RED}✕{Fore.RESET} 仓库链接{Fore.YELLOW}似乎不是GitHub上的{Fore.RESET}，请确保你的仓库链接正确")
        return "url error"
    # 拆分所有者和仓库名
    parts = url.split('/')
    if len(parts) >= 2:
        owner = parts[0]
        repo = parts[1]
        return owner, repo
        # 先返回 所有者 再返回 仓库名
    else:
        print(f"{Fore.RED}✕{Fore.RESET} 仓库链接{Fore.YELLOW}无效{Fore.RESET}，请确保你的仓库链接正确\n{Fore.BLUE}[!]{Fore.RESET} 建议检查链接是否过度，例如以下情况:\n{Fore.GREEN}正确:{Fore.RESET} https://github.com/example/example-repo/\n{Fore.RED}错误{Fore.RESET} https://github.com/example/example-repo/labels/")
        return "url error"

def get_labels(owner, repo, save):
    # 本函数有以下行为
    # 正常操作保存标签，并返回successful，错误时输出错误原因并返回具体错误信息
    # 可能返回如下错误
    # cancel 操作取消 | get error 获取时出错

    # 获取标签

    if save:
        output = save
    else:
        print("请选择保存位置:", end=" ")

        output = filedialog.asksaveasfilename(filetypes=[
            ("标签数据json文件", "*.json")
        ])

    if not output:
        print(f"{Fore.RED}✕{Fore.RESET} 未选择保存位置")
        return "cancel"# 返回取消状态

    if not output.endswith(".json"):
        output += ".json"
    
    if os.path.exists(output):
        print(f"{Fore.RED}✕{Fore.RESET} 保存位置已被占用！")
        return "cancel"# 返回取消状态

    print(f"\r{Fore.GREEN}✓{Fore.RESET} 已选择保存位置: {Fore.BLUE}{output}{Fore.RESET}")
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
        print(f"{Fore.RED}✕{Fore.RESET} 无法获取标签，返回的状态码不为200: {Fore.YELLOW}{response.status_code}{Fore.RESET}")
        return "get error"# 返回获取错误

# ---------------------------------------------------------------------------
def clear_labels(owner, repo, token):
    # 本函数有以下行为
    # 正常操作清空指定仓库标签，并返回successful，错误时输出错误原因并返回具体错误信息
    # 可能返回如下错误
    # cancel 操作取消 | get error 获取时出错

    flag = 0

    # 确认
    print(f"{Fore.BLUE}?{Fore.RESET} 确认删除?\n{Fore.YELLOW}⚠{Fore.RESET} 此操作将清空指定仓库的{Fore.YELLOW}所有{Fore.RESET}标签，不可撤销!")
    if not (input("[Y]确认 [N]取消 : ").lower() in ["y", "yes", "确认"]):
        print(f"{Fore.BLUE}[!]{Fore.RESET} 已取消操作")
        return "cancel"

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
            print(f"{Fore.BLUE}?{Fore.RESET} 是否继续?")
            try:
                input(f"按{Fore.BLUE}Enter{Fore.RESET}键确认，按{Fore.BLUE}Ctrl + C{Fore.RESET}键取消...")
            except KeyboardInterrupt:
                print(f"{Fore.BLUE}[!]{Fore.RESET} 已取消操作")
                return "cancel"

    if flag:
        print(f"{Fore.YELLOW}⚠{Fore.RESET} 操作完成，共出现 {Fore.YELLOW}{flag}{Fore.RESET} 个失败项。")
    else:
        print(f"{Fore.GREEN}✓{Fore.RESET} 成功清除所有标签！")
    return "successful"# 即使有 flag 也返回 successful

# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='GitHub Labels Manager (GLM), 自动帮你复制仓库标签、获取仓库标签、清空已有标签的工具')
    subparsers = parser.add_subparsers(dest='command', required=True, help='可用命令')

    # 命令：get
    parser_get = subparsers.add_parser('get', help='获取标签')
    parser_get.add_argument('repo_url', type=str, help='GitHub仓库URL')
    parser_get.add_argument('--save', type=str, help='标签信息保存的位置')

    # 命令：set
    parser_set = subparsers.add_parser('set', help='设置标签')
    parser_set.add_argument('repo_url', type=str, help='GitHub仓库URL')
    parser_set.add_argument('--token', type=str, help='GitHub访问令牌')

    # 命令：config
    parser_config = subparsers.add_parser('config', help='修改配置')
    parser_config.add_argument('--token', type=str, help='设置GitHub访问令牌')
    parser.add_argument('--edit', help='打开配置文件', action='store_true')

    # 命令：clear
    parser_clear = subparsers.add_parser('clear', help='清空标签')
    parser_clear.add_argument('repo_url', type=str, help='GitHub仓库URL')
    parser_clear.add_argument('--token', type=str, help='GitHub访问令牌')

    args = parser.parse_args()

    if args.command == 'get':
        # 获取功能的实现
        running_result = formatting_url(args.repo_url)
        if running_result == "url error":
            return 1
        running_result = get_labels(running_result[0], running_result[1], args.save)
        if running_result in ["cancel", "get error"]:
            return 1
    #elif args.command == 'set':
    #    # 设置功能的实现
    #    running_result = formatting_url(args.repo_url)
    #    if running_result == "url error":
    #        return 1
    #    running_result = 
    elif args.command == 'config':
        # 配置功能的实现
        if args.token:
            running_result = set_token(args.token)
            if running_result == "error":
                return 1
        elif args.edit:
            # 仅使用一次且较短，不设置函数
            try:
                webbrowser.open(config_path)
                print(f"{Fore.GREEN}✓{Fore.RESET} 已打开配置文件")
            except Exception as e:
                print(f"{Fore.RED}✕{Fore.RESET} 无法打开配置文件: {Fore.RED}{e}{Fore.RESET}\n{Fore.BLUE}[!]{Fore.RESET} 请确认配置文件路径正确: {Fore.BLUE}{config_path}{Fore.RESET}")
        else:
            print(f"{Fore.RED}✕{Fore.RESET} 缺少配置项")
            return 1
    elif args.command == 'clear':
        # 清除功能的实现
        running_result = formatting_url(args.repo_url)
        if running_result == "url error":
            return 1
        if args.token:
            token = args.token
        else:
            token = read_token()
            if token in ["error", "token error"]:
                return 1
        running_result = clear_labels(running_result[0], running_result[1], token)
        if running_result in ["cancel"]:
            return 1
    else:
        print(f"{Fore.RED}✕{Fore.RESET} 不支持的命令")
        return 1
    return 0

if __name__ == '__main__':
    result = main()
    input(f"{Fore.BLUE}[!]{Fore.RESET} 按 {Fore.BLUE}Enter{Fore.RESET} 键退出...")
    sys.exit(result)
