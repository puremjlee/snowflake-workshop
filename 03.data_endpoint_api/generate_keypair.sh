#!/bin/bash

# ===========================================
# Snowflake RSA 키페어 생성 스크립트
# ===========================================

echo "🔐 Snowflake용 RSA 키페어 생성 중..."

# 개인키 생성 (PKCS#8 형식)
echo "1️⃣ 개인키 생성 중..."
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt

# 공개키 생성  
echo "2️⃣ 공개키 생성 중..."
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub

# 권한 설정
chmod 600 rsa_key.p8
chmod 644 rsa_key.pub

echo "✅ 키페어 생성 완료!"
echo ""
echo "📁 생성된 파일:"
echo "  - rsa_key.p8 (개인키 - 안전하게 보관)"
echo "  - rsa_key.pub (공개키 - Snowflake에 등록)"
echo ""
echo "📋 다음 단계:"
echo "1. 공개키 내용 확인:"
echo "   cat rsa_key.pub"
echo ""
echo "2. Snowflake에서 공개키 등록 (헤더/푸터 제거 후 한줄로):"
echo "   ALTER USER your_username SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG...';"
echo ""
echo "3. JWT 토큰 생성:"
echo "   python jwt_token_generator.py"
echo ""
echo "4. curl로 테스트:"
echo "   ./snowflake_curl.sh"

# 공개키 내용을 Snowflake용으로 변환해서 출력
echo "----------------------------------------"
echo "🔑 Snowflake 등록용 공개키 (복사해서 사용하세요):"
echo "----------------------------------------"
# 헤더/푸터 제거하고 한줄로 만들기
cat rsa_key.pub | grep -v "BEGIN PUBLIC KEY" | grep -v "END PUBLIC KEY" | tr -d '\n'
echo ""
echo "----------------------------------------" 

