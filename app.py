# -*- coding: utf-8 -*- # 이 파일이 UTF-8 인코딩으로 작성되었음을 명시합니다. 한글 처리를 위해 중요합니다.

from flask import Flask, request # Flask 웹 프레임워크와 클라이언트의 요청 정보를 다루는 request 객체를 가져옵니다.
from RedisClusterClient import RedisClient # Redis 클러스터와 통신하는 기능을 제공하는 사용자 정의 모듈에서 RedisClient 클래스를 가져옵니다.
from EmlServer import EmlServer # 이메일 발송 기능을 제공하는 사용자 정의 모듈에서 EmlServer 클래스를 가져옵니다.
import LoggerFactory # 로깅(로그 기록) 기능을 제공하는 사용자 정의 모듈을 가져옵니다.
import random # 난수(무작위 숫자)를 생성하는 데 사용되는 파이썬 기본 모듈입니다.
import string # 문자열 상수(예: 숫자 '0123456789', 소문자 알파벳 등)를 제공하는 파이썬 기본 모듈입니다.
import datetime # 날짜 및 시간 관련 기능을 제공하는 파이썬 기본 모듈입니다.
# I will use mysql instead of mssql
import pymysql # MySQL 데이터베이스와 연동하기 위한 라이브러리입니다.

app = Flask(__name__) # Flask 애플리케이션 객체를 생성합니다. 웹 서버의 중심 역할을 합니다. '__name__'은 현재 스크립트의 이름을 나타냅니다.
redisClient = RedisClient() # RedisClient 클래스의 인스턴스를 생성합니다. 이 객체를 통해 Redis와 통신할 수 있습니다.
logger = LoggerFactory.loggerFactory() # LoggerFactory 모듈의 loggerFactory 함수를 호출하여 로거 객체를 생성합니다. 프로그램 실행 중 정보를 기록할 때 사용합니다.

@app.route('/') # 웹 주소의 가장 기본 경로인 '/' (루트 경로)로 클라이언트의 요청이 왔을 때 아래 함수를 실행하도록 연결(라우팅)합니다.
def home(): # '/' 경로 요청을 처리하는 'home' 함수를 정의합니다.
    return 'Hello, World' # 클라이언트(웹 브라우저 등)에게 'Hello, World'라는 문자열을 응답으로 보냅니다.

# 고객문의 답변 이메일 발송 기능을 처리하는 엔드포인트입니다.
@app.route('/qnaReplyMail', methods=['POST']) # '/qnaReplyMail' 경로로 'POST' 방식의 HTTP 요청이 왔을 때 아래 함수를 실행합니다.
def qnaReplyMailStart(): # '/qnaReplyMail' POST 요청을 처리하는 'qnaReplyMailStart' 함수를 정의합니다.
    logger.info("/qnaReplyMail 요청 시작") # 로거를 사용하여 정보성 메시지를 기록합니다. 요청이 시작되었음을 알립니다.
    params = request.get_json() # 클라이언트가 POST 요청과 함께 보낸 JSON 형태의 데이터를 파이썬 딕셔너리로 변환하여 'params' 변수에 저장합니다.
    idx = params['idx'] # 'params' 딕셔너리에서 'idx' 키에 해당하는 값을 가져와 'idx' 변수에 저장합니다.
    conn = None # 데이터베이스 연결 객체를 저장할 변수를 초기화합니다. 연결 실패 시 None 상태를 유지합니다.
    try: # 데이터베이스 연결, 쿼리 실행, 이메일 발송 등 오류가 발생할 수 있는 코드를 try 블록 안에 작성합니다.
        # MSSQL 데이터베이스에 연결합니다.
        # 주의: 데이터베이스 서버 주소, 포트, 사용자 이름, 비밀번호, 데이터베이스 이름이 코드에 직접 노출되어 있어 보안상 매우 위험합니다.
        conn = pymysql.connect(server="homejdh.iptime.org:9002", user='root', password='fldeldehdgn1!', database='travelPlaner',charset='utf8mb4')
        cursor = conn.cursor() # 데이터베이스에서 SQL 명령을 실행하고 결과를 가져오기 위한 커서(cursor) 객체를 생성합니다.

        # 실행할 SQL 쿼리 문자열을 정의합니다.
        # 주의: 'idx' 변수의 값을 SQL 문자열 안에 직접 합치고 있습니다. 이는 SQL Injection 공격에 취약한 패턴입니다.
        # 파라미터 바인딩 기능을 사용해야 안전합니다.
        # how can i use parameter binding?
        # 파라미터 바인딩을 사용하려면 SQL 쿼리 문자열에 '?' 또는 '%s'와 같은 플레이스홀더를 사용하고, execute 메소드의 두 번째 인자로 값을 전달합니다.
        # please show me example
        # 예를 들어, cursor.execute("SELECT * FROM table WHERE id = %s", (idx,))와 같이 사용합니다.
        cursor.execute("select * from TRIP WHERE ID = %s", (idx,)) # 정의된 SQL 쿼리를 데이터베이스에서 실행합니다.
        row = cursor.fetchone() # 실행 결과에서 첫 번째 행(row)의 데이터를 가져옵니다.
        # 가져온 데이터(row)에서 필요한 값들을 추출하고, CONTENT와 RESPONSE 필드의 캐리지 리턴(\r) 문자를 HTML 줄바꿈 태그(<br>)로 바꾼 후 리스트 'data'에 저장합니다. 마지막에 요청받은 idx도 추가합니다.
        print(row)
        # row[0] : ID, row[1] : NAME, row[2] : EMAIL, row[3] : CONTENT, row[4] : RESPONSE, row[5] : REGDATE, row[6] : STATUS
        data = [row[0], row[1], row[2], row[3].replace('\r','<br>'), row[4],row[5].replace('\r','<br>'), row[6], idx]
        conn.close() # 데이터베이스 연결을 닫습니다.

        smtpClient = EmlServer() # 이메일 발송 기능을 담당하는 EmlServer 클래스의 인스턴스를 생성합니다.
        result = smtpClient.sendMail_qnaReply(data) # EmlServer 객체의 sendMail_qnaReply 메소드를 호출하여 실제 이메일을 발송합니다. 발송 결과를 'result'에 저장합니다.
    except Exception as ex: # try 블록 안에서 Exception (모든 종류의 오류)이 발생하면 이 블록을 실행합니다.
        # if conn: conn.close() # 오류 발생 시 데이터베이스 연결이 열려 있다면 닫는 로직이 필요할 수 있습니다. (현재 코드는 성공 시 try에서 닫고 있습니다.)
        print(ex) # 발생한 오류 내용을 콘솔에 출력합니다. (운영 환경에서는 로그 시스템 사용 권장)
        result = 'fail' # 오류가 발생했으므로 결과 값을 'fail'로 설정합니다.
    return result # 이메일 발송 결과 ('success' 또는 'fail')를 클라이언트에게 응답으로 반환합니다.

