from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from clean import clean
import json
from kafka import KafkaConsumer, KafkaProducer
from time import sleep
'''
NNG	일반 명사 -> 반드시 남겨둔다
NNP	고유 명사 -> 반드시 남겨둔다
NNB	의존 명사 -> 반드시 삭제
NR	수사 -> 반드시 삭제
NP	대명사 -> 반드시 삭제
VV	동사
VA	형용사
VX	보조 용언
VCP	긍정 지시사(이다)
VCN	부정 지시사(아니다)
MM	관형사 -> 긴가민가
MAG	일반 부사 -> 
MAJ	접속 부사 -> 
감탄사	IC	감탄사 ->
조사는 전부 삭제
JKS	주격 조사
JKC	보격 조사
JKG	관형격 조사
JKO	목적격 조사
JKB	부사격 조사
JKV	호격 조사
JKQ	인용격 조사
JX	보조사
JC	접속 조사
어미는 모두 삭제
EP	선어말 어미
EF	종결 어미
EC	연결 어미
ETN	명사형 전성 어미
ETM	관형형 전성 어미
XPN	체언 접두사
접미사(XS)	XSN	명사 파생 접미사
XSV	동사 파생 접미사
XSA	형용사 파생 접미사
어근	XR	어근
SF	종결 부호(. ! ?) -> 반드시 제외
SP	구분 부호(, / : ;) -> 반드시 제외
SS	인용 부호 및 괄호(' " ( ) [ ] < > { } ― ‘ ’ “ ” ≪ ≫ 등) -> 반드시 제외
SE	줄임표(…) -> 반드시 제외
SO	붙임표(- ~) -> 반드시 제외
SW	기타 특수 문자 -> 이거는 모르겠다?
SL	알파벳(A-Z a-z) -> 남겨두기
SH	한자 -> 남겨두기
SN	숫자(0-9) -> 이거는 남겨두기
UN	분석 불능* -> 이거는 한번 보고
W_URL	URL 주소* -> 키워드니까 반드시 제외 / 그래프 분석에서는 활용하는 거로
W_EMAIL	이메일 주소* -> 반드시 제외
W_HASHTAG	해시태그(#abcd)* -> 반드시 제외
W_MENTION	멘션(@abcd)* -> 반드시 제외
'''
remain_dic = {
    'NNG': True,
    'NNP': True,
    'NNB': False,
    'NR': False,
    'NP': False,
    'VV': True,
    'VVI': True,
    'VVR': True, 
    'VA': True,
    'VAI': True,
    'VAR': True, 
    'VX': False,
    'VXI': True,
    'VXR': True, 
    'VCP': False,
    'VCN': False,
    'MM': True,
    'MAG': True,
    'MAJ': False,
    'IC': False,
    'JKS': False, 
    'JKC': False,
    'JKG': False,
    'JKO': False,
    'JKB': False,
    'JKV': False,
    'JKQ': False,
    'JX': False,
    'JC': False,
    'EP': False,
    'EF': False,
    'EC': False,
    'ETN': False,
    'ETM': False,
    'XPN': False,
    'XSN': False,
    'XSV': False,
    'XSA': False,
    'XSAI': False,
    'XSAR': False,
    'XR': False,
    'SF' : False,
    'SP' : False,
    'SS' : False,
    'SE' : False,
    'SO' : False,
    'SW' : True,
    'SL' : True,
    'SH' : True,
    'SN' : True,
    'UN' : True,
    'W_URL' : False,
    'W_EMAIL' : False,
    'W_HASHTAG' : False,
    'W_MENTION' : False,
}

# 단어 : 품사 순으로 구성
stopwords_dict = {
    'ㅉㅉ' : 'SW',
    'ㄹㅇㅋㅋ' : 'SW',
    'ㅋㅋ' : 'SW',
    'ㅅㅂ' : 'SW',
    'ㅈㄹ' : 'SW',
    'ㅁㅊ' : 'SW',
    'ㅗㅗ' : 'SW',
    'ㅡㅡ' : 'SW',
    'ㅜㅜ' : 'SW',
    'ㅠㅠ' : 'SW',
    'ㅎㅎ' : 'SW',
    '왜' : 'MAG',
    'App' : 'SL',
    'dc' : 'SL',
    'DC' : 'SL',
}


def main():
    topic_name = "analyze-keywords"
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[
            "localhost:9092",
        ],
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="keyword-group",
        # value_deserializer=lambda x: loads(x.decode("utf-8")),
        consumer_timeout_ms=1000,
    )
    producer = KafkaProducer(
        acks=0,
        bootstrap_servers=[
            'localhost:9092'
        ],
    )
    print("start")
    
    while True:
        for message in consumer:
            print('==========')

            data = json.loads(message.value.decode('utf-8'))
            print(data)

            data['keywords'] = one_sentence_keyword(data['contents'])
            print(data['keywords'])

            del data['contents']

            producer.send('add-keywords', bytes(json.dumps(data), 'utf-8'))
            producer.flush()


def one_sentence_keyword(_sentence):
    if not _sentence:
        return []
    
    ret = []
    sentence = clean(_sentence)
    print(sentence)
    
    for tok in kiwi.tokenize(sentence, stopwords=stopwords):
        if remain_dic.get(tok.tag):
            # tag는 품사 form은 형태소(글자 그 자체) 
            if len(tok.form) == 1:
                continue
            ret.append(tok.form)
    return ret


if __name__ == "__main__":
    kiwi = Kiwi(num_workers=0, model_path=None, load_default_dict=True, integrate_allomorph=True, model_type='sbg', typos=None, typo_cost_threshold=2.5)
    kiwi.prepare()
    # 품사별 포함 불포함 여부
    stopwords = Stopwords()
    for key, value in stopwords_dict.items():
        stopwords.add((key, value))
    main()
