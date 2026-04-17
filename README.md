# SRT字幕翻译工具

一个专业的SRT字幕翻译工具，严格保持时间轴不变，支持多种LLM API。

## 功能特点

- ✅ **严格保持时间轴**：翻译过程中绝对不修改 `start_time` 和 `end_time`
- ✅ **批处理优化**：支持自定义批处理大小（默认15行），减少API调用次数
- ✅ **智能提示词**：仅发送文本内容给LLM，避免时间轴信息干扰
- ✅ **多线程处理**：翻译过程不阻塞UI界面
- ✅ **完整错误处理**：网络错误、API错误自动重试
- ✅ **实时进度显示**：进度条和日志框实时反馈翻译状态
- ✅ **文件编码智能检测**：支持多种编码格式的SRT文件
- ✅ **预览功能**：翻译前可预览原文内容

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. **运行程序**：
   ```bash
   python main.py
   ```

2. **配置API设置**：
   - 输入你的API Key
   - 设置API URL（默认为OpenAI）
   - 选择合适的模型

3. **选择文件**：
   - 点击"浏览"选择SRT文件
   - 设置输出文件路径

4. **翻译设置**：
   - 选择源语言和目标语言
   - 设置批处理大小（建议15行）

5. **开始翻译**：
   - 点击"开始翻译"按钮
   - 观察进度条和日志信息

## 支持的语言

- **源语言**：Auto Detect（自动检测）、English（英语）、Chinese（中文）、French（法语）、Japanese（日语）、Korean（韩语）
- **目标语言**：Chinese（中文）、English（英语）、French（法语）、Japanese（日语）、Korean（韩语）

## API配置说明

### DeepSeek API（默认配置）
```
API URL: https://api.deepseek.com/v1
API Key: your_deepseek_api_key
模型: deepseek-chat, deepseek-coder
```

### OpenAI API
```
API URL: https://api.openai.com/v1/chat/completions
模型: gpt-3.5-turbo, gpt-4, gpt-4-turbo
```

### 其他兼容API
支持任何兼容OpenAI ChatGPT API格式的服务，只需修改API URL即可。

## 文件结构

```
merge_audio/
├── main.py              # 主程序入口
├── gui.py               # GUI界面
├── srt_parser.py        # SRT文件解析器
├── translator.py        # 翻译引擎和处理逻辑
├── requirements.txt     # 依赖包列表
└── README.md           # 使用说明
```

## 核心逻辑说明

### 1. SRT解析
- 使用正则表达式精确解析SRT格式
- 智能检测文件编码
- 严格保持时间轴数据不变

### 2. 翻译流程
- 批处理方式减少API调用
- 仅发送纯文本内容给LLM
- 智能解析翻译结果
- 自动行数匹配验证

### 3. 错误处理
- API调用失败自动重试
- 翻译结果格式验证
- 网络异常处理
- 文件操作异常处理

## 注意事项

1. **API配额**：注意API调用次数限制，适当调整批处理大小
2. **网络连接**：确保网络连接稳定
3. **文件备份**：建议翻译前备份原始SRT文件
4. **编码格式**：程序会自动处理编码，建议使用UTF-8格式

## 常见问题

### Q: 翻译失败怎么办？
A: 检查API Key和网络连接，查看日志框中的错误信息。

### Q: 如何添加其他LLM API？
A: 在API设置中修改URL和模型名称即可。

### Q: 翻译结果不准确怎么办？
A: 可以尝试调整模型参数，或者减小批处理大小以提高翻译质量。

## 许可证

本项目仅供学习和个人使用。
