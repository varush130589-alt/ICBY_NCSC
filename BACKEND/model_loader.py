import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "IBCY_QWEN3_4B_FINAL",
    "IBCY_QWEN3_4B_FINAL"
)

print("Loading IBCY tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    local_files_only=True
)

print("Tokenizer loaded.")

print("Loading IBCY model into RAM...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    local_files_only=True,
    torch_dtype="auto",
    device_map={"": "cpu"},
    low_cpu_mem_usage=True
)

model.eval()

print("IBCY model loaded successfully.")
print("Device: CPU")


def generate_response(message, history=None):

    messages = []

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": message
    })

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    response = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True
    )

    return response