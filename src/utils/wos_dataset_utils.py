import json
import os
import pathlib
from collections import Counter

import pandas as pd
import spacy

from spacy.matcher import Matcher
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

patternNew = [{"TAG": "JJ", "LEMMA": "new"},
              {"POS": "NOUN"}]
patternNovel = [{"TAG": "JJ", "LEMMA": "novel"},
                {"POS": "NOUN"}]

matcher.add("NewOrNovel", [patternNew, patternNovel])
new_words = []
novel_words = []
counts = 0


def init():
    global counts, novel_words, new_words
    new_words = []
    novel_words = []
    counts = 0


def load_file_and_process(path, key):
    global counts
    df = pd.read_excel(path)
    if key in df.columns:
        tqdm.pandas(unit='articles', position=0, postfix=f'path:{path}', desc=f'year:{year}')
        df = df[~pd.isna(df[key])]
        df[key].progress_apply(match_words)
        counts += len(df)


def match_words(content):
    try:
        doc = nlp(content)
    except Exception as e:
        print(e)
        return
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]
        text = span.lemma_.lower().split(' ')
        if text[0] == 'new':
            new_words.append(text[1])
        elif text[0] == 'novel':
            novel_words.append(text[1])


def get_files_with_extension(folder_path, extension):
    # 将文件夹路径转换为Path对象
    folder_path = pathlib.Path(folder_path)

    # 使用列表推导式获取符合条件的文件列表
    result_files = [file for file in folder_path.rglob(f'*{extension}') if file.is_file()]

    return result_files


def save_to_json(year, **args):
    json_dict = dict(year=year, **args)
    return json.dumps(json_dict)


if __name__ == '__main__':
    root_fold = 'resource\\data\\WOS数据集'
    result = []
    for year in range(2000, 2023):
        print(f'year:{year}')
        init()
        year_fold = os.path.join(root_fold, str(year))
        xls_files = get_files_with_extension(year_fold, '.xls')
        for xls in tqdm(xls_files, colour='green'):
            load_file_and_process(str(xls), 'Abstract')
        new_counter = Counter(new_words)
        novel_counter = Counter(novel_words)
        str_json = save_to_json(year, new=new_counter, novel=novel_counter, counts=counts)
        result.append(str_json)
        print(str_json)
    with open(os.path.join(root_fold, 'result.json'), 'w') as f:
        json.dump(result, f)
