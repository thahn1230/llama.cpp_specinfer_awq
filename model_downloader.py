from transformers import AutoTokenizer, AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("google/gemma-7b")
tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b")

model.save_pretrained("./models/gemma-7b")
tokenizer.save_pretrained("./models/gemma-7b")