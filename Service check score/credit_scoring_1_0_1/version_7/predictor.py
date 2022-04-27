import datetime
from unittest import result
import joblib
import os
import numpy as np
import requests
from copy import deepcopy
from decimal import *

####################################################
def count_page_like(d):
    n = 0
    for vv in d.values():
        if vv:
            n += 1
    return n


def get_data(Phone, card_number, full_name):
    
    try:
        data = {'phone': Phone, 'card_number': card_number, 'name': full_name, 'is_for_cs': True}
        r = requests.post('http://172.16.30.245:9114/checkHavingInfo', json=data, timeout=5)
        response = r.json()['result']['having_data']
        if response['zalo']:
            if response['zalo_same_name']:
                response['zalo'] = 2
            else:
                response['zalo'] = 1
        else:
            response['zalo'] = 0
        # response['zalo'] = response['zalo_same_name']
        response_clone = deepcopy(response)
        if response_clone['fb']['page_count'] > 0:
            for k, v in response_clone['fb'].items():
                if k == 'page_count':
                    continue
                elif k == 'ecomerce':
                    n = count_page_like(v)
                    response['fb'].update({'ecommerce_count': n})
                elif k == 'phone_store':
                    n = count_page_like(v)
                    response['fb'].update({'electronic_store_count': n})
                elif k == 'reviewer':
                    n = count_page_like(v)
                    response['fb'].update({'electronic_reviewer_count': n})
                elif k == 'vtv':
                    n = count_page_like(v)
                    response['fb'].update({'vtv_count': n})

        elif response['fb']['page_count'] == 0:
            response['fb'].update({'ecommerce_count': 0})
            response['fb'].update({'electronic_store_count': 0})
            response['fb'].update({'electronic_reviewer_count': 0})
            response['fb'].update({'vtv_count': 0})
        else:
            response['fb'].update({'ecommerce_count': -1})
            response['fb'].update({'electronic_store_count': -1})
            response['fb'].update({'electronic_reviewer_count': -1})
            response['fb'].update({'vtv_count': -1})
        try:
            _ = response['msb']
        except:
            response['msb'] = None
        try:
            _ = response['bhxh']
        except:
            response['bhxh'] = None
        try:
            _ = response['tax']
        except:
            response['tax'] = None
        return response
    except:
        # print(traceback.format_exc())
        default_response = {'msb': None,
                             'bhxh': None, 'zalo': None,
                             'momo': None, 'tax': None,
                             'tiki': None, 'pasgo': None,
                             'shopee': None, 'sendo': None,
                             'fb':{
                                 'page_count': -1,
                                 'ecommerce_count': -1,
                                 'electronic_store_count': -1,
                                 'electronic_reviewer_count': -1,
                                 'vtv_count': -1
                             }
                            }
        return default_response

###################################################
# UPPERBOUND_NUMERICAL_FEATURES = {'LoanAmount' : 100e6, 'LoanTime' : 12 * 30,
#                                  'LoanAgain':10, 'NumberOfLoans':10,
#                                  'Salary' : 100e6, 'customer_age' : 70}
UPPERBOUND_NUMERICAL_FEATURES = {'LoanAmount': Decimal(100e6), 'LoanTime': Decimal(12 * 30),
                                 'LoanAgain': Decimal(10), 'NumberOfLoans': Decimal(10),
                                 'Salary': Decimal(100e6), 'customer_age': Decimal(70), 'bad_momo': Decimal(10)}


def encode_hubid(HubId, normalize=True):
    if HubId is None:
        return 0
    else:
        return int(HubId)

def encode_bad_momo(bad_momo, normalize=True):
    if bad_momo is None or str(bad_momo) is str(''):
        return -2
    else:
        return int(bad_momo)

def encode_loan_amount(money, normalize=True):
    if money is None:
        return 0
    if normalize:
        return money / UPPERBOUND_NUMERICAL_FEATURES['LoanAmount']
    else:
        return money


def encode_loan_time(loan_time, normalize=True):
    if loan_time is None:
        return 0
    if normalize:
        return loan_time / UPPERBOUND_NUMERICAL_FEATURES['LoanTime']
    else:
        return loan_time

def encode_salary(salary, normalize=True):
    if salary is None:
        return 0
    if normalize:
        return salary / UPPERBOUND_NUMERICAL_FEATURES['Salary']
    else:
        return salary

