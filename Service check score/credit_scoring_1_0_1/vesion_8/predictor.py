import datetime
from unittest import result
import joblib
import os
import numpy as np
import requests
from copy import deepcopy
from decimal import *

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

        



