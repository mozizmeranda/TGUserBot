from transformers import AutoModelForCausalLM, AutoTokenizer

# Укажи название модели (например, RuGPT)
model_name = "sberbank-ai/rugpt3large_based_on_gpt2"

# Скачай токенизатор
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Скачай модель
model = AutoModelForCausalLM.from_pretrained(model_name)

# Сохрани модель и токенизатор локально
model.save_pretrained("./rugpt_model")
tokenizer.save_pretrained("./rugpt_tokenizer")

print("Модель и токенизатор успешно скачаны!")