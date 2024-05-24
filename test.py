from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# model_path = 'Helsinki-NLP/opus-mt-en-zh'
# model_path = './models/opus-mt-en-zh'
model_path = './models/opus-mt-zh-en'

tokenizer = AutoTokenizer.from_pretrained(model_path)

model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# sample_text = "a brown horse standing on top of a lush green field"
sample_text = "一匹棕色马 站在一片平淡的绿地顶上"

batch = tokenizer([sample_text], return_tensors="pt")

generated_ids = model.generate(**batch)

res = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(res)
