# SRT 字幕工具 - 生成 .exe 独立应用指南

## 🎯 目标

将 Python 项目打包成一个 **.exe 可执行文件**，可以在任何 Windows 电脑上直接运行，**无需安装 Python**。

---

## 📋 前置条件

### 必需
- Windows 7+
- Python 3.7+ **已经安装**（当前电脑上有即可）
- 网络连接（用于下载 PyInstaller）

### 检查环境

```bash
# 打开 CMD 或 PowerShell，输入：
python --version  # 应该显示 Python 3.7 或更高

pip --version     # 应该显示 pip 版本
```

---

## 🚀 快速打包步骤（5 分钟）

### 步骤 1：安装打包工具

```bash
# 打开 CMD/PowerShell，输入：
pip install pyinstaller
```

### 步骤 2：进入项目目录

```bash
# 进入项目所在目录，比如：
cd d:\PythonProject\merge_audio

# 或者用资源管理器打开项目目录，按 Shift + 右键，选择"在此处打开 PowerShell"
```

### 步骤 3：生成 .exe 文件

```bash
# 复制下面这条命令，在 PowerShell 中运行：

pyinstaller --onefile --windowed --add-data ".:." main.py

# 或者更完善的版本（包含图标）：
pyinstaller --onefile --windowed --add-data ".:." -n "SRT字幕工具" main.py
```

### 步骤 4：等待生成完成

- 第一次运行需要 2-5 分钟
- 完成后会看到提示：`131 INFO: Bundle complete! Output: ...`

### 步骤 5：获取 .exe 文件

```
你的项目目录/
├── dist/          ← 找这个文件夹
│   └── main.exe   ← 这就是你要的！
├── build/
├── main.spec
└── ...其他文件
```

✅ **完成！** 将 `dist/main.exe` 复制到任何电脑都能直接运行。

---

## 📦 完整的打包命令解释

### 参数说明

```bash
pyinstaller \
  --onefile \                    # 生成单个 .exe 文件（默认生成一堆 dll）
  --windowed \                   # 运行时不显示 cmd 窗口（GUI 应用必需）
  --add-data ".:." \             # 包含当前目录所有文件
  -n "SRT字幕工具" \             # 设置 .exe 文件名
  --icon icon.ico \              # 可选：设置图标文件
  main.py                        # 入口文件
```

### 不同场景的命令

#### 最简单版本（推荐）
```bash
pyinstaller --onefile --windowed -n "SRT字幕工具" main.py
```

#### 包含所有资源的版本
```bash
pyinstaller --onefile --windowed --add-data ".:." -n "SRT字幕工具" main.py
```

#### 带图标和版本信息
```bash
pyinstaller --onefile --windowed --add-data ".:." ^
  -n "SRT字幕工具" ^
  --icon=app.ico ^
  main.py
```

---

## 🔧 常见问题和解决方案

### 问题 1：生成的 .exe 无法运行

**症状**：双击没有反应或立即闪退

**原因**：缺少 Python 依赖包或文件

**解决**：
```bash
# 重新打包，添加所有必需的模块
pyinstaller --onefile --windowed --hidden-import=requests \
  --hidden-import=chardet --hidden-import=tkinter \
  -n "SRT字幕工具" main.py
```

### 问题 2：.exe 文件过大（>100MB）

**原因**：包含了整个 Python 环境和所有库

**这是正常的**，但可以优化：

```bash
# 使用 --onedir 模式（输出是一个文件夹）减小 .exe 本身的大小
pyinstaller --onedir --windowed -n "SRT字幕工具" main.py

# 然后将 dist/SRT字幕工具/ 文件夹整个压缩或分发
```

### 问题 3：运行时提示"ModuleNotFoundError"

**症状**：.exe 运行时说"找不到 xxx 模块"

**解决**：在打包时添加 `--hidden-import` 参数

```bash
pyinstaller --onefile --windowed \
  --hidden-import=requests \
  --hidden-import=chardet \
  --hidden-import=tkinter \
  -n "SRT字幕工具" main.py
```

### 问题 4：API 调用失败

**原因**：可能是依赖包不完整

**解决**：
```bash
# 1. 先验证当前环境没有问题
python main.py  # 能运行说明环境没问题

# 2. 重新打包，指定包含所有依赖
pyinstaller --onefile --windowed \
  --hidden-import=requests \
  --hidden-import=chardet \
  -n "SRT字幕工具" main.py

# 3. 在使用前，用当前电脑测试一下生成的 .exe
```

---

## 📂 完整的脚本文件

为了让打包更方便，可以创建一个批处理文件 `build.bat`：

```batch
@echo off
chcp 65001 >nul
echo === SRT字幕工具 EXE 打包脚本 ===
echo.

REM 检查 PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
)

REM 清空旧的打包文件
echo 清理旧文件...
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul
del /q *.spec 2>nul

REM 打包
echo.
echo 正在生成 EXE 文件...
echo 这需要 2-5 分钟，请耐心等待...
echo.

pyinstaller --onefile --windowed --add-data ".:." ^
  --hidden-import=requests ^
  --hidden-import=chardet ^
  -n "SRT字幕工具" ^
  main.py

if errorlevel 1 (
    echo 打包失败！请检查错误信息
    pause
    exit /b 1
)

echo.
echo === 打包完成！===
echo EXE 文件位置：%cd%\dist\SRT字幕工具.exe
echo.
echo 你现在可以：
echo 1. 复制 dist\SRT字幕工具.exe 到其他电脑使用
echo 2. 或者分享整个 dist 文件夹
echo.
pause
```

**使用方法**：将上面的代码保存为 `build.bat`，然后双击运行即可。

