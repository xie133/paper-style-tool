# 论文风格助手

将论文语气调整为更像自己的写作风格，支持缩写和扩写，由 Claude AI 驱动。

## 功能

- **改语气**：上传自己的写作样本，工具学习你的风格后改写论文，内容保持不变
- **缩写**：按目标字数或自然语言指令压缩论文
- **扩写**：按目标字数或自然语言指令扩展论文
- 支持中文和英文论文
- 输入：粘贴文本 / 上传 .txt .pdf .docx
- 输出：页面显示（流式）/ 下载 DOCX 或 PDF

## 快速开始

### 1. 配置 API Key

编辑项目根目录的 `.env` 文件：

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

打开 http://localhost:5173

## 使用说明

1. **左栏**：上传自己写的文章作为风格样本（可多篇），填写风格文字描述
2. **中栏**：粘贴论文或上传文件，选择操作模式（改语气 / 缩写 / 扩写）
3. **右栏**：查看流式输出结果，可复制或下载为 DOCX / PDF

## 运行测试

```bash
cd backend
pytest tests/ -v
```

## 项目结构

```
paper-style-tool/
├── backend/
│   ├── main.py              # FastAPI 入口和路由
│   ├── file_parser.py       # 文件解析（PDF/DOCX/TXT）
│   ├── prompt_builder.py    # Prompt 构建与语言检测
│   ├── claude_client.py     # Claude API 流式调用
│   ├── downloader.py        # DOCX/PDF 文件生成
│   └── tests/               # 后端单元测试
├── frontend/
│   └── src/
│       ├── App.jsx           # 主应用（状态管理）
│       ├── api.js            # API 调用封装
│       └── components/       # 三栏组件
├── .env                      # API Key（不提交到 git）
└── README.md
```
