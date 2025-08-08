import os
import sys
import json
import keyring
import argparse
import requests
import webbrowser
from tkinter import filedialog
from colorama import init, Fore

init(autoreset=True)

version = "develop"
script_path = os.path.dirname(os.path.abspath(sys.argv[0]))
config_path = os.path.join(script_path, "config.json")

# -----------------------------------------------------------------------------------------------------

def read_token():
    # 凭据 github-access-token.glm
    try:
        token = keyring.get_password("github-access-token.glm", "github-access-token")
        if token == None:
            print(f"{Fore.YELLOW}⚠{Fore.RESET} 你可能还没设置Token, 请尝试使用以下命令设置Token:\n    glm config --token <YOUR-TOKEN>\n")
            return "error"
        # else:
        return token
    except Exception as e:
        print(f"{Fore.RED}✕{Fore.RESET} 读取Token时出错:\n{Fore.RED}{e}{Fore.RESET}")
        return "error"

def set_token(token: str, yes=False):
    # 凭据 github-access-token.glm
    # == 移除 ==
    if token == "remove":
        try:
            if not yes:
                print(f"{Fore.YELLOW}⚠{Fore.RESET} 确定要移除设置的Token?")
                input(f"按{Fore.BLUE}Enter{Fore.RESET}键确认，按{Fore.BLUE}Ctrl + C{Fore.RESET}键取消...")
            keyring.delete_password("github-access-token.glm", "github-access-token")
            print(f"{Fore.GREEN}✓{Fore.RESET} 成功移除设置的Token")
            return "successful"
        except KeyboardInterrupt:
            print(f"{Fore.BLUE}[!]{Fore.RESET} 已取消操作")
            return "error"
        except Exception as e:
            print(f"{Fore.RED}✕{Fore.RESET} 移除设置的Token时出错:\n{Fore.RED}{e}{Fore.RESET}\n")
            return "error"

    # == 添加 ==
    # --- Token 检查 ---
    if not (token.startswith("ghp_") or token.startswith("github_pat_") or yes):
        print(f"{Fore.YELLOW}⚠{Fore.RESET} 请确认Token是否正确")
        try:
            input(f"按{Fore.BLUE}Enter{Fore.RESET}键确认，按{Fore.BLUE}Ctrl + C{Fore.RESET}键取消...")
        except KeyboardInterrupt:
            print(f"{Fore.BLUE}[!]{Fore.RESET} 已取消操作")
            return "error"
    # -----------------

    try:
        keyring.set_password("github-access-token.glm", "github-access-token", token)
        print(f"{Fore.GREEN}✓{Fore.RESET} 成功更新Token")
        return "successful"
    except Exception as e:
        print(f"{Fore.RED}✕{Fore.RESET} 更新Token时出错:\n{Fore.RED}{e}{Fore.RESET}\n")
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
        # GitHub API URL
        api_url = f'https://api.github.com/repos/{owner}/{repo}/labels'
        return api_url
        # 直接返回GitHub API URL
    else:
        print(f"{Fore.RED}✕{Fore.RESET} 仓库链接{Fore.YELLOW}无效{Fore.RESET}，请确保你的仓库链接正确\n{Fore.BLUE}[!]{Fore.RESET} 建议检查链接是否过度，例如以下情况:\n{Fore.GREEN}正确:{Fore.RESET} https://github.com/example/example-repo/\n{Fore.RED}错误{Fore.RESET} https://github.com/example/example-repo/labels/")
        return "url error"

def get_labels(url, save, yes=False):
    # 本函数有以下行为
    # 正常操作保存标签，并返回successful，错误时输出错误原因并返回具体错误信息
    # 可能返回如下错误
    # cancel 操作取消 | get error 获取时出错

    # v1.8
    # 在调用时如果传入 yes=True则直接确认所有提示

    # 获取标签

    if save:
        output = save
    else:
        # 无论是否 --yes 都要选择
        print("请选择保存位置:", end=" ")
        output = filedialog.asksaveasfilename(filetypes=[
            ("标签数据json文件", "*.json")
        ])

    if not output:
        print(f"{Fore.RED}✕{Fore.RESET} 未选择保存位置")
        return "cancel" # 返回取消状态

    if not output.endswith(".json"):
        output += ".json"
    
    if os.path.exists(output) and not yes:
        print(f"{Fore.YELLOW}⚠{Fore.RESET} 保存位置已被占用！是否覆盖 [Y/N]")
        if input(f"{Fore.BLUE}?{Fore.RESET} [Y] 覆盖 [N] 取消: ").lower() not in ["是", "覆盖", "y", "yes"]:
            print(f"{Fore.BLUE}[!]{Fore.RESET} 已取消操作")
            return "cancel" # 返回取消状态

    print(f"\r{Fore.GREEN}✓{Fore.RESET} 已选择保存位置: {Fore.BLUE}{output}{Fore.RESET}")
    # ------------

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
        return "successful"
    else:
        print(f"{Fore.RED}✕{Fore.RESET} 无法获取标签，返回的状态码不为200: {Fore.YELLOW}{response.status_code}{Fore.RESET}")
        return "get error"# 返回获取错误

