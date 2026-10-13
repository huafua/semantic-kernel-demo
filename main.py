import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion

async def main():
    # 1. 初始化內核
    kernel = Kernel()

    # 2. 配置你的大模型服務（這裡以 OpenAI 為例，請替換為你實際的 API Key）
    # 提示詞插件必須依賴 LLM 服務才能運行
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="ds",
            ai_model_id="deepseek-v4-flash",
            api_key="sk-88428990f8e54413b6171b4c3bb94698"
        )
    )

    # 3. 讀取並加載 YAML 插件文件
    yaml_path = os.path.join("plugins", "joke_plugin.yml")
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_content = f.read()

    # 將 YAML 直接轉換為內核函數，並註冊到名為 "MyPlugin" 的插件容器中
    joke_function = kernel.add_function_from_prompt_yaml(
        plugin_name="MyPlugin",
        yaml_content=yaml_content
    )

    # 4. 顯式調用（因為 YAML 中沒有定義變數，所以不需要傳入 arguments）
    print("🤖 正在請求大模型講笑話...")
    response = await kernel.invoke(joke_function)

    # 5. 輸出結果
    print("\n🎉 大模型的回答：")
    print(response)

# 執行非同步主函數
if __name__ == "__main__":
    asyncio.run(main())