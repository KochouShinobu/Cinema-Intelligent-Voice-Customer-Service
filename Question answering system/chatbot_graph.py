#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier import *
from question_parser import *
from answer_search import *
from speech_recognition import *
import pyttsx3 as pyttsx
import re


'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '抱歉我听不懂你在说什么！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        #print("final_answers:", final_answers)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    #print(jihe)
    question = ""
    for item in jihe:
        question = item
    print(question)
    #question = input('用户:')
    answer = handler.chat_main(question)
    print('Server:', answer)

    def change_voice(engine, language, gender='VoiceGenderFemale'):
        for voice in engine.getProperty('voices'):
            if language in voice.languages and gender == voice.gender:
                engine.setProperty('voice', voice.id)
                return True

        raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

    engine = pyttsx.init()
    change_voice(engine, "zh_CN", "VoiceGenderFemale")
    engine.say(answer)
    engine.runAndWait()

