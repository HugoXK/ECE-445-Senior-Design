
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BertModel

def infer(text):
    output_str = ''
    for col in ['position_x', 'position_y', 'force', 'velocity_xy', 'velocity_z']:
        model_path = f'./MassageMateNLP/models/bert/{col}'
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        model.eval()
        
        encoded_input = tokenizer(text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0].detach().cpu().numpy()[0]
        answer = ['-1', '0', '1'][scores.argmax()]
        output_str += f'{col}: {answer}\n'
    return output_str

if __name__ == "__main__":
    print(infer("That's hurt, be milder!"))
