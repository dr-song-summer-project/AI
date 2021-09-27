# from flask import Flask, request
# from flask_restx import Api, Resource, reqparse

import json
from collections import OrderedDict
from khaiii import KhaiiiApi

api = KhaiiiApi()

# 형태소 분석 과정 (형태소 분해부)
def nlp_process(text):
    file_data = OrderedDict() 
    mor_list = [[] for _ in range(len(api.analyze(text)))] #test version

    for i, word in enumerate(api.analyze(text)):
        morph_dic = {"index" : i}
        morph_str = ""
        for morph in word.morphs:
            #morph lex, tag를 dic 에 추가
            # morph_dic[morph.lex] = morph.tag #형태소를 쓸 때 씀            
            morph_str += f"{morph.lex}/{morph.tag}, "
            mor_list[i].append((morph.lex, morph.tag)) #test version
            
        morph_dic["morph"] = morph_str[:-2]
        file_data[i] = morph_dic
        morph_dic = {}

    print(mor_list) #test version
        

    json_data = json.dumps(file_data, ensure_ascii=False)    

    return json_data