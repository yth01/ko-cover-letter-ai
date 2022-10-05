import torch
import kss
from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel, BartForConditionalGeneration
from model.TextRank_answer_summary_model import TextRank

app = FastAPI()

KoGPT2_tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
  bos_token='<s>', eos_token='</s>', unk_token='<unk>',
  pad_token='<pad>', mask_token='<mask>')
KoGPT2_answer_generative_model = GPT2LMHeadModel.from_pretrained("./model/koGPT2_answer_generative_model")

KoBART_tokenizer = PreTrainedTokenizerFast.from_pretrained("gogamza/kobart-base-v2")
KoBART_title_generative_model = BartForConditionalGeneration.from_pretrained("./model/koBART_title_generative_model")


class CoverLetter(BaseModel):
    input: str
    output: Union[list, None] = None


@app.post("/answer/generative-model")
def generate_answer(cover_letter: CoverLetter):

    tokenizer = KoGPT2_tokenizer
    model = KoGPT2_answer_generative_model

    input_ids = []
    sentences = kss.split_sentences(cover_letter.input)
    for sentence in sentences[:-1]:
        input_ids += tokenizer.encode(sentence) + tokenizer.encode("<unused0>")
    if '.' in sentences[-1]:
        input_ids += tokenizer.encode(sentences[-1]) + tokenizer.encode("<unused0>")
    else:
        input_ids += tokenizer.encode(sentences[-1])
    input_ids = torch.tensor([input_ids])

    generate_ids = model.generate(input_ids,
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


@app.post("/title/generative-model")
def generate_answer(cover_letter: CoverLetter):

    tokenizer = KoBART_tokenizer
    model = KoBART_title_generative_model

    input_ids = tokenizer.encode(cover_letter.input, return_tensors="pt")
    generate_ids = model.generate(input_ids,
                              max_length=input_ids.shape[1] + 16,
                              pad_token_id=tokenizer.pad_token_id,
                              eos_token_id=tokenizer.eos_token_id,
                              bos_token_id=tokenizer.bos_token_id,
                              do_sample=True,
                              temperature=1.1,
                              top_k=50,
                              top_p=0.92,
                              num_return_sequences=5
                              )
    cover_letter.output = []
    for ids in generate_ids:
        cover_letter.output.append(tokenizer.decode(ids, skip_special_tokens=True))
    return {"generate_title": cover_letter.output}


@app.post("/answer/summary-model")
def summary_answer(cover_letter: CoverLetter):
    textrank = TextRank(cover_letter.input)
    cover_letter.output = textrank.summarize(3)
    return {"summary_answer": cover_letter.output}
