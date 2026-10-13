# Semantic Kernel Python YAML 插件範例 (Kernel)

本專案是一個基於 **Microsoft Semantic Kernel (Python SDK)** 的範例專案，展示如何透過 **YAML** 格式定義提示詞外掛（Prompt Plugin），並在 Semantic Kernel 中動態載入與調用大語言模型（LLM）服務。

---

## 📑 目錄 (Table of Contents)

- [專案簡介](#-專案簡介)
- [核心特性](#-核心特性)
- [專案結構](#-專案結構)
- [環境需求](#-環境需求)
- [安裝指南](#-安裝指南)
- [配置說明](#-配置說明)
- [快速開始](#-快速開始)
- [YAML 外掛結構說明](#-yaml-外掛結構說明)
- [注意事項](#-注意事項)

---

## 📖 專案簡介

Semantic Kernel 支援以 YAML 格式宣告式地編寫 Prompt 外掛。這將 Prompt 模板、執行參數（如 `temperature`、`max_tokens`）以及函數描述與主程式碼解耦，便於維護、版本控管與團隊協作。

本範例專案展示：
1. 如何初始化 `Kernel` 實例。
2. 配置 OpenAI 相容的 Chat Completion 服務（例如 DeepSeek、OpenAI 等）。
3. 讀取並使用 `kernel.add_function_from_prompt_yaml()` 載入 YAML 提示詞外掛。
4. 非同步調用該函數並獲取模型回覆。

---

## ✨ 核心特性

- **現代化套件管理**：使用 [uv](https://github.com/astral-sh/uv) 進行快速、可靠的 Python 虛擬環境與相依套件管理。
- **宣告式 Prompt 外掛**：使用 Semantic Kernel 標準 YAML 格式定義提示詞與參數。
- **多模型相容**：基於 `OpenAIChatCompletion`，可靈活對接 OpenAI、Azure OpenAI 或支援 OpenAI 相容 API 的模型服務商（如 DeepSeek）。
- **非同步支援**：全流程基於 Python `asyncio` 非同步設計。

---

## 📁 專案結構

```text
kernel/
├── plugins/
│   └── joke_plugin.yml     # YAML 格式提示詞外掛 (Prompt Plugin)
├── .python-version         # 建議 Python 版本 (3.13)
├── main.py                 # 主程式：Kernel 初始化、載入外掛與調用
├── pyproject.toml          # 專案相依性與規格定義
├── uv.lock                 # uv 套件鎖定檔案
└── README.md               # 專案說明文件
```

---

## 🛠 環境需求

- **Python**：>= 3.13
- **套件管理工具**：建議使用 [uv](https://github.com/astral-sh/uv)（亦可使用原生 `pip` / `venv`）

---

## 🚀 安裝指南

### 方式一：使用 uv（推薦）

1. 若尚未安裝 `uv`，可參考官方說明安裝：
   - **Windows (PowerShell)**:
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```
   - **macOS / Linux**:
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

2. 進入專案根目錄並同步虛擬環境與相依套件：
   ```bash
   uv sync
   ```

### 方式二：使用原生 Python venv 與 pip

```bash
# 建立虛擬環境
python -m venv .venv

# 啟用虛擬環境
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 安裝相依套件
pip install -e .
```

---

## ⚙️ 配置說明

在執行前，請編輯 `main.py` 中的模型連線資訊：

```python
kernel.add_service(
    OpenAIChatCompletion(
        service_id="ds",
        ai_model_id="deepseek-v4-flash",  # 替換為欲使用的模型名稱
        api_key="your_api_key_here"      # 替換為實際的 API Key
        # 若為第三方相容服務商 (如 DeepSeek)，可透過 base_url 指定 API Endpoint
    )
)
```

> 💡 **安全提示**：建議透過環境變數（如 `os.getenv("OPENAI_API_KEY")`）載入 API Key，避免將私鑰提交至版本控制系統中。

---

## 💻 快速開始

完成設定後，執行主程式：

### 使用 uv 執行：
```bash
uv run python main.py
```

### 或直接在啟用虛擬環境後執行：
```bash
python main.py
```

### 預期輸出範例：
```text
🤖 正在請求大模型講笑話...

🎉 大模型的回答：
為什麼企鵝的肚子是白色的？
因為牠手太短，洗澡只能洗到前面。
```

---

## 📝 YAML 外掛結構說明

`plugins/joke_plugin.yml` 遵循 Semantic Kernel YAML 規範：

```yaml
name: "get_joke"                        # 函數名稱
description: "隨機講一個好笑的冷笑話"      # 函數描述（可供 Planner 或 Agent 自主調用識別）
template_format: "semantic-kernel"      # 模板格式
template: |                             # 提示詞模板
  請為用戶隨機講一個幽默、冷門且好笑的冷笑話。
  不要說任何廢話，直接輸出笑話內容。
execution_settings:                     # 執行參數設定
  default:
    temperature: 0.7
    max_tokens: 200
```

若需要在外掛中使用變數，可以使用 `{{$變數名}}` 語法，例如：
```yaml
template: |
  請為用戶講一個關於 {{$topic}} 的冷笑話。
```
在調用時傳入 `KernelArguments(topic="程式設計師")` 即可。

---

## ⚠️ 注意事項

1. **API Key 保護**：請勿在公開儲存庫中硬編碼真實的 API 金鑰。
2. **模型相容性**：若使用非 OpenAI 原生端點（如自建模型、DeepSeek 等），請確保服務支援 OpenAI Chat Completion 格式介面。
3. **Semantic Kernel 版本**：本專案使用 `semantic-kernel >= 1.36.0`，語法採用 Semantic Kernel 1.x 最新架構。
