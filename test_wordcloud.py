import redis
from redis import Redis
import json
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

r = redis.Redis(host='localhost', port=6379)

stopwords = set()
with open('chineseStopWords.txt', encoding='gbk') as f:
    for line in f:
        print(line.rstrip('\r\n').encode())
        stopwords.add(line.rstrip('\r\n'))

print(len(stopwords))
print(stopwords)
items = redis.lrange('dbreview:items', 0, -1)
print(type(items))


words = {}
for item in items:
    val = json.loads(item)['review']
    for word in jieba.cut(val):
        words[word] = words.get(word, 0) + 1
print(len(words))  # 829
print(sorted(words.items(), key=lambda x: x[1], reverse=True))
# [('，', 119), ('的', 73), ('。', 55), ('了', 42), ('是', 23), (' ', 22), ('人', 19), # ('也', 19), ('和', 16), ('彩蛋', 16), ('!', 15), ('反派', 13),
# ('蚁', 13), ('在', 12), ('我', 12), ('都', 12), ('被', 11), ('很', 11), ('好', 10)


words = {}
for item in items:
    val = json.loads(item)['review']
    for word in jieba.cut(val):
        if word not in stopwords:
            words[word] = words.get(word, 0) + 1

total = len(words)
print(total)
frenq = {k: v / total for k, v in words.items()}
print(sorted(frenq.items(), key=lambda x: x[1], reverse=True))

wordcloud = WordCloud(font_path='simhei.ttf', background_color='white', max_font_size=80)

plt.figure(2)
wordcloud.fit_words(frenq)
plt.imshow(wordcloud)
plt.axis('off')  # 去掉坐标系 plt.show()
