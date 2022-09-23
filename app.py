from flask import Flask, render_template, request, redirect, url_for
import requests, socket, json

# TODO
# 최종 수정시, 아래 링크로 URL 수정 및 맨 아래 port=35001 로 포트 열기
url = "http://192.168.56.102:30080"
# url = "http://backend-lb:8080"

app = Flask(__name__)

# 메인 화면
@app.route('/')
def main():
    return render_template("/index.html")

# 일기 작성 화면
@app.route('/write')
def write():
    return render_template("/writeDiary.html")

# 일기 업로드
@app.route('/', methods=['post'])
def save():
    # 전달된 값 처리 후 백앤드 서버로 전송
    result = request.form
    diary = {
        'title':result['title'],
        'content':result['content']
    }
    
    print(diary)

    # 백엔드 서버로 전송
    test11 = requests.post(url + '/', json=diary)

    # 데이터 확인
    print('서버 응답 완료')
    print('입력값 확인 : ', test11)
    print('요청 url : ', test11.url)
    print('요청 header : ', test11.headers)   
    print('내용 : ', test11._content)
    print('확인 : ', type(test11.text))
    # print('req 확인 : ', type(test11['data']['seq']))
    
    # 들어오는 값이 str -> json 형식으로 변환 후 원하는 데이터 추출 (seq)
    mySeq = json.loads(test11.text)
    print('두번째 확인 : ', mySeq['data']['seq'])
    
    seq = mySeq['data']['seq']
    
    return redirect('/' + str(seq))

# 일기 전체 목록 날짜 내림차순으로 로드
@app.route('/list')
def list():
    lists = requests.get(url + '/list').json()
    return render_template('/list.html', lists = lists['data']['results'])

# 특정한 일련번호 일기 로드
@app.route('/<seq>')
def detail(seq):
    diarylist = requests.get(url + '/' + seq).json()
    frontHost = socket.gethostname()
    print(socket.gethostname())
    return render_template("/detailView.html",
        seq = seq,
        diary = diarylist['data']['result'],
        frontHost = frontHost)

# 일기 삭제
@app.route('/del/<seq>')
def delDiary(seq):
    # 백엔드 서버로 전송
    delResult = requests.delete(url + '/' + seq)

    print('삭제 확인')
    print('입력값 확인 : ', delResult)
    print('요청 url : ', delResult.url)
    print('요청 header', delResult.headers)
    print('내용 : ', delResult._content)

    # list 화면으로 이동
    return redirect(url_for('list'))

# 모든 외부 접속을 허용함 (포트는 기본 5000)
if __name__ == "__main__":
    app.run(host='0.0.0.0')
