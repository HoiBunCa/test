from config import phone_converter
import pandas as pd
import numpy as np

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

def normalize_data(data):
    all_records = []
    result_all = []
    for phone, df_phone in data.groupby('Phone_84'):
        n = len(df_phone)
        for i, row in df_phone.iterrows():
            for j in range(0, n):
                if j == (n - 1):
                    result = {
                        "Phone": phone,
                        "FullName": row['FullName'],
                        "NationalCard": row['NationalCard'],
                        "LoanBriefId": row['LoanBriefId'],
                        "Gender": row['Gender'],
                        "DOB": row['DOB'],
                        "ProvinceId": row['ProvinceId'],
                        "JobId": row['JobId'],
                        "IsMerried": row['IsMerried'],
                        "NumberBaby": row['NumberBaby'],
                        "LivingWith": row['LivingWith'],
                        "IsSim": row['IsSim'],
                        "ResidentType": row['ResidentType'],
                        "ImcomeType": row['ImcomeType'],
                        "LoanAmountExpertiseAI": row['LoanAmountExpertiseAI'],
                        "bad_momo": row['bad_momo'],
                        "bhxh": row['bhxh'],
                        "pasgo": row['pasgo'],
                        "sendo": row['sendo'],
                        "tiki": row['tiki'],
                        "lotus": row['lotus']
                    }
        all_records.append(result)

    df_result = pd.DataFrame(all_records)

    for phone, df_phone in data.groupby('Phone_84'):
        n = len(df_phone)
        average = 0
        max = 0
        sum = 0
        arr = []

        for i, row in df_phone.iterrows():
            arr.append(row['LoanAmount'])
        sum = np.sum(arr)
        avg = np.average(arr)
        max = np.max(arr)
        result = {
            "Phone": row['Phone_84'],
            "SumLoanAmount": sum,
            "AverageLoanAmount": avg,
            "MaxLoanAmount": max
        }
        result_all.append(result)

    df_result_2 = pd.DataFrame(result_all)

    data_all = pd.merge(df_result, df_result_2, left_on="Phone", right_on="Phone", how="inner")


if __name__ == '__main__':
    # phone = '01664058928'
    # phone = '841664058928'
    # phone = '0364058928'
    # phone = '84364058928'
    # phone = ' 0364058928'
    phone = '+84364058928'

    a = normalize_phone(phone)
    print("Phone before nomalize is: ", phone)
    print("Phone after nomalize is: ", a)