def encode_province(value):
    itos = {0: None, 1: 'hà nội', 2: 'hà giang', 4: 'cao bằng', 6: 'bắc kạn', 8: 'tuyên quang', 10: 'lào cai', 11: 'điện biên', 12: 'lai châu', 14: 'sơn la', 15: 'yên bái', 17: 'hòa bình', 19: 'thái nguyên', 20: 'lạng sơn', 22: 'quảng ninh', 24: 'bắc giang', 25: 'phú thọ', 26: 'vĩnh phúc', 27: 'bắc ninh', 30: 'hải dương', 31: 'hải phòng', 33: 'hưng yên', 34: 'thái bình', 35: 'hà nam', 36: 'nam định', 37: 'ninh bình', 38: 'thanh hóa', 40: 'nghệ an', 42: 'hà tĩnh', 44: 'quảng bình', 45: 'quảng trị', 46: 'thừa thiên huế', 48: 'đà nẵng', 49: 'quảng nam', 51: 'quảng ngãi', 52: 'bình định', 54: 'phú yên', 56: 'khánh hòa', 58: 'ninh thuận', 60: 'bình thuận', 62: 'kon tum', 64: 'gia lai', 66: 'đắk lắk', 67: 'đắk nông', 68: 'lâm đồng', 70: 'bình phước', 72: 'tây ninh', 74: 'bình dương', 75: 'đồng nai', 77: 'bà rịa - vũng tàu', 79: 'hồ chí minh', 80: 'long an', 82: 'tiền giang', 83: 'bến tre', 84: 'trà vinh', 86: 'vĩnh long', 87: 'đồng tháp', 89: 'an giang', 91: 'kiên giang', 92: 'cần thơ', 93: 'hậu giang', 94: 'sóc trăng', 95: 'bạc liêu', 96: 'cà mau'}
    stoi = {None:0, 'hà nội': 1, 'hà giang': 2, 'cao bằng': 4, 'bắc kạn': 6, 'tuyên quang': 8, 'lào cai': 10, 'điện biên': 11, 'lai châu': 12, 'sơn la': 14, 'yên bái': 15, 'hòa bình': 17, 'thái nguyên': 19, 'lạng sơn': 20, 'quảng ninh': 22, 'bắc giang': 24, 'phú thọ': 25, 'vĩnh phúc': 26, 'bắc ninh': 27, 'hải dương': 30, 'hải phòng': 31, 'hưng yên': 33, 'thái bình': 34, 'hà nam': 35, 'nam định': 36, 'ninh bình': 37, 'thanh hóa': 38, 'nghệ an': 40, 'hà tĩnh': 42, 'quảng bình': 44, 'quảng trị': 45, 'thừa thiên huế': 46, 'đà nẵng': 48, 'quảng nam': 49, 'quảng ngãi': 51, 'bình định': 52, 'phú yên': 54, 'khánh hòa': 56, 'ninh thuận': 58, 'bình thuận': 60, 'kon tum': 62, 'gia lai': 64, 'đắk lắk': 66, 'đắk nông': 67, 'lâm đồng': 68, 'bình phước': 70, 'tây ninh': 72, 'bình dương': 74, 'đồng nai': 75, 'bà rịa - vũng tàu': 77, 'hồ chí minh': 79, 'long an': 80, 'tiền giang': 82, 'bến tre': 83, 'trà vinh': 84, 'vĩnh long': 86, 'đồng tháp': 87, 'an giang': 89, 'kiên giang': 91, 'cần thơ': 92, 'hậu giang': 93, 'sóc trăng': 94, 'bạc liêu': 95, 'cà mau': 96}
    provinces = {v:i for i, v in enumerate([None, 'hà nội', 'hà giang', 'cao bằng', 'bắc kạn', 'tuyên quang', 'lào cai', 'điện biên', 'lai châu', 'sơn la', 'yên bái', 'hòa bình', 'thái nguyên', 'lạng sơn', 'quảng ninh', 'bắc giang', 'phú thọ', 'vĩnh phúc', 'bắc ninh', 'hải dương', 'hải phòng', 'hưng yên', 'thái bình', 'hà nam', 'nam định', 'ninh bình', 'thanh hóa', 'nghệ an', 'hà tĩnh', 'quảng bình', 'quảng trị', 'thừa thiên huế', 'đà nẵng', 'quảng nam', 'quảng ngãi', 'bình định', 'phú yên', 'khánh hòa', 'ninh thuận', 'bình thuận', 'kon tum', 'gia lai', 'đắk lắk', 'đắk nông', 'lâm đồng', 'bình phước', 'tây ninh', 'bình dương', 'đồng nai', 'bà rịa - vũng tàu', 'hồ chí minh', 'long an', 'tiền giang', 'bến tre', 'trà vinh', 'vĩnh long', 'đồng tháp', 'an giang', 'kiên giang', 'cần thơ', 'hậu giang', 'sóc trăng', 'bạc liêu', 'cà mau'])}
    try:
        p = itos[value]
        idx = provinces[p]
    except:
        try:
            value = value.lower()
            idx = provinces[value]
        except:
            idx = provinces[None]
    v = np.zeros((len(provinces)))
    v[idx] = 1
    return v


