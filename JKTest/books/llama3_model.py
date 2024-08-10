from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


model_name = 'facebook/bart-large-cnn'  # Replace with the actual model name or path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


# Tokenize with explicit parameter setting
class GenerateSummary:
    """
    Generate Summary
    """
    def __init__(self) -> None:
        pass
    
    def generate_summary(self, text):
        inputs = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary


