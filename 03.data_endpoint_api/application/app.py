#!/usr/bin/env python3
"""
Snowflake SQL Query Web Application
사용자가 SQL을 입력하면 Snowflake에서 결과를 가져와 테이블로 표시하는 웹앱
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
import json
import base64
import time
import hashlib
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import requests
import os

# Flask 앱 설정
app = Flask(__name__)
app.config['SECRET_KEY'] = 'snowflake-query-app-secret-key'

# Snowflake 설정 (jwt_token_generator.py와 동일)
ACCOUNT = "SFSEAPAC-KR_DEMO28"
USER = "API_USER"
PRIVATE_KEY_FILE = "../rsa_key.p8"
SNOWFLAKE_API_URL = f"https://{ACCOUNT}.snowflakecomputing.com/api/v2/statements"

def base64_encode(data, is_json=True):
    """JavaScript base64Encode 함수와 동일"""
    if is_json:
        text = json.dumps(data, separators=(',', ':'))
    else:
        text = data
    
    if isinstance(text, str):
        text = text.encode('utf-8')
    
    encoded = base64.urlsafe_b64encode(text).decode('utf-8')
    return encoded.rstrip('=')

def generate_jwt_token():
    """JWT 토큰 생성 (jwt_token_generator.py와 동일)"""
    try:
        # 개인키 로드
        with open(PRIVATE_KEY_FILE, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        
        # 공개키 지문 생성 (base64)
        public_key_der = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        sha256_hash = hashlib.sha256(public_key_der).digest()
        fingerprint_base64 = base64.b64encode(sha256_hash).decode('utf-8')
        
        # 시간 처리
        now = int(time.time() * 1000)
        expires = now + (60 * 60 * 1000)  # 1시간
        
        iat = int(now / 1000)
        exp = int(expires / 1000)
        
        # JWT Header
        header = {"alg": "RS256", "typ": "JWT"}
        
        # JWT Payload
        issuer = f"{ACCOUNT}.{USER}.SHA256:{fingerprint_base64}"
        subject = f"{ACCOUNT}.{USER}"
        
        payload = {
            "iss": issuer,
            "sub": subject,
            "exp": exp,
            "iat": iat
        }
        
        # Header와 Payload 인코딩
        header_encoded = base64_encode(header)
        payload_encoded = base64_encode(payload)
        
        # 서명 생성
        signing_input = f"{header_encoded}.{payload_encoded}"
        signature = private_key.sign(
            signing_input.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        signature_encoded = base64_encode(signature, is_json=False)
        
        # JWT 토큰 조립
        jwt_token = f"{header_encoded}.{payload_encoded}.{signature_encoded}"
        
        return jwt_token
        
    except Exception as e:
        print(f"JWT 생성 에러: {e}")
        return None

def execute_snowflake_query(sql, warehouse="COMPUTE_WH"):
    """Snowflake에 SQL 쿼리 실행"""
    try:
        # JWT 토큰 생성
        jwt_token = generate_jwt_token()
        if not jwt_token:
            return {"error": "JWT 토큰 생성 실패"}
        
        # API 요청
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
            'X-Snowflake-Authorization-Token-Type': 'KEYPAIR_JWT'
        }
        
        data = {
            'statement': sql,
            'warehouse': warehouse,
            'timeout': 120
        }
        
        response = requests.post(SNOWFLAKE_API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # 결과 데이터 가공
            if 'data' in result and 'resultSetMetaData' in result:
                columns = [col['name'] for col in result['resultSetMetaData']['rowType']]
                rows = result['data']
                
                return {
                    "success": True,
                    "columns": columns,
                    "rows": rows,
                    "row_count": len(rows),
                    "execution_time": result.get('statementHandle', 'N/A')
                }
            else:
                return {
                    "success": True,
                    "columns": [],
                    "rows": [],
                    "row_count": 0,
                    "message": "쿼리가 성공했지만 결과 데이터가 없습니다."
                }
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            return {
                "error": error_data.get('message', f'HTTP {response.status_code} 에러'),
                "code": error_data.get('code', response.status_code)
            }
            
    except requests.exceptions.Timeout:
        return {"error": "요청 시간 초과 (30초)"}
    except requests.exceptions.ConnectionError:
        return {"error": "Snowflake 서버 연결 실패"}
    except Exception as e:
        return {"error": f"예상치 못한 에러: {str(e)}"}

# 라우트 정의
@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query_api():
    """SQL 쿼리 API 엔드포인트"""
    try:
        data = request.get_json()
        
        if not data or 'sql' not in data:
            return jsonify({"error": "SQL 쿼리가 필요합니다"}), 400
        
        sql = data['sql'].strip()
        warehouse = data.get('warehouse', 'COMPUTE_WH')
        
        if not sql:
            return jsonify({"error": "SQL 쿼리가 비어있습니다"}), 400
        
        # 위험한 SQL 명령어 체크 (기본적인 보안)
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE']
        sql_upper = sql.upper()
        
        for keyword in dangerous_keywords:
            if sql_upper.strip().startswith(keyword):
                return jsonify({
                    "error": f"보안상 {keyword} 명령어는 허용되지 않습니다. SELECT 쿼리만 사용해주세요."
                }), 403
        
        # Snowflake 쿼리 실행
        result = execute_snowflake_query(sql, warehouse)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"서버 에러: {str(e)}"}), 500

@app.route('/health')
def health():
    """헬스 체크"""
    try:
        # JWT 토큰 생성 테스트
        token = generate_jwt_token()
        return jsonify({
            "status": "healthy",
            "jwt_generated": bool(token),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "페이지를 찾을 수 없습니다"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "내부 서버 에러"}), 500

if __name__ == '__main__':
    # 템플릿 디렉토리 확인
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("🚀 Snowflake SQL Query Web App 시작!")
    print("📊 브라우저에서 http://localhost:5000 으로 접속하세요")
    print("💡 Ctrl+C로 종료할 수 있습니다")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
