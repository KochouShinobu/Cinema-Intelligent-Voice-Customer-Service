'''''
import os
import json

cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
data_path = os.path.join(cur_dir, 'prepare_data/data1.json')
f = open(data_path, 'r',  encoding='utf-8')
m = json.load(f)  #m:list类型数据

list1 = ['a', 'a', 'b', 'c']
x = set(list1)
print(x)
print(type(x))

movies = []
for it in m:  #it：dict类型数据
    movies += it['movie']
    print(movies)
    print(type(movies))


from py2neo import Graph, Node, Relationship, NodeMatcher

# 连图数据库
graph = Graph('http://localhost:7474', username='neo4j', password='926909')

# 创建结点，类型是Person，剩下是属性
node1 = Node('Person', label="lalala", name="lilisister", age=3)
node2 = Node('Person', label="lalala", name="lilisister2", age=2)
node3 = Node('Person', name="lily", age=23)
node4 = Node('Person', name="lilymom", age=23)

# 把结点放到到图上去
for node in [node1, node2, node3, node4]:
    graph.create(node)

# 创建关系：
relationship1 = Relationship(node1, '姐妹', node2)
graph.create(relationship1)

'''''


import pyttsx3

def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

engine = pyttsx3.init()
for voice in engine.getProperty('voices'):
    print(voice)
change_voice(engine, "zh_CN", "VoiceGenderFemale")
engine.say("你好")
engine.runAndWait()