# 이메일 발송 및 레디스 저장을 처리하는 엔드포인트입니다. (회원가입/정보수정 인증 등)
# gubun : 회원가입/정보수정 구분 값 (join/modMember)
@app.route('/sendMail/<gubun>', methods=['POST']) # '/sendMail/' 뒤에 오는 <gubun> 값을 변수로 받아, 'POST' 요청이 왔을 때 아래 함수를 실행합니다.
def send(gubun): # URL에서 추출된 <gubun> 값이 'gubun' 변수로 전달됩니다.
    if not (gubun == 'join' or gubun == 'modMember'): # 'gubun' 값이 'join' 또는 'modMember' 둘 다 아닐 경우
        return 'error' # 'error'라는 문자열을 응답으로 보내고 함수 실행을 종료합니다.
    try: # 오류 처리를 위한 try 블록을 시작합니다.
        params = request.get_json() # 클라이언트의 JSON 요청 데이터를 가져옵니다.
        email = params['email'] # JSON 데이터에서 'email' 값을 가져옵니다.
        authNumber = make_random_code(6) # 6자리의 랜덤 숫자 인증 번호를 생성합니다.
        # Redis에 이메일(email)을 키(Key)로, 생성한 인증 번호(authNumber)를 값(Value)으로 저장합니다.
        # 유효 시간은 datetime.timedelta(hours=1)로 설정하여 1시간 후에 자동 삭제되도록 합니다.
        result = redisClient.setValue(email, authNumber, datetime.timedelta(hours=1))
        if result == 'success': # Redis 저장이 성공했다면
            smtpClient = EmlServer() # 이메일 발송을 위한 EmlServer 객체를 생성합니다.
            result = smtpClient.sendMail(gubun, authNumber, email) # EmlServer의 sendMail 메소드를 호출하여 이메일을 발송합니다. gubun 값에 따라 다른 내용의 이메일이 발송될 수 있습니다.
            if result == 'fail': # 이메일 발송이 실패했다면
                redisClient.delValue(email) # Redis에 저장했던 인증 번호를 삭제하여 불필요한 데이터나 인증 오류를 방지합니다.
    except Exception as ex: # try 블록 안에서 오류 발생 시
        # if 'email' in locals(): redisClient.delValue(email) # 오류 발생 시 email 변수가 존재하면 Redis 삭제 시도 (params 파싱 오류 시 email 변수 없을 수 있음) - 개선 필요
        logger.debug("SEND EMAIL & SET REDIS ERROR : {e}".format(e=ex)) # 발생한 오류 내용을 디버그 레벨로 로깅합니다. 오류 내용을 {e} 위치에 삽입합니다.
        result = 'fail' # 오류 발생 시 결과 값을 'fail'로 설정합니다.
    return result # 이메일 발송 및 Redis 저장 결과('success' 또는 'fail')를 응답으로 반환합니다.

