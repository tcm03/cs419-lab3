import json

documents = {}
all_articles = []
with open('data.json', encoding = 'utf-8') as f:
    data = json.load(f)
    for category, articles in data.items():
        all_articles.extend(articles)

with open('new_data.json', 'w', encoding = 'utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False)