# default using one-hot encoding when onehot=True, otherwise using label encoding
def encode_categorical_feature(value, map_table, onehot=True):
    try:
        idx = map_table[value]
    except:
        idx = map_table[None]

    if onehot:
        v = np.zeros((len(map_table)))
        v[idx] = 1
        return v
    else:
        return idx


#############################################################
'''
Encode extra features which are infered from existed features
'''
def encode_salary_level(salary, normalize=True):
    if salary is None:
        return 0
    if salary <= 5e6:
        level = 1
    elif salary <= 1e7:
        level = 2
    elif salary <= 1.8e7:
        level = 3
    elif salary <= 3.2e7:
        level = 4
    elif salary <= 5.2e7:
        level = 5
    elif salary <= 8e7:
        level = 6
    else:
        level = 7
    if normalize:
        return level / 7
    else:
        return level

def encode_age(age, normalize=True):
    if age is None:
        return 0
    if normalize:
        return age / UPPERBOUND_NUMERICAL_FEATURES['customer_age']
    else:
        return age

def encode_jobid(jobid):
    if jobid is None:
        category = 0
    elif jobid in {35, 75, 105, 45, 102, 92, 54, 53, 68, 95, 104, 103, 94, 96, 25, 69, 93, 81, 80, 56, 122, 123, 97, 44,
                   118, 58, 76, 73, 50, 114, 43, 30, 62, 46, 113, 112, 154, 65, 107, 57, 52, 50, 55, 47}:
        category = 1  # nganh nghe on dinh
    elif jobid in {109, 170, 60, 112, 108, 181, 41, 132, 64, 111, 117, 110, 61, 51, 90, 33, 70, 6, 32, 48, 98, 126, 77,
                   22, 101, 36, 49, 24, 115, 66, 87, 88}:
        category = 2  # nganh nghe tu do/ it on dinh
    elif jobid in {37, 124, 100, 99, 10, 31, 26, 38, 59, 29}:
        category = 3  # tu kinh doanh
    elif jobid in {125, 106, 116, 71, 72}:
        category = 4  # xe om cong nghe & shipper
    else:
        category = 5  # khac

    one_hot = [0, 0, 0, 0, 0, 0]
    one_hot[category] = 1
    return one_hot


def encode_numerical_feature(value, normalize=True):
    if value is None:
        return 0
    return value

USING_FB = False
USING_ECOM = False

