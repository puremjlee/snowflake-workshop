
use demo.magi_handson;

// 01. data loading 에서 설정한 git integration 사용
CREATE OR REPLACE GIT REPOSITORY snowflake_workshop
API_INTEGRATION = git_api_integration
GIT_CREDENTIALS = git_api_secret
ORIGIN = 'https://github.com/xxxxxxxx/snowflake-workshop.git';