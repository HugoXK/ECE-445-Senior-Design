import speech_recognition as sr 
import sys 

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import BertModel
r = sr.Recognizer()

def infer(text):
    out_dict = {}
    output_str = ''
    for col in ['position_x', 'position_y', 'force', 'velocity_xy', 'velocity_z']:
        model_path = f'/home/wentao/project/nlp/MassageMateNLP/models/bert/{col}'
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        model.eval()
        encoded_input = tokenizer(text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0].detach().cpu().numpy()[0]
        answer = ['-1', '0', '1'][scores.argmax()]
        output_str += f'{col}: {answer}\n'
        out_dict[col] = answer 
    if 'up' in text.lower():
        out_dict['position_y'] = '1'
    elif 'down' in text.lower():
        out_dict['position_y'] = '-1'
    if 'right' in text.lower():
        out_dict['position_x'] = '1'
    elif 'left' in text.lower():
        out_dict['position_x'] = '-1'
    return out_dict


def asr():
    with sr.Microphone() as source: 
        print("Talk")
        r.adjust_for_ambient_noise(source)
        audio_text = r.listen(source,timeout=10)
        print("Time over")
        try: 
            ret_text = r.recognize_google(audio_text)
            print("Text:",ret_text)
        except:
            ret_text = ""
            print("Don't get")
    return ret_text

def nlp_main():
    out_text = asr()
    if(out_text == ""):
        return None
    else:
        return infer(out_text)

if __name__ == "__main__":
    print(nlp_main())