# ---------------------------------------------------------------------------
def clear_labels(url, token, yes=False):
    # 本函数有以下行为
    # 正常操作清空指定仓库标签，并返回successful，错误时输出错误原因并返回具体错误信息
    # 可能返回如下错误
    # cancel 操作取消 | get error 获取时出错

    # v1.7
    # 在调用时如果传入 yes=True则直接确认所有提示

    flag = 0

    if not yes:
        # 确认
        print(f"{Fore.BLUE}?{Fore.RESET} 确认删除?\n{Fore.YELLOW}⚠{Fore.RESET} 此操作将清空指定仓库的{Fore.YELLOW}所有{Fore.RESET}标签，不可撤销!")
        if not (input("[Y]确认 [N]取消 : ").lower() in ["y", "yes", "确认"]):
            print(f"{Fore.BLUE}[!]{Fore.RESET} 已取消操作")
            return "cancel"

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
            if not yes:
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

def set_labels(url, token, json_file=None):
    if not json_file:
        json_file = filedialog.askopenfilename(filetypes=[
            ("标签数据json文件", "*.json"),
            ("All files", "*.*")
        ])
        if not json_file:
            print(f"{Fore.RED}✕{Fore.RESET} 未选择标签数据json文件")
            return "cancel"
    if not os.path.exists(json_file):
        print(f"{Fore.RED}✕{Fore.RESET} 选择的标签数据json文件{Fore.YELLOW}不存在{Fore.RESET}")
        return "cancel"

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
        elif response.status_code == 422 and "already_exists" in response.text:
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
                    return "update error"
        elif response.status_code == 401 and "Bad credentials" in response.text:
            print(f"{Fore.RED}✕{Fore.RESET} 创建标签 {Fore.BLUE}{label['name']}{Fore.RESET} 失败: {Fore.YELLOW}{response.status_code}{Fore.RESET}\n{Fore.RED}{response.text}{Fore.RESET}\n{Fore.BLUE}[!]{Fore.RESET} 这很有可能是因为你的 {Fore.YELLOW}Token 过期或无效{Fore.RESET} ，请检查你的 Token 是否有效\n{Fore.BLUE}[!]{Fore.RESET} 你可以使用 {Fore.GREEN}glm config --token <你的_TOKEN>{Fore.RESET} 命令来更新当前设置的 Token")
            return "error"
        else:
            print(f"{Fore.RED}✕{Fore.RESET} 创建标签 {Fore.BLUE}{label['name']}{Fore.RESET} 失败: {Fore.YELLOW}{response.status_code}{Fore.RESET}\n{Fore.RED}{response.text}{Fore.RESET}")
            return "error"
    print(f"{Fore.GREEN}✓{Fore.RESET} 成功设置所有标签！")
    return "successful"

# ---------------------------------------------------------------------------

def copy_labels(source_url, set_url, token, json_file, save=False, yes=False):
    # 调用get与set函数复制仓库标签
    # 传入先所有者，再仓库名
    # 先源仓库，再目标仓库，token，json_file，save
    if get_labels(source_url, json_file, yes) == "successful":
        if set_labels(set_url, token, json_file) == "successful":
            if not save:
                try:
                    os.remove(json_file)
                except Exception as e:
                    print(f"{Fore.RED}✕{Fore.RESET} 删除临时数据文件时出错:\n{Fore.RED}{e}{Fore.RESET}")
                    return "file error"
            print(f"{Fore.GREEN}✓{Fore.RESET} 成功复制所有标签！")
            return "successful"
    return "function not return successful"

# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='GitHub Labels Manager (GLM), 自动帮你复制仓库标签、获取仓库标签、清空已有标签的工具')
    subparsers = parser.add_subparsers(dest='command', required=True, help='可用命令')

    # 命令：get
    parser_get = subparsers.add_parser('get', help='获取标签')
    parser_get.add_argument('repo_url', type=str, help='GitHub仓库URL')
    parser_get.add_argument('--save', type=str, help='标签信息保存的位置')
    parser_get.add_argument('--yes', help='忽略(直接确认)操作中的所有提示', action='store_true')

    # 命令：set
    parser_set = subparsers.add_parser('set', help='设置标签')
    parser_set.add_argument('repo_url', type=str, help='GitHub仓库URL')
    parser_set.add_argument('--token', type=str, help='GitHub访问令牌')
    parser_set.add_argument('--json', type=str, help='标签数据文件')

    # 命令：copy
    parser_copy = subparsers.add_parser('copy', help='复制标签')
    parser_copy.add_argument('source_repo_url', type=str, help='源仓库URL')
    parser_copy.add_argument('set_repo_url', type=str, help='目标仓库URL')
    parser_copy.add_argument('--token', type=str, help='GitHub访问令牌')
    parser_copy.add_argument('--json', type=str, help='标签数据文件的存放位置(默认为glm所在目录下的labels-temp.json)')
    parser_copy.add_argument('--save', help='保留获取到的标签数据文件', action='store_true')
    parser_copy.add_argument('--yes', help='忽略(直接确认)操作中的所有提示', action='store_true')

    # 命令：config
    parser_config = subparsers.add_parser('config', help='修改配置')
    parser_config.add_argument('--token', type=str, help='设置GitHub访问令牌')
    parser_config.add_argument('--edit', help='打开配置文件', action='store_true')
    parser_config.add_argument('--version', help='显示GLM版本', action='store_true')
    parser_config.add_argument('--show', help='显示当前配置', action='store_true')
    parser_config.add_argument('--yes', help='忽略(直接确认)操作中的所有提示', action='store_true')

    # 命令：clear
    parser_clear = subparsers.add_parser('clear', help='清空标签')
    parser_clear.add_argument('repo_url', type=str, help='GitHub仓库URL')
    parser_clear.add_argument('--token', type=str, help='GitHub访问令牌')
    parser_clear.add_argument('--yes', help='忽略(直接确认)操作中的所有提示', action='store_true')

    args = parser.parse_args()

    if args.command == 'get':
        # 获取功能的实现
        running_result = formatting_url(args.repo_url)
        if running_result == "url error":
            return 1, running_result
        running_result = get_labels(running_result, args.save, args.yes)
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
                running_result = set_labels(running_result, token, args.json)
            else:
                print(f"{Fore.RED}✕{Fore.RESET} 指定的标签数据文件必须是json文件 (以.json结尾)")
                return 1, running_result
        else:
            running_result = set_labels(running_result, token)
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
            json_file = args.json
            if not json_file.endswith(".json"):
                json_file += ".json"
            running_result = copy_labels(source_repo, set_repo, token, json_file, args.save, args.yes)
        else:
            running_result = copy_labels(source_repo, set_repo, token, os.path.join(script_path, "labels-temp.json"), False, args.yes)
        if running_result in ["file error", "function not return successful"]:
            return 1, running_result
    elif args.command == 'config':
        # 配置功能的实现
        if args.show:
            with open(config_path, 'r') as file:
                data = json.load(file)

            if read_token() != 'error':
                token = f"{Fore.GREEN}已设置{Fore.RESET}"
            else:
                token = f"{Fore.YELLOW}未设置或读取出错{Fore.RESET}"

            print(f"{Fore.GREEN}✓{Fore.RESET} 当前配置信息如下:\n  账户设置:\n    Token: {token}\n  程序设置:\n    版本: {Fore.BLUE}GitHub Labels Manager v{version} by 鸭鸭「カモ」{Fore.RESET}\n      安装在: {Fore.BLUE}{script_path}{Fore.RESET}")
        elif args.token:
            running_result = set_token(args.token, args.yes)
            if running_result == "error":
                return 1, running_result
        elif args.edit:
            # 仅使用一次且较短，不设置函数
            try:
                webbrowser.open(config_path)
                print(f"{Fore.GREEN}✓{Fore.RESET} 已打开配置文件")
            except Exception as e:
                print(f"{Fore.RED}✕{Fore.RESET} 无法打开配置文件: {Fore.RED}{e}{Fore.RESET}\n{Fore.BLUE}[!]{Fore.RESET} 请确认配置文件路径正确: {Fore.BLUE}{config_path}{Fore.RESET}")
        elif args.version:
            print(f"{Fore.GREEN}✓{Fore.RESET} 当前使用的版本为:\nGitHub Labels Manager v{Fore.BLUE}{version}{Fore.RESET}\n安装在: {Fore.BLUE}{script_path}{Fore.RESET}")
        else:
            print(f"{Fore.RED}✕{Fore.RESET} 缺少配置项")
            return 1, "cancel"
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
        running_result = clear_labels(running_result, token, args.yes)
        if running_result in ["cancel"]:
            return 1, running_result
    else:
        print(f"{Fore.RED}✕{Fore.RESET} 不支持的命令")
        return 1, "command not found"
    return 0, None

if __name__ == '__main__':
    result = main()
    if result[0] != 0:
        print(f"{Fore.YELLOW}⚠{Fore.RESET} 检测到程序异常退出，原因 {Fore.YELLOW}{result[1]}({result[0]}){Fore.RESET}")
    # 因为不会有人直接运行本程序，故不用input暂停
    sys.exit(result[0])
