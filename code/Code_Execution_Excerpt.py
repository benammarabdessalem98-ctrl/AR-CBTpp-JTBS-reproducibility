"""AR-CBT++ representative execution excerpt.

This is a compact, non-secret excerpt of the frozen Kaggle three-judge runner used
for the reported evaluation. It documents revision locking, prompt hashing,
4-bit NF4 loading controls, and per-item audit persistence. The complete notebooks
were executed separately for Qwen3-8B, Mistral-Nemo-Instruct-2407, and Gemma-3-12B-IT.
"""
import hashlib, json
import torch
from huggingface_hub import HfApi
from transformers import BitsAndBytesConfig

EXPECTED_ITEMS = 144
MAX_INPUT_TOKENS = 3000
MAX_NEW_TOKENS = 260
SEED = 42

MODEL_PROFILES = {
    "J_Qwen3": (
        "Qwen/Qwen3-8B",
        "b968826d9c46dd6066d109eabc6255188de91218",
    ),
    "J_MistralNemo": (
        "mistralai/Mistral-Nemo-Instruct-2407",
        "04d8a90549d23fc6bd7f642064003592df51e9b3",
    ),
    "J_Gemma3_12B": (
        "google/gemma-3-12b-it",
        "96b6f1eccf38110c56df3a15bffe176da04bfd80",
    ),
}

EXPECTED_SYSTEM_SHA256 = (
    "53a7b9cb5f929c651a240deff94ddd43def5e537a09897ab645b8a09e1a7c24a"
)
EXPECTED_ITEM_TEMPLATE_SHA256 = (
    "df2b92690605f9996983247ab4d0db201b2798e47d269f4c0445617e5d5a9638"
)

def verify_frozen_text(system_prompt, item_template):
    system_sha = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
    item_sha = hashlib.sha256(item_template.encode("utf-8")).hexdigest()
    if system_sha != EXPECTED_SYSTEM_SHA256:
        raise RuntimeError("Frozen system prompt SHA mismatch.")
    if item_sha != EXPECTED_ITEM_TEMPLATE_SHA256:
        raise RuntimeError("Frozen item-template SHA mismatch.")


def verify_model_revision(repo, expected_sha, hf_token):
    info = HfApi().model_info(
        repo_id=repo, revision=expected_sha, token=hf_token
    )
    if info.sha != expected_sha:
        raise RuntimeError(f"Exact model revision mismatch: {info.sha}")


def quantization_config():
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )


def persist_audit_record(path, judge_id, repo, model_sha, item_id,
                         status, retry_count, prompt_sha, raw_output, error):
    record = {
        "judge_id": judge_id,
        "judge_model": repo,
        "model_commit_sha": model_sha,
        "judge_item_id": item_id,
        "status": status,
        "retry_count": retry_count,
        "prompt_sha256": prompt_sha,
        "raw_output": raw_output,
        "error": error,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
