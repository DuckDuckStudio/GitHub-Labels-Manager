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
                print(f"{Fore.YELLOW}⚠{Fore.RESET} Please check whether the Token is correct.")
                try:
                    input(f"Press {Fore.BLUE}Enter{Fore.RESET} to confirm, press {Fore.BLUE}Ctrl + C{Fore.RESET} to cancel...")
                except KeyboardInterrupt:
                    print(f"{Fore.BLUE}[!]{Fore.RESET} Cancelled operation.")
                    return "token error"
            return token
    except Exception as e:
        print(f"{Fore.RED}✕{Fore.RESET} Error reading configuration file.")
        return "error"

def set_token(token):
    try:
        # --- Token 检查 ---
        if not token.startswith('ghp_'):
            print(f"{Fore.YELLOW}⚠{Fore.RESET} Please check whether the Token is correct.")
            try:
                input(f"Press {Fore.BLUE}Enter{Fore.RESET} to confirm, press {Fore.BLUE}Ctrl + C{Fore.RESET} to cancel...")
            except KeyboardInterrupt:
                print(f"{Fore.BLUE}[!]{Fore.RESET} Cancelled operation.")
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
        print(f"{Fore.GREEN}✓{Fore.RESET} Successfully update Token.")
        return "successful"
    except Exception as e:
        print(f"{Fore.RED}✕{Fore.RESET} An error occurred processing the configuration file:\n{Fore.RED}{e}{Fore.RESET}\n")
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
        print(f"{Fore.RED}✕{Fore.RESET} The repo link {Fore.YELLOW}does not appear to be on GitHub{Fore.RESET}, please make sure your repo link is correct.")
        return "url error"
    # 拆分所有者和仓库名
    parts = url.split('/')
    if len(parts) >= 2:
        owner = parts[0]
        repo = parts[1]
        return owner, repo
        # 先返回 所有者 再返回 仓库名
    else:
        print(f"{Fore.RED}✕{Fore.RESET} The repo link is {Fore.YELLOW}invalid{Fore.RESET}, please make sure your repo link is correct.\n{Fore.BLUE}[!]{Fore.RESET} The repo link should like the following:\n{Fore.GREEN}Correct:{Fore.RESET} https://github.com/example/example-repo/\n{Fore.RED}Error:{Fore.RESET} https://github.com/example/example-repo/labels/")
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
        print("Please select a save location:", end=" ")

        output = filedialog.asksaveasfilename(filetypes=[
            ("Label data json file", "*.json")
        ])

    if not output:
        print(f"{Fore.RED}✕{Fore.RESET} No save location is selected.")
        return "cancel"# 返回取消状态

    if not output.endswith(".json"):
        output += ".json"
    
    if os.path.exists(output):
        print(f"{Fore.RED}✕{Fore.RESET} The save location is occupied!")
        return "cancel"# 返回取消状态

    print(f"\r{Fore.GREEN}✓{Fore.RESET} The save location has been selected: {Fore.BLUE}{output}{Fore.RESET}")
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
        
        print(f"{Fore.GREEN}✓{Fore.RESET} Label information has been written to {Fore.BLUE}{output}{Fore.BLUE}")
    else:
        print(f"{Fore.RED}✕{Fore.RESET} Unable to get labels，The status code returned by the remote server is not 200: {Fore.YELLOW}{response.status_code}{Fore.RESET}")
        return "get error"# 返回获取错误

# ---------------------------------------------------------------------------
def clear_labels(owner, repo, token):
    # 本函数有以下行为
    # 正常操作清空指定仓库标签，并返回successful，错误时输出错误原因并返回具体错误信息
    # 可能返回如下错误
    # cancel 操作取消 | get error 获取时出错

    flag = 0

    # 确认
    print(f"{Fore.BLUE}?{Fore.RESET} Confirm deletion?\n{Fore.YELLOW}⚠{Fore.RESET} This operation will empty {Fore.YELLOW}all{Fore.RESET} labels, irrevocable!")
    if not (input("[Y] Confirm [N] Cancel:").lower() in ["y", "yes", "confirm"]):
        print(f"{Fore.BLUE}[!]{Fore.RESET} Cancelled operation.")
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
            print(f"{Fore.GREEN}✓{Fore.RESET} Label {Fore.BLUE}{label['name']}{Fore.RESET} deleted successfully")
        else:
            print(f"{Fore.RED}✕{Fore.RESET} Failed to delete label {Fore.BLUE}{label['name']}{Fore.RESET}: {Fore.YELLOW}{response.status_code}{Fore.RESET}\n{Fore.RED}{response.text}{Fore.RESET}")
            flag += 1
            print(f"{Fore.BLUE}?{Fore.RESET} Continue?")
            try:
                input(f"Press {Fore.BLUE}Enter{Fore.RESET} to confirm, press {Fore.BLUE}Ctrl + C{Fore.RESET} to cancel...")
            except KeyboardInterrupt:
                print(f"{Fore.BLUE}[!]{Fore.RESET} Cancelled operation.")
                return "cancel"

    if flag:
        print(f"{Fore.YELLOW}⚠{Fore.RESET} The operation is complete with {Fore.YELLOW}{flag}{Fore.RESET} failed items.")
    else:
        print(f"{Fore.GREEN}✓{Fore.RESET} Successfully cleared all labels!")
    return "successful"# 即使有 flag 也返回 successful

