from clean import clean
from sentence_transformers import SentenceTransformer, util

# naive_kiwi_keywords_and_comment의 문장 전체를 넣어준다
# 키워드를 넣어준다.




def sim_vec(model, now_comment, comments):
    '''
    유사도를 비교해서 해당 유사도 벡터를 반환하는 함수
    Args:
        model : sentence bert를 수행하는 모델
        now_comment : 현재 문장
        comments : 비교할 문장들의 집합 # json 을 쓰시면 json 그대로 끌고 오셔도 됩니다!
    Returns:
        문장 유사도를 담은 배열
    '''
    # https://www.sbert.net/ 
    # 쉽게 말해 model.encode 는 parameter로 받은 문자열의 배열을 encode를 하는 과정입니다.
    now_comment_vector = model.encode([now_comment])# 키워드 끼리 띄어쓰기로 결합한 이후에 합쳐준다
    vectors = model.encode([comment for comment in comments])# 키워드 끼리 띄어쓰기로 결합한 이후에 합쳐준다
    similarities = util.cos_sim(now_comment_vector, vectors)
    return similarities
    #print(similarities[1400:1401][1400:1401])


def main():
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
    now_comment = '잠온다 ㅠㅠ'
    comments = ['잠이 옵니다', '졸음이 옵니다', '기차가 옵니다', '잠온다 ㅠㅠ']
    map(comments, clean)
    save_file = sim_vec(model, now_comment, comments)
    print(save_file)