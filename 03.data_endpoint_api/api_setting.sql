
create or replace user api_user;
GRANT ROLE ACCOUNTADMIN TO USER API_USER;
alter user api_user set default_role=accountadmin;


// 새로운 공개키 등록
ALTER USER API_USER SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAxxxxx';

// 등록 확인 
desc user API_USER;

SELECT * FROM demo.magi_handson.market_info where base_dt='2025-07-23' and ITEM_NM_KOR='TIGER 코리아밸류업';


