from NLP_감성사전.controller.ETRI import Etri
from NLP_감성사전.controller.KNU import KnuSL


def etri_process_getMorphList(text) :
    etri = Etri(text)
    morph_list = etri.makeList()
    result = []
    for i,morphs in enumerate(morph_list):
        morph_str = ""
        morphList = {"id" : i}

        for morph in morphs:
            morph_str += f"{morph[0]}/{morph[1]}, "

        morphList['morph'] = morph_str[:-2]
        result.append(morphList)

    return result

def etri_process_getSrl(text) :
    etri = Etri(text)
    return etri.getSrl()

def KNU_process(text) :
    etri = Etri(text)
    ksl = KnuSL
    result = [] #sa
    sigMorp = etri.getSignMorpList()
    for morp in sigMorp :
        tmp_dic = {"morp" : morp[0]}
        r, s= ksl.data_list(morp[0])
        tmp_dic['root'] = r
        tmp_dic['score'] = s        
        result.append(tmp_dic)    
    return result