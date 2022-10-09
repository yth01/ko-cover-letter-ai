from fastapi import FastAPI
from pydantic import BaseModel
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel, BartForConditionalGeneration
from service import generate_answer, generate_title, generate_good_advice, generate_regret_advice, summarize_answer


class User(BaseModel):
    input: str


app = FastAPI()

KoGPT2_tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                           bos_token='<s>', eos_token='</s>', unk_token='<unk>',
                                                           pad_token='<pad>', mask_token='<mask>')
KoGPT2_answer_generative_model = GPT2LMHeadModel.from_pretrained("./model/KoGPT2_answer_generative_model")

KoBART_tokenizer = PreTrainedTokenizerFast.from_pretrained("gogamza/kobart-base-v2")
KoBART_title_generative_model = BartForConditionalGeneration.from_pretrained("./model/KoBART_title_generative_model")
KoBART_good_advice_generative_model = BartForConditionalGeneration.from_pretrained("./model/KoBART_good_advice_generative_model")
KoBART_regret_advice_generative_model = BartForConditionalGeneration.from_pretrained("./model/KoBART_regret_advice_generative_model")


@app.post("/generative-model/answer")
def get_generated_answer(user: User):
    return {"generated_answer": generate_answer(user.input, KoGPT2_answer_generative_model, KoGPT2_tokenizer)}


@app.post("/generative-model/title")
def get_generated_title(user: User):
    return {"generated_title": generate_title(user.input, KoBART_title_generative_model, KoBART_tokenizer)}


@app.post("/generative-model/good-advice")
def get_generated_good_advice(user: User):
    return {"generated_good_advice": generate_good_advice(user.input, KoBART_good_advice_generative_model, KoBART_tokenizer)}


@app.post("/generative-model/regret-advice")
def get_generated_regret_advice(user: User):
    return {"generated_regret_advice": generate_regret_advice(user.input, KoBART_regret_advice_generative_model, KoBART_tokenizer)}


@app.post("/summary-model/answer")
def get_summarized_answer(user: User):
    return {"summarized_answer": summarize_answer(user.input)}