# ---------------------------------------------------------------------------

def set_labels(owner, repo, token, json_file=None):
    if not json_file:
        json_file = filedialog.askopenfilename(filetypes=[
            ("Label data json file", "*.json"),
            ("All files", "*.*")
        ])
        if not json_file:
            print(f"{Fore.RED}✕{Fore.RESET} No Label data json file is selected.")
            return "cancel"
    if not os.path.exists(json_file):
        print(f"{Fore.RED}✕{Fore.RESET} The selected label data json file does {Fore.YELLOW}not exist{Fore.RESET}!")
        return "cancel"
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
            print(f"{Fore.GREEN}✓{Fore.RESET} The label {Fore.BLUE}{label['name']}{Fore.RESET} was added successfully.")
        elif response.status_code == 422 and 'already_exists' in response.json().get('errors', [{}])[0].get('message', ''):
            print(f"{Fore.YELLOW}⚠{Fore.RESET} The label {Fore.BLUE}{label['name']}{Fore.RESET} already exists! Do you want to use Label data Data of the json file overrides it?")
            t = input("[Y]Yes [N]No: ").lower()
            if t in ["y", "yes", "update", "overrides"]:
                # 如果标签已存在，尝试更新标签
                update_url = f"{url}/{label['name']}"
                response = requests.patch(update_url, headers=headers, json=payload)
                if response.status_code == 200:
                    print(f"{Fore.GREEN}✓{Fore.RESET} The label {Fore.BLUE}{label['name']}{Fore.RESET} was updated successfully.")
                else:
                    print(f"{Fore.RED}✕{Fore.RESET} Failed to update the label {Fore.BLUE}{label['name']}{Fore.RESET}: {Fore.YELLOW}{response.status_code}{Fore.RESET}\n{Fore.RED}{response.text}{Fore.RESET}")
                    return "update error"
        else:
            print(f"{Fore.RED}✕{Fore.RESET} Failed to create label {Fore.BLUE}{label['name']}{Fore.RESET}: {Fore.YELLOW}{response.status_code}{Fore.RESET}\n{Fore.RED}{response.text}{Fore.RESET}")
            return "error"
    return "successful"

# ---------------------------------------------------------------------------

def copy_labels(source_owner, source_repo, set_owner, set_repo, token, json_file=os.path.join(script_path, "labels-temp.json"), save=False):
    # 调用get与set函数复制仓库标签
    # 传入先所有者，再仓库名
    # 先源仓库，再目标仓库，token，json_file，save
    if get_labels(source_owner, source_repo, json_file) == "successful":
        if set_labels(set_owner, set_repo, token, json_file) == "successful":
            if not save:
                try:
                    os.remove(json_file)
                    return "successful"
                except Exception as e:
                    print(f"{Fore.RED}✕{Fore.RESET} Error deleting temporary data file:\n{Fore.RED}{e}{Fore.RESET}")
                    return "file error"
    return "function not return successful"

# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='GitHub Labels Manager (GLM), Tools that automatically help you copy repo labels, get repo labels, and empty existing labels.')
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available command')

    # 命令：get
    parser_get = subparsers.add_parser('get', help='Get labels')
    parser_get.add_argument('repo_url', type=str, help='GitHub repo URL')
    parser_get.add_argument('--save', type=str, help='Location where the label information is saved')

    # 命令：set
    parser_set = subparsers.add_parser('set', help='Set labels')
    parser_set.add_argument('repo_url', type=str, help='GitHub repo URL')
    parser_set.add_argument('--token', type=str, help='GitHub Token')
    parser_set.add_argument('--json', type=str, help='Label data json file')

    # 命令：copy
    parser_copy = subparsers.add_parser('copy', help='Copy labels')
    parser_copy.add_argument('source_repo_url', type=str, help='Source repo URL')
    parser_copy.add_argument('set_repo_url', type=str, help='Target repo URL')
    parser_copy.add_argument('--token', type=str, help='GitHub Token')
    parser_copy.add_argument('--json', type=str, help='Location of the Label data json file (default: labels-temp.json in the glm directory)')
    parser_copy.add_argument('--save', help='Reserve acquired Label data json file', action='store_true')
    # 可选更换 acquired -> obtained @DuckDuckStudio

    # 命令：config
    parser_config = subparsers.add_parser('config', help='Modify the configuration of the program')
    parser_config.add_argument('--token', type=str, help='Set GitHub Token')
    parser_config.add_argument('--edit', help='Open configuration file', action='store_true')
    parser_config.add_argument('--version', help='Displays the version of GitHub Labels Manager (GLM)', action='store_true')

    # 命令：clear
    parser_clear = subparsers.add_parser('clear', help='Clear labels')
    parser_clear.add_argument('repo_url', type=str, help='GitHub repo URL')
    parser_clear.add_argument('--token', type=str, help='GitHub Token')

    args = parser.parse_args()

    if args.command == 'get':
        # 获取功能的实现
        running_result = formatting_url(args.repo_url)
        if running_result == "url error":
            return 1, running_result
        running_result = get_labels(running_result[0], running_result[1], args.save)
        if running_result in ["cancel", "get error"]:
            return 1, running_result
    elif args.command == 'set':
        # 设置功能的实现
        running_result = formatting_url(args.repo_url)
        if running_result == "url error":
            return 1, running_result
        if args.token:
            token = args.token
        else:
            token = read_token()
            if token in ["error", "token error"]:
                return 1, running_result
        if args.json:
            if args.json.endswith('.json'):
                running_result = set_labels(running_result[0], running_result[1], token, args.json)
            else:
                print(f"{Fore.RED}✕{Fore.RESET} The specified Label data file MUST be a json file (ending in.json)")
                return 1, running_result
        else:
            running_result = set_labels(running_result[0], running_result[1], token)
        if running_result in ["cancel", "update error", "error"]:
            return 1, running_result
    elif args.command == 'copy':
        # 复制标签功能的实现
        source_repo = formatting_url(args.source_repo_url)
        if source_repo == "url error":
            return 1, source_repo
        set_repo = formatting_url(args.set_repo_url)
        if set_repo == "url error":
            return 1, set_repo
        if args.token:
            token = args.token
        else:
            token = read_token()
            if token in ["error", "token error"]:
                return 1, running_result
        if args.json:
            json = args.json
            if not json.endswith(".json"):
                json += ".json"
            if args.save:
                running_result = copy_labels(source_repo[0], source_repo[1], set_repo[0], set_repo[1], token, json, True)
            else:
                running_result = copy_labels(source_repo[0], source_repo[1], set_repo[0], set_repo[1], token, json)
        else:
            running_result = copy_labels(source_repo[0], source_repo[1], set_repo[0], set_repo[1], token)
        if running_result in ["file error", "function not return successful"]:
            return 1, running_result
    elif args.command == 'config':
        # 配置功能的实现
        if args.token:
            running_result = set_token(args.token)
            if running_result == "error":
                return 1, running_result
        elif args.edit:
            # 仅使用一次且较短，不设置函数
            try:
                webbrowser.open(config_path)
                print(f"{Fore.GREEN}✓{Fore.RESET} The configuration file has been opened.")
            except Exception as e:
                print(f"{Fore.RED}✕{Fore.RESET} Unable to open the configuration file: {Fore.RED}{e}{Fore.RESET}\n{Fore.BLUE}[!]{Fore.RESET} 请确认配置文件路径正确: {Fore.BLUE}{config_path}{Fore.RESET}")
        elif args.version:
            print(f"{Fore.GREEN}✓{Fore.RESET} The current version is:\nGitHub Labels Manager v{Fore.BLUE}{version}{Fore.RESET}")
        else:
            print(f"{Fore.RED}✕{Fore.RESET} Missing configuration item.")
            return 1, running_result
    elif args.command == 'clear':
        # 清除功能的实现
        running_result = formatting_url(args.repo_url)
        if running_result == "url error":
            return 1, running_result
        if args.token:
            token = args.token
        else:
            token = read_token()
            if token in ["error", "token error"]:
                return 1, running_result
        running_result = clear_labels(running_result[0], running_result[1], token)
        if running_result in ["cancel"]:
            return 1, running_result
    else:
        print(f"{Fore.RED}✕{Fore.RESET} Unsupported command.")
        return 1, "command not found"
    return 0, None

if __name__ == '__main__':
    result = main()
    if result[0] != 0:
        print(f"{Fore.YELLOW}⚠{Fore.RESET} An abnormal program exit was detected，Reason: {Fore.YELLOW}{result[1]}({result[0]}){Fore.RESET}")
    input(f"{Fore.BLUE}[!]{Fore.RESET} Press {Fore.BLUE}Enter{Fore.RESET} to exit.")
    sys.exit(result[0])
