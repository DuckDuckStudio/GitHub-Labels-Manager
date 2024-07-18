# GitHub Labels Manager (GLM)

*Enjoy your day and let automation do it for you. :)*  

<img alt="Banner" src="https://svg-banners.vercel.app/api?type=rainbow&text1=GitHub%20Labels%20Manager&width=800&height=400" style="text-align: center;">

[中文](https://github.com/DuckDuckStudio/GitHub-Labels-Manager/blob/main/README.md) | [English](https://github.com/DuckDuckStudio/GitHub-Labels-Manager/blob/main/other-languages/en_US/README.md)  

## 项目简介
GLM提供了以下几种功能:  
- [x] 获取某个仓库的所有标签，并存在指定目录的`labels.json`中
- [x] 清空某个仓库的标签 *(需要有repo权限的token)*
- [x] 依据指定的 **json** 文件设置某个仓库的标签 *(先清空指定仓库的标签后再设置，需要有repo权限的token)*
- [x] 复制某个仓库的标签到另一个仓库 *(先清空指定仓库的标签后再设置，需要有repo权限的token)*

### 关于图标
目前的图标仅作临时使用，后续如有正式设计将会替换。  
[吐槽动态](https://www.bilibili.com/opus/949997717411594275)  

> [!TIP]
> 如果你想设计新图标可以将你的设计发至<Yzcbs123@163.com>，感谢您对本项目的支持！  

## 使用前配置
### Python
请确保你的设备上有Python环境。  
运行以下命令检查Python版本：  

```bash
python --version
```

你可能会看到类似这样的输出：  

```
C:\Users\user_name>python --version
Python 3.12.0
```

#### 安装所需库
`cd`到项目目录后运行如下命令:  
```powershell
# 创建虚拟环境
python -m venv .venv
# 激活虚拟环境
.venv\Scripts\Activate.ps1
# 安装所需库
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

> [!TIP]
> 使用winget获取的不需要弄。  

### Token
你需要一个GitHub Token才可以运行部分功能。  

> [!TIP]
> 官方文档 → [管理个人访问令牌 - GitHub 文档](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#%E5%88%9B%E5%BB%BA-personal-access-token-classic)  

请按照以下步骤获取GitHub Token。  

1. 登录 GitHub：  
   打开 GitHub 并登录到您的账户。  

2. 进入设置页面：  
   点击右上角的个人头像，然后选择“**Settings**”（设置）。  

3. 导航到Token设置：  
   在左侧菜单中，点击“**Developer settings**”（开发者设置）。  
   然后再在左侧菜单上，找到并点击展开“**Personal access tokens**”（个人账户Tokens）。  
   选择“**Personal access tokens**”下的“**Tokens (classic)**”（Tokens（典型））。  

4. 新建Token：  
   在右上角展开“**Generate new token**”（生成新的Token）。  
   选择“**Generate new token (classic)**”（生成新的Token（典型））。  

5. 填写Token信息：  
   按着表格填就好。  
   Note → Token的名字，随便取，中文也行。  
   Expiration → Token存在的时间，可以选“No expiration”（不会过期）。  
   Select scopes → Token的作用域，这里需要选**repo**。  

6. 生成Token：  
   点击最下面的绿色按钮（“Generate token”（生成Token））生成Token。  

7. 复制生成的Token：  
   *请注意，在此之后你将无法再次获取这个Token，请妥善保管Token，不要上传到公共仓库中。*  

8. 将Token填入配置文件：  
   将你的Token填入`config.json`中的`token`中。  
   或者运行`glm config --token <YOUR-TOKEN>`。

## 如何获取
请[前往Releases页获取](https://github.com/DuckDuckStudio/GitHub-Labels-Manager/releases)  

### 使用winget获取
运行以下命令:  
```powershell
winget install DuckStudio.GitHubLabelsManager
```

> [!TIP]
> 设支持的版本号为n，则 $1.1 \leqslant n \leqslant 1.2$  

## 如何使用
运行以下命令以获取帮助:  
```powershell
glm --help # winget获取的
python glm.py --help # python源码的
```
获取子命令的帮助:  
```powershell
glm <command> --help # winget获取的
python glm.py <command> --help # python源码的
```
