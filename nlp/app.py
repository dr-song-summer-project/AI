from flask import Flask, request, make_response, jsonify
from flask_restx import Api, Resource
import json
from collections import OrderedDict

from controller.nlp_controller import nlp_process
from controller.init import etri_process_getSrl
from controller.init import etri_process_getMorphList
from controller.init import KNU_process


app = Flask(__name__)
api = Api(app, version='1.0', title="nlp process api",
          description="test nlp api")

#nlp
ns = api.namespace('api', description="NLP process API")


@ns.route('')
class ApiForCorpus(Resource):
    def post(self):
        originCorpus = request.json.get('corpus')
        
        # 형태소 분석 Controller
        processed_corpus = nlp_process(originCorpus)        
        

        return make_response(processed_corpus, 200)

@ns.route('/process')
class divideCorpus(Resource):
    def post(self):
        originCorpus = request.json.get('corpus')

        processed_corpues = OrderedDict()

        processed_corpues0 = etri_process_getMorphList(originCorpus) #morph

        processed_corpus1 = etri_process_getSrl(originCorpus) #phrase

        processed_corpus2 = KNU_process(originCorpus) #sentimentScore

        processed_corpues['morph'] = processed_corpues0
        processed_corpues['phrase'] = processed_corpus1
        processed_corpues['sentiScore'] = processed_corpus2
      
        return make_response(jsonify(processed_corpues), 200)
        #받은 문장을 가지고 분석 시장

@ns.route('/sentiScore')
class knuCorpus(Resource):
    def post(self):
        originCorpus = request.json.get('corpus')
        
        processed_corpus = KNU_process(originCorpus)
        return make_response(processed_corpus, 200)
        #받은 문장을 가지고 분석 시장


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)