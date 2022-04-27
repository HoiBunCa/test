import pandas as pd
import missingno as msno

# dictionary convert to normal
phone_converter = {'0120': '070', '0121': '079', '0122': '077', '0126': '076', '0128': '078',
                   '0123': '083', '0124': '084', '0125': '085', '0127': '081', '0129': '082',
                   '0162': '032', '0163': '033', '0164': '034', '0165': '035', '0166': '036',
                   '0167': '037', '0168': '038', '0169': '039',
                   '0186': '056', '0188': '058',
                   '0199': '059'}

def normalize_phone(phone):
    head_84 = '84'
    try:
        if phone[0:1] == ' ' or phone[0:1] == '+':
            phone = phone[1:]
        if phone[0:2] == '84':
            phone = '0' + phone[2:]
        if phone[0:2] == '01':
            head_0 = phone_converter[phone[:4]]
            phone = head_0 + phone[4:]  # return phone with 10 numbers, and header is 0!
            # convert to 84
        if phone[0:1] == '0':
            phone = head_84 + phone[1:]
        return phone
    except:
        return phone


# df_3 = pd.read_csv('history_loan_enrichment_v2_202204071601.csv', header=0, dtype={"LoanBriefId": str, 'Phone': str, "NationalCard":str})

# df_join_1 = pd.read_csv('Customer_add_district_infomation.csv', header=0, dtype={"LoanBriefId": str, 'Phone': str, "NationalCard":str})

# n = len(df_3)

# for i in range(0, n):
#     df_3['Phone'][i] = normalize_phone(df_3['Phone'][i])
#     print("df_3 processed to {} in {} ==> {}". format(i, n, df_3['Phone'][i]))

# df_3.to_csv('df_3.csv')

# ##
# m = len(df_join_1)

# for i in range(0, m):
#     df_join_1['Phone'][i] = normalize_phone(df_join_1['Phone'][i])
#     print("df_3 processed to {} in {} ==> {}". format(i, m, df_join_1['Phone'][i]))

# df_join_1.to_csv('df_join_1.csv')


# df_3 = pd.read_csv('df_3.csv', header=0, dtype={"LoanBriefId": str, 'Phone': str, "NationalCard":str})

# df_join_1 = pd.read_csv('df_join_1.csv', header=0, dtype={"LoanBriefId": str, 'Phone': str, "NationalCard":str})

# df_join_2 = pd.merge(df_3, df_join_1, left_on='Phone', right_on = 'Phone', how = 'left')

# df_join_2.to_csv('df_join_2.csv')

df_join_2 = pd.read_csv('df_join_2.csv', header=0, dtype={"LoanBriefId": str, 'Phone': str, "NationalCard":str})

print(df_join_2.columns)


features = ['LoanBriefId', 'ProductId', 'RateTypeId', 'FullName_x', 'Phone', 'DOB_x', 'Gender_x', 'NationalCard_x', 'LoanAmount', 'LoanAmountExpertiseAI', 'LoanTime', 'FromDate', 'ProvinceId', 'CreatedTime'
            , 'HubId', 'JobId_x', 'IsMerried_x', 'NumberBaby_x', 'Salary_x', 'LivingWith', 'ImcomeType', 'RelationshipType', 'bad_momo', 'IsReMarketing', 'ResidentType', 'IsHeadOffice', 'IsLocate', 'IsReborrow', 'is_proof_income',
            'is_shk', 'Population', 'Area', 'PopulationDensity']

final_data = df_join_2[features]

final_data.to_csv('final_data.csv')