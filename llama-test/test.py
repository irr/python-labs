from langchain.llms import LlamaCpp
from torch import cuda

print(cuda.current_device())

llama-2-70b-chat.ggmlv3.q3_K_L.bin
# wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q2_K.bin
model_path = r'/home/ivanrocha/Downloads/Llama/llama-2-7b-chat.ggmlv3.q2_K.bin'

llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=4,
    n_ctx=512,
    temperature=0
)

output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"])

print(output)
