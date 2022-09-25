import re
import numpy as np
import pandas as pd


def _str_replace(text, patterns: list, replacement=" "):
    assert isinstance(text, pd.core.series.Series)
    assert isinstance(patterns, list)

    for pattern in patterns:
        text = text.str.replace(pattern, replacement)

    return text


def _re_sub(text, patterns: dict):
    assert isinstance(text, pd.core.series.Series)
    assert isinstance(patterns, dict)

    for pattern in patterns:
        text[text.notna()] = text[text.notna()].apply(lambda x: re.sub(pattern, patterns[pattern], x))

    return text


def _filt_and_trim(text, only_hangul=False, replacement=" "):
    assert isinstance(text, pd.core.series.Series)
    pattern = "[^ㄱ-ㅎㅏ-ㅣ가-힣]" if only_hangul else "[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9&.]"

    text[text.notna()] = text[text.notna()].apply(lambda x: re.sub(pattern, replacement, x))
    text[text.notna()] = text[text.notna()].apply(lambda x: re.sub("\s+", replacement, x))

    return text.str.strip()


def _preprocess_company(data):
    assert isinstance(data, pd.core.frame.DataFrame)

    data["회사명"] = data["회사명"].str.lower()
    data["회사명"] = _str_replace(data["회사명"], patterns=["㈜", "주식회사"])
    data["회사명"] = _re_sub(data["회사명"], patterns={r"\([^)]*\)": " "})
    data.loc[data["회사명"].str[0] == "셰", "회사명"] = "셰플러코리아"
    data["회사명"] = _filt_and_trim(data["회사명"])

    return data


def _preprocess_field(data):
    assert isinstance(data, pd.core.frame.DataFrame)

    data["직무분야"] = data["직무분야"].str.split("·")

    for i in range(data["직무분야"].apply(lambda x: len(x)).max()):
        idx = data["직무분야"].apply(lambda x: len(x) >= (i + 1))
        data.loc[idx, f"직무분야_{i + 1}"] = data.loc[idx, "직무분야"].apply(lambda x: x[i])

    data.drop(columns=["직무분야"], inplace=True)

    return data


def _split_title(data):
    assert isinstance(data, pd.core.frame.DataFrame)

    data = data.sort_index()
    data_ = data.copy()
    data_["답변"] = _re_sub(data_["답변"], patterns={
        "\r\n\"": "{",
        "\"\r": "}",
        "\s*\[": "{",
        "\]": "}",
        "[\s]": " "
    })
    data_title = data_[data_["답변"].str.contains('{' and '}')]
    idx = data_title.index
    data_no_title = data_.drop(idx)
    data_no_title["제목"] = np.nan
    data_title["제목"] = _re_sub(data_title["답변"], patterns={
        "\{": "",
        "\}.*": ""
    })
    title = pd.concat([data_title["제목"], data_no_title["제목"]], axis=0).sort_index()
    data["제목"] = title

    return data


def _preprocess_qna(data):
    assert isinstance(data, pd.core.frame.DataFrame)

    data = _split_title(data)
    data["답변"] = data["답변"].str.lower()
    data["답변"] = _re_sub(data["답변"], patterns={
        "아쉬운점\s\d": " ",
        "좋은점\s\d": " ",
        "글자수\s\d{1,}[,]?\d{1,}자\d{1,}[,]?\d{1,}byte": " ",
        "[,]{1,}": " ",
        "o{3,}": " ",
        "[\s]": " "
    })
    data["답변"] = _filt_and_trim(data["답변"])

    return data