---

## 🎁 分发和使用

### 方案 1：单个 .exe 文件

如果使用的是 `--onefile` 参数：

```
dist/
└── SRT字幕工具.exe    ← 直接复制这个文件到其他电脑
```

**优点**：
- ✅ 文件小（只需发送一个 .exe）
- ✅ 容易分发
- ✅ 容易创建快捷方式

**缺点**：
- ❌ 第一次运行时解压会慢一些
- ❌ 文件本身会比较大（>100MB）

### 方案 2：文件夹模式

如果使用的是 `--onedir` 参数：

```
dist/
└── SRT字幕工具/        ← 整个文件夹复制到其他电脑
    ├── main.exe
    ├── python3.x.dll
    ├── ...其他文件
    └── ...
```

**优点**：
- ✅ 运行速度快（无需解压）
- ✅ .exe 本身较小

**缺点**：
- ❌ 需要分发整个文件夹
- ❌ 不能分离文件

### 推荐方案

**对于最终用户**：使用 `--onefile`，生成单个 .exe 文件。

```bash
# 最终推荐命令
pyinstaller --onefile --windowed --add-data ".:." \
  --hidden-import=requests --hidden-import=chardet \
  -n "SRT字幕工具" main.py

# 然后将 dist/SRT字幕工具.exe 分发给用户
```

---

## 🔐 安全和信任

### Windows SmartScreen 警告

当用户运行你的 .exe 时，可能会看到：
```
Windows 已保护你的电脑
Microsoft Defender SmartScreen 阻止了不可识别应用的启动
```

**这是正常的**（对于新应用都会这样）。

**用户可以点击**：
- "更多信息" → "仍要运行"

**如何避免这个警告**（需要付费）：
- 购买 Authenticode 证书并签名
- 等待 .exe 获得足够的下载（微软会自动信任）

---

## 📊 EXE 大小优化

### 默认大小
- 未优化：150-200MB
- 已优化：80-120MB

### 优化方法

```bash
# 1. 使用 --onedir（略小一些）
pyinstaller --onedir ...

# 2. 移除测试文件
del /q test_*.py

# 3. 删除不必要的依赖
# 检查 requirements.txt，移除未使用的包

# 4. 最终打包
pyinstaller --onefile --onefile-windowed ...
```

---

## 🧪 测试 .exe

### 在打包电脑上测试

```bash
# 1. 进入 dist 文件夹
cd dist

# 2. 双击 SRT字幕工具.exe
# 或在命令行运行：
.\SRT字幕工具.exe

# 3. 测试所有功能：
#    - 翻译
#    - 矫正
#    - 合并
```

### 在其他电脑上测试

```bash
# 将 dist\SRT字幕工具.exe 复制到另一台电脑（无需 Python）
# 在那台电脑上双击运行
# 所有功能应该正常工作
```

---

## 📝 创建快捷方式

### 美化用户体验

1. **创建快捷方式**：
   - 在 `SRT字幕工具.exe` 上右键
   - "创建快捷方式"
   - 放到桌面

2. **设置图标**（可选）：
   ```bash
   # 创建 app.ico 文件（使用在线工具或 Adobe）
   # 然后在打包时添加：
   pyinstaller --icon=app.ico ...
   ```

3. **创建启动器**：
   ```batch
   @echo off
   cd /d "%~dp0"
   SRT字幕工具.exe
   ```

---

## 🚀 完整的分发清单

### 发给用户的文件

#### 方式 1：单个 EXE（推荐）
```
发送给用户：
└── SRT字幕工具.exe  (100-150MB)
```

#### 方式 2：带说明文件
```
发送给用户：
├── SRT字幕工具.exe
├── 使用说明.txt
└── API配置指南.txt
```

#### 方式 3：完整包
```
发送给用户（压缩包）：
├── SRT字幕工具.exe
├── 使用说明.md
├── API获取指南.md
└── 示例字幕.srt
```

### 用户使用步骤

```
1. 接收 SRT字幕工具.exe
2. 双击运行（首次启动会解压，需要 30 秒）
3. 配置 API Key
4. 开始使用
```

---

## 💡 最佳实践

### 1. 版本管理
```bash
# 打包时使用版本号
pyinstaller -n "SRT字幕工具_v1.0.0" main.py

# 这样用户可以:
# - SRT字幕工具_v1.0.0.exe
# - SRT字幕工具_v1.1.0.exe
# 同时安装不同版本
```

### 2. 日志和调试
```bash
# 如果用户反保问题，可以添加日志：
# 在 main.py 添加：
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)
```

### 3. 自动更新（可选）
```python
# 在启动时检查新版本
import requests
response = requests.get('https://example.com/version.txt')
```

---

## 🆘 快速排除故障

| 问题 | 解决方案 |
|------|---------|
| .exe 闪退 | 查看错误信息，添加 `--hidden-import` |
| 找不到模块 | 检查 requirements.txt，重新打包 |
| 运行缓慢 | 使用 `--onedir` 而不是 `--onefile` |
| 文件过大 | 删除测试文件，移除不必要的依赖 |
| API 无法访问 | 验证网络，检查 API Key |

---

## 📞 下一步

1. **立即生成 .exe**：
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed -n "SRT字幕工具" main.py
   ```

2. **测试 .exe**：
   ```bash
   dist\SRT字幕工具.exe
   ```

3. **分发给用户**：
   ```
   复制 dist\SRT字幕工具.exe 到其他电脑
   ```

4. **用户使用**：
   ```
   双击 SRT字幕工具.exe
   配置 API Key
   开始使用
   ```

---

**祝打包顺利！** 🎉
