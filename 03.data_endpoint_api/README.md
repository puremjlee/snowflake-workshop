## 03. 데이터 엔드포인트 API

### 3-1. api_user 생성 
```sql
api_setting.sql 참조
```

### 3-2. keypair 생성
``` baxh
./generate_keypair.sh 
```

### 3-3. api_user 의 public key 업데이트 
```sql
api_setting.sql 참조
```

### 3-4. jwt 토큰생성
- jwt_token_generator.py 에서 ACCOUNT, USER, PRIVATE_KEY_FILE 정보 수정
- ACCOUNT 정보 확인은 화면 좌측 하단 사용자이름 클릭-> Account 에 마우스 오버 -> View account detail -> Account identifier 사용 
``` baxh
python jwt_token_generator.py
```

### 3-5. 쿼리실행요청
- snowflake_curl.sh 에서 ACCOUNT 정보 수정
- snowflake_curl.sh 에서 JWT_TOKEN 값을 3-4 의 토큰 값으로 수정

```bash
./snowflake_curl.sh 실행
```
