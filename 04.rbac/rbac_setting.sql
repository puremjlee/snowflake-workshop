use role accountadmin;
use demo.magi_handson;
use warehouse compute_wh;

// 맵핑테이블 생성
CREATE OR REPLACE TABLE mcp_role_mapping (
    mcp_nm_kor VARCHAR,
    role_name VARCHAR
);

// 맵핑테이블 데이터적재
INSERT INTO mcp_role_mapping (mcp_nm_kor, role_name) VALUES
('하나자산운용', 'ROLE_A'),
('삼성자산운용(ETF)', 'ROLE_A'),
('키움투자자산운용', 'ROLE_A'),
('미래에셋자산운용', 'ROLE_A'),
('미래에셋자산운용', 'ROLE_C'),
('미래에셋자산운용', 'ROLE_D'),
('한국투자신탁운용(ETF)', 'ROLE_A'),
('우리자산운용', 'ROLE_A'),
('iM에셋자산운용', 'ROLE_A'),
('iM에셋자산운용', 'ROLE_B'),
('KB자산운용', 'ROLE_A'),
('KB자산운용', 'ROLE_B'),
('KB자산운용', 'ROLE_D'),
('한화자산운용', 'ROLE_A'),
('한화자산운용', 'ROLE_B'),
('교보악사자산운용', 'ROLE_A'),
('교보악사자산운용', 'ROLE_B'),
('흥국자산운용', 'ROLE_A'),
('흥국자산운용', 'ROLE_B'),
('타임폴리오자산운용', 'ROLE_B'),
('타임폴리오자산운용', 'ROLE_C'),
('NH-Amundi자산운용', 'ROLE_B'),
('NH-Amundi자산운용', 'ROLE_C'),
('NH-Amundi자산운용', 'ROLE_D'),
('신한자산운용', 'ROLE_A'),
('신한자산운용', 'ROLE_B'),
('신한자산운용', 'ROLE_C'),
('신한자산운용', 'ROLE_D'),
('DB자산운용', 'ROLE_A'),
('DB자산운용', 'ROLE_B'),
('DB자산운용', 'ROLE_C'),
('DB자산운용', 'ROLE_D'),
('우리자산운용', 'ROLE_B'),
('우리자산운용', 'ROLE_C'),
('우리자산운용', 'ROLE_D'),
('트러스톤자산운용', 'ROLE_B'),
('트러스톤자산운용', 'ROLE_C'),
('IBK자산운용', 'ROLE_B'),
('IBK자산운용', 'ROLE_C');

select * from mcp_role_mapping;

// row access policy 생성
CREATE OR REPLACE ROW ACCESS POLICY mcp_role_mapping_policy
AS (mcp_nm_kor VARCHAR) RETURNS BOOLEAN ->
    EXISTS (
        SELECT 1 FROM mcp_role_mapping
        WHERE mcp_role_mapping.mcp_nm_kor = mcp_nm_kor
        AND (mcp_role_mapping.role_name = CURRENT_ROLE() or CURRENT_ROLE() ='ACCOUNTADMIN')
    );

// row access policy 적용
ALTER TABLE asset_info ADD ROW ACCESS POLICY mcp_role_mapping_policy ON (mcp_nm_kor);
-- alter table asset_info drop ROW ACCESS POLICY mcp_role_mapping_policy ;


// 새로운 custom role 생성
create or replace role role_A;

// db 와 schema 에 대한 접근 권한 할당
grant usage on database demo to role role_A;
grant usage on schema demo.magi_handson to role role_A;

// 스키마 아래 모든 객체에 모든권한
grant all privileges on schema demo.magi_handson to role role_A;

// 모든 테이블에 select 권한
grant select on all tables in schema demo.magi_handson to role role_A;

// 스키마 아래 미래 생성될 테이블에 select 권한
grant select on future tables in schema demo.magi_handson to role role_A;

// warehouse 사용 권한 할당
grant usage on warehouse compute_wh to role role_A;

// 사용자에게 role 할당
grant role role_A to user mjlee; 

// accountadmin role 테스트
use role accountadmin;
select * from asset_info
where mcp_nm_kor = '타임폴리오자산운용';

// role_A 테스트
use role role_a;
select * from asset_info
where mcp_nm_kor = '타임폴리오자산운용';

------------------------------------------------- 
use role accountadmin;

create or replace role role_B;
grant usage on database demo to role role_B;
grant usage on schema demo.magi_handson to role role_B;
grant all privileges on schema demo.magi_handson to role role_B;
grant select on all tables in schema demo.magi_handson to role role_B;
grant select on future tables in schema demo.magi_handson to role role_B;
grant usage on warehouse compute_wh to role role_B;
grant role role_B to user mjlee; 

create or replace role role_C;
grant usage on database demo to role role_C;
grant usage on schema demo.magi_handson to role role_C;
grant all privileges on schema demo.magi_handson to role role_C;
grant select on all tables in schema demo.magi_handson to role role_C;
grant select on future tables in schema demo.magi_handson to role role_C;
grant usage on warehouse compute_wh to role role_C;
grant role role_C to user mjlee; 

create or replace role role_D;
grant usage on database demo to role role_D;
grant usage on schema demo.magi_handson to role role_D;
grant all privileges on schema demo.magi_handson to role role_D;
grant select on all tables in schema demo.magi_handson to role role_D;
grant select on future tables in schema demo.magi_handson to role role_D;
grant usage on warehouse compute_wh to role role_D;
grant role role_D to user mjlee; 


// accountadmin role 테스트
use role accountadmin;
select count(*) from asset_info;

// role_A 테스트
use role role_a;
select count(*) from asset_info;

// role_B 테스트
use role role_b;
select count(*) from asset_info;

// role_C 테스트
use role role_c;
select count(*) from asset_info;

// role_D 테스트
use role role_d;
select count(*) from asset_info;




