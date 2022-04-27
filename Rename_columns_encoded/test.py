from re import S
import utils
import features_encoding as fe
import pandas as pd
data = utils.load("data/training_raw_data.pkl")

# names = ['LoanAmount_1', 'LoanTime_1', 'Salary_1', 'customer_age_1', 'LoanAmountExpertiseAI_1', 'ProvinceId_1', 'ProvinceId_2', 'ProvinceId_3', 'ProvinceId_4', 'ProvinceId_5', 'ProvinceId_6', 'ProvinceId_7', 'ProvinceId_8', 'ProvinceId_9', 'ProvinceId_10', 'ProvinceId_11', 'ProvinceId_12', 'ProvinceId_13', 'ProvinceId_14', 'ProvinceId_15', 'ProvinceId_16', 'ProvinceId_17', 'ProvinceId_18', 'ProvinceId_19', 'ProvinceId_20', 'ProvinceId_21', 'ProvinceId_22', 'ProvinceId_23', 'ProvinceId_24', 'ProvinceId_25', 'ProvinceId_26', 'ProvinceId_27', 'ProvinceId_28', 'ProvinceId_29', 'ProvinceId_30', 'ProvinceId_31', 'ProvinceId_32', 'ProvinceId_33', 'ProvinceId_34', 'ProvinceId_35', 'ProvinceId_36', 'ProvinceId_37', 'ProvinceId_38', 'ProvinceId_39', 'ProvinceId_40', 'ProvinceId_41', 'ProvinceId_42', 'ProvinceId_43', 'ProvinceId_44', 'ProvinceId_45', 'ProvinceId_46', 'ProvinceId_47', 'ProvinceId_48', 'ProvinceId_49', 'ProvinceId_50', 'ProvinceId_51', 'ProvinceId_52', 'ProvinceId_53', 'ProvinceId_54', 'ProvinceId_55', 'ProvinceId_56', 'ProvinceId_57', 'ProvinceId_58', 'ProvinceId_59', 'ProvinceId_60', 'ProvinceId_61', 'ProvinceId_62', 'ProvinceId_63', 'ProvinceId_64', 'IsReMarketing_1', 'IsReMarketing_2', 'IsReMarketing_3', 'Gender_1', 'Gender_2', 'Gender_3', 'JobId_1', 'JobId_2', 'JobId_3', 'JobId_4', 'JobId_5', 'JobId_6',
#          'ImcomeType_1', 'ImcomeType_2', 'ImcomeType_3', 'ImcomeType_4', 'ImcomeType_5', 'ImcomeType_6', 'ImcomeType_7', 'IsMerried_1', 'IsMerried_2', 'IsMerried_3', 'LivingWith_1', 'LivingWith_2', 'LivingWith_3', 'LivingWith_4',
#          'RateTypeId_1', 'RateTypeId_2', 'RateTypeId_3', 'RateTypeId_4', 'RateTypeId_5', 'RateTypeId_6', 'RateTypeId_7', 'RateTypeId_8', 'ProductId_1', 'ProductId_2', 'ProductId_3', 'ProductId_4', 'ProductId_5', 'ProductId_6', 'RelationshipType_1', 'RelationshipType_2', 'RelationshipType_3', 'RelationshipType_4', 'RelationshipType_5', 'RelationshipType_6', 'RelationshipType_7', 'RelationshipType_8', 'RelationshipType_9', 'RelationshipType_10', 'RelationshipType_11', 'RelationshipType_12', 'RelationshipType_13', 'RelationshipType_14', 'RelationshipType_15', 'RelationshipType_16', 'ResidentType_1', 'ResidentType_2', 'ResidentType_3', 'ResidentType_4', 'ResidentType_5', 'ResidentType_6', 'ResidentType_7', 'ResidentType_8', 'ResidentType_9', 'ResidentType_10', 'ResidentType_11', 'ResidentType_12', 'ResidentType_13', 'ResidentType_14', 'ResidentType_15', 'ResidentType_16', 'ResidentType_17', 'telco_1', 'telco_2', 'telco_3', 'telco_4', 'telco_5', 'telco_6', 'HubId_1', 'bad_momo_1', 'IsHeadOffice_1', 'IsHeadOffice_2', 'IsHeadOffice_3', 'IsLocate_1', 'IsLocate_2', 'IsLocate_3', 'is_shk_1', 'is_shk_2', 'is_shk_3']


df = pd.DataFrame(data)
# df.columns = ['label']

df.to_csv("training_raw_data.csv", index=False)


def returnListFeatureNames():
    feature_names, feature_indices = fe.get_feature_index()
    arr_name = []
    for k, v in zip(feature_names, feature_indices):
        for j in range(1,  v[1] - v[0] + 1):
            arr_name.append(k + "_" + str(j))
        print(k, v[1] - v[0], v)
    return arr_name


# if __name__ == '__main__':
#     a = returnListFeatureNames()
#     print(a)
