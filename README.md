# GitHub Labels Manager (GLM)

## 项目简介
GLM提供了以下几种功能:  
- [x] 获取某个仓库的所有标签，并存在指定目录的`labels.json`中
- [ ] 清空某个仓库的标签 *(需要有repo权限的token)*
- [ ] 依据指定的**json**文件设置某个仓库的标签 *(先清空指定仓库后再设置，需要有repo权限的token)*
- [ ] 复制某个仓库的标签到另一个仓库 *(先清空指定仓库后再设置，需要有repo权限的token)*

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

### Token
你需要一个GitHub Token才可以运行部分功能。  
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

## 如何获取
使用Git克隆本仓库即可。  
```powershell
git clone https://github.com/DuckDuckStudio/GitHub-Labels-Manager.git
```
