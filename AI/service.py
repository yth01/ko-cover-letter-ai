import torch
import kss
from model.TextRank_answer_summary_model import TextRank


def generate_answer(user_input, model, tokenizer):
    input_ids = []
    sentences = kss.split_sentences(user_input)
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
    model_output = []
    for ids in generate_ids:
        model_output.append(tokenizer.decode(ids[input_ids.shape[1]:], skip_special_tokens=True))
    return model_output


def generate_title(user_input, model, tokenizer):
    input_ids = tokenizer.encode(user_input, return_tensors="pt")
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
    model_output = []
    for ids in generate_ids:
        model_output.append(tokenizer.decode(ids, skip_special_tokens=True))
    return model_output


def generate_good_advice(user_input, model, tokenizer):
    input_ids = tokenizer.encode(user_input, return_tensors="pt")
    generate_ids = model.generate(input_ids,
                                  max_length=input_ids.shape[1] + 128,
                                  pad_token_id=tokenizer.pad_token_id,
                                  eos_token_id=tokenizer.eos_token_id,
                                  bos_token_id=tokenizer.bos_token_id,
                                  do_sample=True,
                                  temperature=1.1,
                                  top_k=50,
                                  top_p=0.92,
                                  num_return_sequences=3
                                  )
    model_output = []
    for ids in generate_ids:
        model_output.append(tokenizer.decode(ids, skip_special_tokens=True))
    return model_output


def generate_regret_advice(user_input, model, tokenizer):
    input_ids = tokenizer.encode(user_input, return_tensors="pt")
    generate_ids = model.generate(input_ids,
                                  max_length=input_ids.shape[1] + 256,
                                  pad_token_id=tokenizer.pad_token_id,
                                  eos_token_id=tokenizer.eos_token_id,
                                  bos_token_id=tokenizer.bos_token_id,
                                  do_sample=True,
                                  temperature=1.1,
                                  top_k=50,
                                  top_p=0.92,
                                  num_return_sequences=3
                                  )
    model_output = []
    for ids in generate_ids:
        model_output.append(tokenizer.decode(ids, skip_special_tokens=True))
    return model_output


def summarize_answer(user_input):
    return TextRank(user_input).summarize(3)
