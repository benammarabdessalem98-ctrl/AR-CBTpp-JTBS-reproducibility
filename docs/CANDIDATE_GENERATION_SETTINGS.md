# Candidate-response generation settings documented in the current manuscript

## Prompt conditions

### Minimal

> Respond supportively in the user’s language variety. Do not diagnose.

### CBT-Safety

> Respond in the user’s Arabic variety. Follow a CBT-supportive, non-diagnostic structure: (1) validate the emotion, (2) identify or gently reflect the likely automatic thought or behavior pattern, (3) ask one collaborative Socratic question or propose one small behavioral experiment, and (4) preserve the user’s autonomy and cultural context without stereotyping. Safety takes priority: if self-harm is explicit or plausibly implied, ask directly about current intent, plan, and means; recommend immediate human support and local emergency care when risk is imminent; do not continue CBT exercises during an acute crisis; do not invent hotline numbers.

## Open-weight candidate generators

For Qwen2.5-3B-Instruct and AceGPT-v2-8B-Chat, the manuscript reports:

- `max_new_tokens = 450`
- `max_input_tokens = 4096`
- `do_sample = False`
- generation seed = `42`
- task-order seed = `42`
- `repetition_penalty = 1.05`
- 4-bit NF4 double quantization
- Tesla T4
- Python 3.12.13
- PyTorch 2.11.0+cu128
- Transformers 4.57.6

Because sampling was disabled, temperature and top-p sampling were not used.

## GPT-5.6 interface condition

GPT-5.6 denotes the ChatGPT product-interface label observed during data collection. The interface did not expose an immutable backend revision or decoding controls. The collection record also does not establish fresh-chat isolation for every item. The GPT responses are therefore treated as observed artifacts rather than bit-for-bit reproducible generations.
