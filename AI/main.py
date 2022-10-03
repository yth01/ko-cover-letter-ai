import torch
import kss
from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from transformers import GPT2LMHeadModel
from transformers import PreTrainedTokenizerFast

app = FastAPI()

generative_model = GPT2LMHeadModel.from_pretrained("./model/koGPT2_answer_generative_model")
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
  bos_token='<s>', eos_token='</s>', unk_token='<unk>',
  pad_token='<pad>', mask_token='<mask>')


class CoverLetter(BaseModel):
    input: str
    output: Union[list, None] = None


@app.post("/answer/generative-model")
def generate_answer(cover_letter: CoverLetter):
    input_ids = []
    sentences = kss.split_sentences(cover_letter.input)
    for sentence in sentences[:-1]:
        input_ids += tokenizer.encode(sentence) + tokenizer.encode("<unused0>")
    if '.' in sentences[-1]:
        input_ids += tokenizer.encode(sentences[-1]) + tokenizer.encode("<unused0>")
    else:
        input_ids += tokenizer.encode(sentences[-1])
    input_ids = torch.tensor([input_ids])

    generate_ids = generative_model.generate(input_ids,
                              max_length=input_ids.shape[1] + 256,
                              pad_token_id=tokenizer.pad_token_id,
                              eos_token_id=tokenizer.encode("<unused0>")[0],
                              bos_token_id=tokenizer.bos_token_id,
                              do_sample=True,
                              temperature=1.1,
                              top_k=50,
                              top_p=0.92,
                              num_return_sequences=5
                              )
    cover_letter.output = []
    for ids in generate_ids:
        cover_letter.output.append(tokenizer.decode(ids[input_ids.shape[1]:], skip_special_tokens=True))
    return {"generate_answer": cover_letter.output}