used_features = [
    {
        'name': 'LoanAmount',
        'type': 'numerical',
        'encoding': encode_loan_amount,
        'normalize': True,
        'used': True
    },
    {
        'name': 'LoanTime',
        'type': 'numerical',
        'encoding': encode_loan_time,
        'normalize': True,
        'used': True
    },
    {
        'name': 'Salary',
        'type': 'numerical',
        'encoding': encode_salary,
        'normalize': True,
        'used': False
    },
    {
        'name': 'customer_age',
        'type': 'numerical',
        'encoding': encode_age,
        'normalize': True,
        'used': True
    }, {
        'name': 'postCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'angryCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'commentCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    },
{
        'name': 'hahaCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    },
    {
        'name': 'likeCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'loveCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'sadCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'shareCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'wowCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'subscriberCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'friendCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'groupCount',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'page_count',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'ecommerce_count',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'electronic_store_count',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'electronic_reviewer_count',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'vtv_count',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': USING_FB
    }, {
        'name': 'num_cac_call',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': False
    }, {
        'name': 'LoanAmountExpertiseAI',
        'type': 'numerical',
        'encoding': encode_numerical_feature,
        'normalize': True,
        'used': True
    }, {
        'name': 'ProvinceId',
        'type': 'categorical',
        'encoding': encode_province,
        'mapping': None,
        'output_size': 64,
        'used': True
    }, {
        'name': 'IsReMarketing',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': True
    }, {
        'name': 'Gender',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, 0: 1, 1: 2},
        'used': True
    }, {
        'name': 'JobId',
        'type': 'categorical',
        'encoding': encode_jobid,
        'mapping': None,
        'output_size': 6,
        'used': True
    }, {
        'name': 'ImcomeType',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
        'used': True
    }, {
        'name': 'IsMerried',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': True
    }, {
        'name': 'LivingWith',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, 0: 0, 1: 1, 2: 2},
        'used': True
    }, {
        'name': 'RateTypeId',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, 1: 1, 6: 2, 7: 3, 8: 4, 10: 5, 13: 6, 14: 7},
        'used': True
    }, {
        'name': 'ProductId',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, 1: 1, 2: 2, 5: 3, 19: 4, 28: 5},
        'used': True
    }, {
        'name': 'schoolTypes',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, "High School": 1, "Graduate School": 2, "College": 3},
        'used': USING_FB
    }, {
        'name': 'RelationshipType',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13,
                    14: 14, 15: 15},
        'used': True
    }, {
        'name': 'RelationshipPhone',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': True
    }, {
        'name': 'ResidentType',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13,
                    13: 14, 14: 15, 15: 16},
        'used': True
    },
    {
        'name': 'msb',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'bhxh',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'tax',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'zalo',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'tiki',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'pasgo',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'shopee',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'sendo',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'telco',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, 'vinaphone': 1, 'viettel': 2, 'mobiphone': 3, 'vietnammobile': 4, 'gmobile': 5},
        'used': True
    }, {
        'name': 'momo',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': USING_ECOM
    }, {
        'name': 'HubId',
        'type': 'numerical',
        'encoding': encode_hubid,
        'normalize': True,
        'used': True
    }, {
        'name': 'bad_momo',
        'type': 'numerical',
        'encoding': encode_bad_momo,
        'normalize': True,
        'used': True
    },
    {
        'name': 'IsHeadOffice',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': True
    }, {
        'name': 'IsLocate',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': True
    }, {
        'name': 'IsReborrow',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': True
    }, {
        'name': 'is_proof_income',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': True
    }, {
        'name': 'is_shk',
        'type': 'categorical',
        'encoding': encode_categorical_feature,
        'mapping': {None: 0, True: 1, False: 2},
        'used': True
    }
]

class Predictor:
    def __init__(self):
        self.model_name = "version 7"
        self.model_ver = "1_0_7"
        self.model_desc = "Model test theo y.c cua anh Thien-97"
        self.model = None

        self.MODEL = {'weights': {'pos': 0.5, 'neg': 0.5},
                      'probs': {'pos': 0.8, 'neg': 0.9},
                      'probs_cfn_certain': {'pos': 0.8, 'neg': 0.9},
                      'probs_cfn': {'pos': 0.65, 'neg': 0.95}}
        self.telco_converter = {'086': 'viettel', '096': 'viettel', '097': 'viettel', '098': 'viettel',
                                '032': 'viettel',
                                '033': 'viettel', '034': 'viettel', '035': 'viettel', '036': 'viettel',
                                '037': 'viettel',
                                '038': 'viettel', '039': 'viettel',
                                '088': 'vinaphone', '091': 'vinaphone', '094': 'vinaphone', '083': 'vinaphone',
                                '084': 'vinaphone', '085': 'vinaphone', '081': 'vinaphone', '082': 'vinaphone',
                                '089': 'mobiphone', '090': 'mobiphone', '093': 'mobiphone', '070': 'mobiphone',
                                '076': 'mobiphone', '077': 'mobiphone', '078': 'mobiphone', '079': 'mobiphone',
                                '092': 'vietnammobile', '056': 'vietnammobile', '058': 'vietnammobile',
                                '099': 'gmobile', '059': 'gmobile', '087': 'viettel', '052': 'vietnammobile'}

    def load_model(self, model_path):
        print('loading %s ...' % model_path)
        if os.path.isfile(model_path):
            self.model = joblib.load(model_path)
            return self.model
        else:
            return None