# 인증번호 확인 기능을 처리하는 엔드포인트입니다.
@app.route('/chkValid', methods=['POST']) # '/chkValid' 경로로 'POST' 요청이 왔을 때 아래 함수를 실행합니다.
def chkValid(): # '/chkValid' POST 요청을 처리하는 'chkValid' 함수를 정의합니다.
    try: # 오류 처리를 위한 try 블록을 시작합니다. (주로 JSON 파싱 오류 등을 대비)
        params = request.get_json() # 클라이언트의 JSON 요청 데이터를 가져옵니다.
        email = params['email'] # JSON 데이터에서 'email' 값을 가져옵니다.
        authNumber = params['authNumber'] # JSON 데이터에서 'authNumber' (클라이언트가 입력한 인증 번호) 값을 가져옵니다.
        result = redisClient.getValue(email) # Redis에서 이메일(email)을 키로 저장된 값(서버가 발송했던 인증 번호)을 가져옵니다.

        if result: # Redis에 해당 이메일로 저장된 값이 있다면 (즉, 이메일 인증 유효 시간이 아직 남았고 값이 존재한다면)
            if authNumber == result: # 클라이언트가 보낸 authNumber와 Redis에서 가져온 result(서버가 저장했던 인증 번호)가 같다면
                logger.info("EMAIL AUTH NUMBER CHECK :: SUCCESS :: email={e}, request={a}, result={r}".format(e=email, a=authNumber, r=result)) # 인증 성공 상세 로그를 남깁니다.
                return 'success' # 'success'라는 응답을 반환합니다.
            else: # 클라이언트가 보낸 인증 번호와 Redis 값이 다르다면
                logger.info("EMAIL AUTH NUMBER CHECK :: FAIL :: email={e}, request={a}, result={r}".format(e=email, a=authNumber, r=result)) # 인증 실패 상세 로그를 남깁니다.
                return 'fail' # 'fail'이라는 응답을 반환합니다.
        else: # Redis에 해당 이메일로 저장된 값이 없다면 (키가 존재하지 않거나 만료되어서 삭제되었다면)
            logger.info("EMAIL AUTH NUMBER CHECK :: EXPIRED :: {e}".format(e=email)) # 인증 번호가 만료되었거나 존재하지 않음을 알리는 로그를 남깁니다.
            return 'expired' # 'expired'라는 응답을 반환합니다.
    except Exception as ex: # try 블록 안에서 (예: JSON 파싱) 오류 발생 시
        logger.error('NO REQUEST DATA :: {e}'.format(e=ex)) # 오류 내용을 에러 레벨로 로깅합니다.
        return 'no parameter' # 'no parameter'라는 응답을 반환합니다. (요청 데이터 문제임을 암시)

# 지정된 길이의 랜덤한 숫자 문자열을 생성하는 함수입니다.
def make_random_code(len): # 'make_random_code' 함수를 정의하고 생성할 코드의 길이 'len'을 인자로 받습니다.
    num = string.digits # '0123456789' 문자열을 'num' 변수에 저장합니다.
    temp = random.sample(num, len) # 'num' 문자열에서 중복 없이(sample) 'len' 개수의 문자를 무작위로 선택하여 리스트 'temp'에 저장합니다.
    authNumber = "".join(temp) # 리스트 'temp'에 있는 문자들을 모두 합쳐 하나의 문자열로 만듭니다.
    return authNumber # 완성된 랜덤 인증 번호 문자열을 반환합니다.

# 이 파이썬 스크립트가 직접 실행될 때 아래 코드를 실행합니다. (다른 파일에서 import될 때는 실행되지 않음)
if __name__ == '__main__':
    # Flask 웹 서버를 시작합니다.
    # '0.0.0.0': 서버가 모든 사용 가능한 네트워크 인터페이스의 IP 주소에서 접속을 허용하도록 설정합니다. (외부 접속 허용 시 사용)
    # port=5000: 5000번 TCP 포트로 클라이언트의 요청을 받습니다.
    # debug=False: 디버그 모드를 비활성화합니다. 운영 환경에서는 반드시 False로 설정해야 합니다. (True 시 상세 오류 노출 및 코드 변경 시 자동 재시작 기능)
    # macOS の AirPlay Receiver がポート5000を使用するため5001を使う。
    app.run('0.0.0.0', port=5002, debug=False)

