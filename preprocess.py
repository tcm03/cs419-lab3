import json
import re

import py_vncorenlp
py_vncorenlp.download_model(save_dir='.')
rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='.')


def preprocess_vietnamese_text(text, normalize_spaces=True):
    allowed_chars = "aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐ" \
                    "eEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊ" \
                    "jJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢ" \
                    "pipPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲ" \
                    "ỷỶỹỸýÝỵỴzZ0-9 "

    # Compile a regular expression pattern to match only allowed characters
    pattern = f"[^{re.escape(allowed_chars)}]"

    # Remove any character not in the allowed set
    cleaned_text = re.sub(pattern, "", text)

    # Normalize spaces if required
    if normalize_spaces:
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    return cleaned_text

def lowercase(text):
  return text.lower()

def tokenize(text, tokenizer):
  return tokenizer.word_segment(text)

def remove_stopwords(text):
    text = text.split()
    f = open('./vietnamese-stopwords.txt', 'r')
    stopwords = f.readlines()
    stop_words = [s.replace("\n", '') for s in stopwords]
    doc_words = []
    for word in text:
      if word not in stop_words:
        doc_words.append(word)
    doc_str = ' '.join(doc_words).strip()
    return doc_str

def text_preprocessing(text):
  text = preprocess_vietnamese_text(text)
  text = lowercase(text)
  text = tokenize(text, rdrsegmenter)[0]
  text = remove_stopwords(text)
  return text

def get_data():
  articles = []
  with open('new_data.json', encoding = 'utf-8') as f:
    articles = json.load(f)
  return articles

def preprocess():
    documents = {}
    articles = get_data()
    for article in articles:
      content = article['title'] + ' ' + article['content']
      documents[article['postId']] = text_preprocessing(content)

    # write all documents into a json file
    with open('documents.json', 'w', encoding = 'utf-8') as f:
        json.dump(documents, f, ensure_ascii=False)

if __name__ == "__main__":
    preprocess()