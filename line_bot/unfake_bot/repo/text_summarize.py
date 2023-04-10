from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

model_checkpoint = "models/e5_1"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
def summarize(text):
    input_ids = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
    generated_ids = model.generate(input_ids=input_ids,num_beams=5,repetition_penalty=2.5,length_penalty=1,early_stopping=True,num_return_sequences=1, max_new_tokens=50)
    preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
    return preds[0]