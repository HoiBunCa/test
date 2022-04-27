from decimal import *
# PostgreSQL config
POSTGRE_HOST = '172.16.30.245'
POSTGRE_PORT = '5435'
POSTGRE_USER = 'postgres'
POSTGRE_PWD = 'Eet5aish5eeng7gu'
POSTGRE_DB_CREDIT_SCORE = 'credit_score'
POSTGRE_DB_TIMA_SERVICE = 'tima_service'

POSTGRE_TABLE_TRAIN = 'thuatnh_date_08_03_test'
POSTGRE_TABLE_TEST = 'all_appraisal_test_raw'
POSTGRE_TABLE_LOGGING = 'credit_scoring_log'
POSTGRE_TABLE_DAILY_LOAN = 'daily_loan_disbursement'
POSTGRE_TABLE_DAILY_SCORING = 'daily_credit_scoring'
POSTGRE_TABLE_DAILY_SCORING_TRANSFORMER = 'daily_credit_scoring_transformer'

POSTGRES_QUERY_TRAIN = '''
with data as (
    select *,
           row_number() over (PARTITION by "LMS_LoanID") as rn
    from history_loan_enrichment_v2
)
select *
from data hlev2 inner join loan_label ll on hlev2."LMS_LoanID"=ll."ID"
where hlev2.rn = 1
    and label_risk_lv1 is not null
    and "ProductId" in (2, 5, 28)
    and "CreatedTime" >= '2020-06-01'
    and ll."NextDate" < '2021-09-01'
order by "CreatedTime" desc;
'''
POSTGRES_QUERY_TEST = '''
with data as (
    select *,
           row_number() over (PARTITION by "LMS_LoanID") as rn
    from history_loan_enrichment_v2
)
select *
from data hlev2 inner join loan_label ll on hlev2."LMS_LoanID"=ll."ID"
where hlev2.rn = 1
    and label_risk_lv1 is not null
    and hlev2."Salary" is not null
    and "ProductId" in (2, 5, 28)
    and "CreatedTime" >= '2021-09-01'
order by "CreatedTime" desc;
'''

LABEL_KEY = 'label_risk_lv1'


# dictionary convert to normal
phone_converter = {'0120': '070', '0121': '079', '0122': '077', '0126': '076', '0128': '078',
                   '0123': '083', '0124': '084', '0125': '085', '0127': '081', '0129': '082',
                   '0162': '032', '0163': '033', '0164': '034', '0165': '035', '0166': '036',
                   '0167': '037', '0168': '038', '0169': '039',
                   '0186': '056', '0188': '058',
                   '0199': '059'}

