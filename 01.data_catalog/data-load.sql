
-- create database demo;
-- create schema magi_handson;

use demo.magi_handson;
use warehouse compute_wh; 

// external stage (s3) 생성
CREATE STAGE if not exists ext_stg
URL='s3://sfworkshop-sample-data/';
-- STORAGE_INTEGRATION = myint;

// external stage (s3) 에 위치한 파일확인
ls @ext_stg/data;
-- s3://sfworkshop-sample-data/data/SF_KOSCOM_ETFMST.csv
-- s3://sfworkshop-sample-data/data/SF_KOSCOM_ETF_JITRADE_DAILY.csv
-- s3://sfworkshop-sample-data/data/SF_KOSCOM_ETF_JONG_DAILY.csv
-- s3://sfworkshop-sample-data/data/SF_KOSCOM_ETF_MAST_DAILY.csv

// infer schema 를 위한 파일포맷
create file format csv_format_read 
type=csv
PARSE_HEADER = true;

// 데이터 적재를 위한 파일포맷
create file format csv_format_loading
type=csv
skip_header =1;

// 테이블 생성
CREATE OR REPLACE TABLE SF_KOSCOM_ETF_JITRADE_DAILY
  USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
      INFER_SCHEMA(
        LOCATION => '@ext_stg/data/SF_KOSCOM_ETF_JITRADE_DAILY.csv',
        FILE_FORMAT => 'csv_format_read',
        IGNORE_CASE => true
      )
    )
  );

// 확인
select * from SF_KOSCOM_ETF_JITRADE_DAILY limit 10;

// 적재 
copy into SF_KOSCOM_ETF_JITRADE_DAILY
from @ext_stg/data/SF_KOSCOM_ETF_JITRADE_DAILY.csv
FILE_FORMAT = (FORMAT_NAME = 'csv_format_loading');

----------------------------------------------------------------
// SF_KOSCOM_ETFMST, SF_KOSCOM_ETF_JONG_DAILY.csv 와 SF_KOSCOM_ETF_MAST_DAILY.csv 파일적재해보기

----------------------------------------------------------------
// 적재 확인
show tables;