#############################################################
    # d is a dict of features
    @staticmethod
    def encode(d, normalize=True):
        output = []
        for feature in used_features:
            try:
                if feature['used']:
                    if feature['type'] == 'numerical':
                        output.append(feature['encoding'](d[feature['name']], feature['normalize']))
                    elif feature['type'] == 'categorical':
                        params = [d[feature['name']]]
                        if feature['mapping']:
                            params.append(feature['mapping'])
                        output.extend(feature['encoding'](*params))
                    else:
                        raise Exception('Not found type features')
            except Exception as e:
                raise Exception(f"Failed when encode {feature}: {d[feature['name']]}") from e

        return np.array(output)

############################################################################

    def predict_proba(self, data_inputs):
        X = []
        loanbriefid = []
        for x in data_inputs:
            dob = x["DOB"].year
            # dob = datetime.datetime.strptime(x["DOB"], '%Y-%m-%d').year
            created_time = x["CreatedTime"].split(" ")[0]
            created_time = datetime.datetime.strptime(created_time, '%Y-%m-%d').year
            customer_age = created_time - dob
            loantime = x["LoanTime"] * 360
            mobile_network = (str(x["Phone"])[0:3])
            telco = self.telco_converter[mobile_network]
            x['LoanTime'] = loantime
            x['customer_age'] = customer_age
            x['telco'] = telco
            result = get_data(x["Phone"], x["NationalCard"], x["FullName"])
            x['msb'] = result['msb']
            x['bhxh'] = result['bhxh']
            x['zalo'] = result['zalo']
            x['momo'] = result['momo']
            x['tax'] = result['tax']
            x['sendo'] = result['sendo']
            x['tiki'] = result['tiki']
            x['pasgo'] = result['pasgo']
            x['shopee'] = result['shopee']
            x['page_count'] = result['fb']['page_count']
            x['ecommerce_count'] = result['fb']['ecommerce_count']
            x['electronic_store_count'] = result['fb']['electronic_store_count']
            x['electronic_reviewer_count'] = result['fb']['electronic_reviewer_count']
            x['vtv_count'] = result['fb']['vtv_count']
            x['num_cac_call'] = None
            x['bad_momo'] = 0
            # x['hubid'] = 7024
            # x['isheadoffice'] = False
            # x['islocate'] = False
            # x['isreborrow'] = False
            # x['is_proof_income'] = False
            # x['is_shk'] = False



            loanbriefid.append(x['LoanBriefId'])
            x = self.encode(x)
            X.append(x)
        print("DONE!")
        X = np.array(X)

        y = []
        score = []
        pos_probs = self.model['pos'].predict_proba(X)
        neg_probs = self.model['neg'].predict_proba(X)

        for i in range(len(pos_probs)):
            pos = pos_probs[i]
            neg = neg_probs[i]
            if pos[1] >= self.MODEL['probs']['pos']:
                y.append((1, pos[1], 'pos'))
                score.append({"{str:d}".format(str=loanbriefid[i]): pos[1] * 1000})
            elif neg[0] >= self.MODEL['probs']['neg']:
                y.append((0, neg[0], 'neg'))
                score.append({"{str:d}".format(str=loanbriefid[i]): (1 - neg[0]) * 1000})
            else:
                merge = self.MODEL['weights']['pos'] * pos + self.MODEL['weights']['neg'] * neg
                label = np.argmax(merge)
                if label == 1 and merge[label] >= self.MODEL['probs']['pos']:
                    merge[label] = self.MODEL['probs']['pos']
                elif label == 0 and merge[label] >= self.MODEL['probs']['neg']:
                    merge[label] = self.MODEL['probs']['neg']

                if label == 1 and merge[label] >= self.MODEL['probs_cfn_certain']['pos']:
                    score.append({"{str:d}".format(str=loanbriefid[i]): merge[label] * 1000})
                    y.append((np.argmax(merge), merge[label], 'special_confusion'))
                elif label == 0 and merge[label] >= self.MODEL['probs_cfn_certain']['neg']:
                    score.append({"{str:d}".format(str=loanbriefid[i]): (1 - merge[label]) * 1000})
                    y.append((np.argmax(merge), merge[label], 'special_confusion'))
                else:  # not certain
                    y.append((np.argmax(merge), merge[label], 'confuse'))
                    if np.argmax(merge) == 1:
                        score.append({"{str:d}".format(str=loanbriefid[i]): merge[label] * 1000})
                    else:
                        score.append({"{str:d}".format(str=loanbriefid[i]): (1 - merge[label]) * 1000})
        return score

        





