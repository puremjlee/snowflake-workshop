# ❄️ Snowflake SQL Query Web Application

사용자가 SQL 쿼리를 입력하면 Snowflake에서 결과를 가져와 아름다운 테이블로 표시하는 웹 애플리케이션입니다.

## 📋 필요한 패키지들

### Python 라이브러리 설치
```bash
pip install flask requests PyJWT cryptography
```

또는 requirements 파일 사용:
```bash
pip install -r requirements_webapp.txt
```

#### 패키지 상세 정보
- **Flask>=2.3.0**: 웹 프레임워크
- **requests>=2.31.0**: HTTP 요청 처리
- **PyJWT>=2.8.0**: JWT 토큰 생성
- **cryptography>=41.0.0**: RSA 키 처리 및 암호화

## 🚀 실행 방법

### 1단계: 키페어 생성 (처음 한번만)
```bash
# RSA 키페어 생성
../generate_keypair.sh

# 또는 수동으로:
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

### 2단계: Snowflake에 공개키 등록
```sql
-- Snowflake 웹 콘솔에서 실행
ALTER USER API_USER SET RSA_PUBLIC_KEY='여기에_공개키_내용';
```

### 3단계: 웹 애플리케이션 실행
```bash
python app.py
```

### 4단계: 브라우저에서 접속
```
http://localhost:5000
```

## 📁 프로젝트 파일 구조

```
03.data_endpoint_api/application/
├── app.py                      # Flask 웹 애플리케이션 메인 파일
├── ../jwt_token_generator.py      # JWT 토큰 생성기 (JavaScript 호환)
├── ../generate_keypair.sh         # RSA 키페어 생성 스크립트
├── ../rsa_key.p8                  # RSA 개인키 (생성됨)
├── ../rsa_key.pub                 # RSA 공개키 (생성됨)
├── requirements_webapp.txt     # Python 패키지 의존성
├── templates/
│   └── index.html             # 메인 웹 페이지
└── static/
    └── style.css              # CSS 스타일 파일
```

## ⚙️ 설정 정보

### app.py 설정값 (수정 필요)
```python
# Snowflake 설정
ACCOUNT = "SFSEAPAC-KR_DEMO28"     # 여러분의 Snowflake 계정
USER = "API_USER"                  # 여러분의 Snowflake 사용자
PRIVATE_KEY_FILE = "../rsa_key.p8"  # 개인키 파일 경로
```

### jwt_token_generator.py 설정값
```python
ACCOUNT = "SFSEAPAC-KR_DEMO28"     # app.py와 동일하게
USER = "API_USER"                  # app.py와 동일하게  
PRIVATE_KEY_FILE = "./rsa_key.p8"
```

## 🎯 주요 기능

- **SQL 쿼리 실행**: SELECT 문을 Snowflake에서 실행
- **테이블 결과 표시**: 쿼리 결과를 아름다운 테이블로 표시
- **CSV 내보내기**: 결과를 CSV 파일로 다운로드
- **에러 처리**: 친화적인 에러 메시지
- **반응형 디자인**: 모바일/태블릿 지원
- **실시간 상태 표시**: Snowflake 연결 상태 확인

## 🛡️ 보안 기능

- **JWT 키페어 인증**: 안전한 RSA 기반 인증
- **SQL 인젝션 방지**: SELECT 문만 허용
- **위험한 명령어 차단**: DROP, DELETE, ALTER 등 차단

## 📝 사용 예제

### 기본 쿼리들
```sql
-- 현재 시간과 사용자 확인
SELECT CURRENT_TIMESTAMP() AS 현재시간, CURRENT_USER() AS 사용자;

-- 테이블 목록 조회
SELECT * FROM INFORMATION_SCHEMA.TABLES LIMIT 10;

-- 스키마별 테이블 개수
SELECT TABLE_SCHEMA, COUNT(*) AS 테이블수 
FROM INFORMATION_SCHEMA.TABLES 
GROUP BY TABLE_SCHEMA;
```

## 🚨 문제 해결

### 1. "JWT token is invalid" 에러
```bash
# 새 JWT 토큰 생성
python jwt_token_generator.py

# 출력된 토큰이 정상 작동하는지 확인 후 app.py 재시작
```

### 2. "Module not found" 에러
```bash
# 필요한 패키지 재설치
pip install flask requests PyJWT cryptography
```

### 3. "Private key file not found" 에러
```bash
# 키페어 재생성
./generate_keypair.sh

# Snowflake에 공개키 다시 등록
```

### 4. 웹페이지가 로딩되지 않음
```bash
# 포트 5000이 사용 중인지 확인
lsof -i :5000

# 다른 포트로 실행
python app.py --port=5001
```

## 🔧 고급 설정

### 포트 변경
`app.py` 마지막 줄 수정:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 포트 변경
```

### 운영 환경 배포
```bash
# gunicorn 사용 (운영환경)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📞 지원

문제가 발생하면:
1. **헬스 체크**: `http://localhost:5000/health` 접속
2. **터미널 로그 확인**: Flask 서버 실행 시 나타나는 에러 메시지
3. **JWT 토큰 테스트**: `python jwt_token_generator.py` 실행

## 🎨 커스터마이징

- **UI 색상 변경**: `static/style.css`의 CSS 변수 수정
- **기본 쿼리 변경**: `templates/index.html`의 placeholder 수정
- **웨어하우스 옵션**: `templates/index.html`의 select 옵션 수정

---

🎉 **완성!** 이제 모든 설정이 완료되었습니다!
