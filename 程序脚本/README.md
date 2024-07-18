# GitHub Labels Manager (GLM)

*Enjoy your day and let automation do it for you. :)*  

<img alt="Banner" src="https://svg-banners.vercel.app/api?type=rainbow&text1=GitHub%20Labels%20Manager&width=800&height=400" style="text-align: center;">

## Project profile
GLM provides the following functions:  
- [x] Gets all the labels for a repository, stored in `labels.json` of the specified directory
- [x] Empty the label of a repository *(token with repo permission required)*
- [x] Set the label of a repository according to the specified **json** file *(empty the specified repository's labels before setting, requires a token with repo permission)*
- [x] Copy the label of one repository to another repository *(empty the specified repository's labels before setting, requires a token with repo permission)*

### About icon
The current icon is for temporary use only and will be replaced if there is a formal design.  
[Social media post critiquing something.](https://www.bilibili.com/opus/949997717411594275)  
<!--这有点不好翻译...-->

> [!TIP]
> If you would like to design a new icon, you can send your design to <Yzcbs123@163.com>. Thank you for supporting this project!  

## Before use
### Python
Make sure you have the Python environment on your device.  
Run the following command to check the Python version:  

```bash
python --version
```

You might see output like this:  

```
C:\Users\user_name>python --version
Python 3.12.0
```

#### Install Required Libraries
After cd into the project directory, run the following command:  
```powershell
# Create a virtual environment
python -m venv .venv
# Activate the virtual environment
.venv\Scripts\Activate.ps1
# Install required libraries
pip install -r requirements.txt
```

> [!TIP]
> Programs obtained using winget do not need to set this.  

### Token
You need a GitHub Token to run some of the features.  

> [!TIP]
> Official document → [Managing your personal access tokens - GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#%E5%88%9B%E5%BB%BA-personal-access-token-classic)  

Follow these steps to get a GitHub Token:  

1. Sign in to GitHub:  
   Open GitHub and sign in to your account.

2. Navigate to Settings:  
   Click on your profile icon in the top right corner, then select "**Settings**".

3. Go to Token settings:  
   In the left sidebar, click on "**Developer settings**".  
   Then in the left sidebar again, locate and expand "**Personal access tokens**".  
   Select "**Tokens (classic)**" under "**Personal access tokens**".

4. Generate a new Token:  
   Click on "**Generate new token**" in the upper right corner.  
   Choose "**Generate new token (classic)**".

5. Fill in Token details:  
   Fill in the form as follows:  
   Note → Name your token.  
   Expiration → Choose "No expiration" if you want the token to never expire.  
   Select scopes → Select **repo** for the token's scope.

6. Generate the Token:  
   Click the green button at the bottom ("Generate token").

7. Copy the generated Token:  
   *Note: You won't be able to see this Token again, so make sure to store it securely and do not upload it to public repositories.*

8. Insert the Token into your configuration file:  
   Paste your Token into the `token` field in the `config.json`.

## How to get the program
Please [go to the Releases page](https://github.com/DuckDuckStudio/GitHub-Labels-Manager/releases).  

### Using winget
Run the following command:  
```powershell
winget install DuckStudio.GitHubLabelsManager
```

> [!TIP]
> If the supported version number is *n*, $1.1 \leqslant n \leqslant 1.2$  

## How to use
Run the following command for help:  
```powershell
glm --help # winget or packaged program
python glm.py --help # source code
```
Get help for subcommands:  
```powershell
glm <command> --help # winget or packaged program
python glm.py <command> --help # source code
```
