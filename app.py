from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Download the GGUF file
# model_id = "muhammadnoman76/cortex_q4"
# gguf_filename = "unsloth.Q4_K_M.gguf"  # Replace with the correct filename
# model_path = hf_hub_download(
#     repo_id=model_id,
#     filename=gguf_filename,
#     local_dir=".", 
#     local_dir_use_symlinks=False  
# )

alpaca_prompt = """
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
You are an intelligent agent that analyzes user requests and breaks them down into structured components. Your task is to:

1. Identify the specific actions needed to complete the request
2. Determine which intent-based tools would be appropriate (selecting only from the available intent list)
3. Provide brief justifications for why each intent is relevant
4. Define the high-level goals the request aims to accomplish
5. Generate a concise instruction prompt summarizing how to fulfill the request

Available intents = ["schedule", "email", "sms", "whatsapp", "web_search", "parse_document", "visualize_data", "analyze_data", "analyze_image", "gen_code", "gen_image", "calculate", "execute_code", "academic_search", "finance_news", "translation", "url", "database", "social_media"]

Important notes:
- Provide only the intent category (e.g., "email"), not specific tool names
- If you identify a needed intent that isn't in the list above, include it with "(new)" notation
- Be concise but thorough in your analysis
- Focus on practical implementation rather than theoretical discussion

### Input:
{}

### Response:
"""

# Load model from local file in the copied folder
llm = Llama(
    # model_path= r'.//unsloth.Q4_K_M.gguf',
     model_path= r'.//models--muhammadnoman76--cortex_q4//snapshots//2aa428bbefd7d6e726c270391b0940970567dabe//unsloth.Q4_K_M.gguf',
    n_ctx=2048,
    n_batch=512,
    n_gpu_layers=100,
    verbose=False
)

async def stream_llm_response(task_description: str):
    prompt = alpaca_prompt.format(task_description)
    stream = llm(
        prompt,
        max_tokens=2048,
        stream=True,
    )
    
    for output in stream:
        yield output["choices"][0]["text"]
        await asyncio.sleep(0)

@app.get("/stream")
async def stream_response(task: str = "make an agent which send mail by searching top 5 website from google"):
    return StreamingResponse(stream_llm_response(task), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)