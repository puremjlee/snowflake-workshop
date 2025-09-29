#!/usr/bin/env python3
"""
Snowflake JWT 토큰 생성기 (JavaScript 코드 기반)
정상 동작하는 JavaScript 코드와 동일한 방식으로 JWT를 생성합니다.
"""

import json
import base64
import time
import hashlib
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# ===========================================
# 설정값 - 여기만 수정하세요
# ===========================================
ACCOUNT = "SFSEAPAC-KR_DEMO28"     # JavaScript와 동일
USER = "API_USER"                  # JavaScript와 동일
PRIVATE_KEY_FILE = "./rsa_key.p8"
# ===========================================

def base64_encode(data, is_json=True):
    """JavaScript base64Encode 함수와 동일"""
    if is_json:
        text = json.dumps(data, separators=(',', ':'))  # 공백 없이
    else:
        text = data
    
    # base64 인코딩 후 패딩 제거 (JavaScript와 동일)
    if isinstance(text, str):
        text = text.encode('utf-8')
    
    encoded = base64.urlsafe_b64encode(text).decode('utf-8')
    return encoded.rstrip('=')  # 패딩 제거

def generate_jwt_token():
    """JavaScript buildJWT 함수와 동일한 방식으로 JWT 생성"""
    try:
        print("🔧 JavaScript 방식으로 JWT 토큰 생성 중...")
        
        # 1. 개인키 로드
        with open(PRIVATE_KEY_FILE, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        print("✅ 개인키 로드 완료")
        
        # 2. 공개키 지문 생성 (base64 형식으로!)
        public_key_der = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        sha256_hash = hashlib.sha256(public_key_der).digest()  # bytes 형태
        fingerprint_base64 = base64.b64encode(sha256_hash).decode('utf-8')
        print(f"✅ 공개키 지문 (base64): {fingerprint_base64}")
        
        # 3. 시간 처리 (JavaScript와 동일)
        now = int(time.time() * 1000)  # 밀리초
        expires = now + (60 * 60 * 1000)  # 1시간 후
        
        iat = int(now / 1000)      # 초 단위
        exp = int(expires / 1000)  # 초 단위
        
        print(f"✅ IAT: {iat} ({datetime.fromtimestamp(iat)})")
        print(f"✅ EXP: {exp} ({datetime.fromtimestamp(exp)})")
        
        # 4. JWT Header (JavaScript와 동일)
        header = {
            "alg": "RS256",
            "typ": "JWT"
        }
        
        # 5. JWT Payload (JavaScript와 동일)
        issuer = f"{ACCOUNT}.{USER}.SHA256:{fingerprint_base64}"
        subject = f"{ACCOUNT}.{USER}"
        
        payload = {
            "iss": issuer,
            "sub": subject,
            "exp": exp,
            "iat": iat
        }
        
        print(f"✅ Issuer: {issuer}")
        print(f"✅ Subject: {subject}")
        
        # 6. Header와 Payload를 base64 인코딩
        header_encoded = base64_encode(header)
        payload_encoded = base64_encode(payload)
        
        print(f"✅ Header: {header_encoded}")
        print(f"✅ Payload: {payload_encoded}")
        
        # 7. 서명할 데이터 생성
        signing_input = f"{header_encoded}.{payload_encoded}"
        
        # 8. RSA-SHA256 서명 (JavaScript와 동일)
        signature = private_key.sign(
            signing_input.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        # 9. 서명을 base64 인코딩 (패딩 제거)
        signature_encoded = base64_encode(signature, is_json=False)
        
        # 10. 최종 JWT 토큰 조립
        jwt_token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"
        
        print("\n🎯 JavaScript 방식 JWT 토큰:")
        print("=" * 100)
        print(jwt_token)
        print("=" * 100)
        print("💡 이 토큰을 curl 명령어에 사용하세요 (1시간 유효)")
        
        return jwt_token
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_jwt_token(token):
    """생성된 JWT 토큰 테스트"""
    if not token:
        return False
        
    print("\n🧪 JWT 토큰 API 테스트")
    print("-" * 50)
    
    import requests
    
    url = f"https://{ACCOUNT}.snowflakecomputing.com/api/v2/statements"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'X-Snowflake-Authorization-Token-Type': 'KEYPAIR_JWT'
    }
    
    data = {
        'statement': 'SELECT CURRENT_USER() AS user, CURRENT_TIMESTAMP() AS time',
        'warehouse': 'COMPUTE_WH',
        'timeout': 30
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        result = response.json()
        
        print(f"HTTP 상태: {response.status_code}")
        
        if response.status_code == 200 and 'data' in result:
            print("✅ 성공! JWT 토큰이 올바르게 작동합니다!")
            print("📊 쿼리 결과:")
            for row in result['data']:
                print(f"   사용자: {row[0]}")
                print(f"   시간: {row[1]}")
            return True
        else:
            print(f"❌ 실패: {result.get('message', '알 수 없는 에러')}")
            if 'code' in result:
                print(f"   에러 코드: {result['code']}")
            return False
            
    except Exception as e:
        print(f"❌ 네트워크 에러: {e}")
        return False

if __name__ == "__main__":
    print("❄️ Snowflake JWT 생성기 (JavaScript 호환)")
    print("=" * 60)
    
    # JWT 생성
    jwt_token = generate_jwt_token()
    
    if jwt_token:
        # API 테스트
        success = test_jwt_token(jwt_token)
        
        if success:
            print("\n🎉 완벽! 이 JWT 토큰을 사용하세요.")
        else:
            print("\n🤔 JWT 토큰은 생성되었지만 API 테스트는 실패했습니다.")
    else:
        print("\n❌ JWT 토큰 생성에 실패했습니다.")

