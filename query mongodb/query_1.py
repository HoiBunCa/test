from audioop import avg
from statistics import median
from tkinter.messagebox import YES
from pymongo import MongoClient
import json

uri = "mongodb://taeLu5ipu7OhbahZ:thohwoh5Uo2Ohkei@172.16.30.164:27017/?authSource=admin"
myclient = MongoClient(uri)

mydb = myclient["vehicles-crawled"]
mycol = mydb["chotot"]

motorbikebrand_ = {"aprilia","bazan","benelli","bmw","brixton","cr&s","daelim","detech","ducati",
"euro reibel","gpx","halim","hãng khác","harley davidson","honda","hyosung","kawasaki","keeway",
"kengo","ktm","kymco","lambretta","malaguti","moto guzzi","mv agusta","nioshima","norton","peugeot",
"piaggio","rebelusa","regal raptor","royal enfield","sachs","sanda","suzuki","sym","taya","triumph",
"vento","victory","visitor","yamaha"}
# print(type(motorbikebrand_))

# def query_bike_model(motorbikebrand_ : set):
#     tmp_model = []
#     for x in motorbikebrand_:
#         # if x['motorbikebrand_'] :
#             pass

# query_bike_model(motorbikebrand_)

# myquery = { "motorbikebrand": "honda" }
# def query_chotot(finter):
#     mydoc = mycol.find(filter = myquery)


# print(mydoc[1]['area_v2'])



# data = {}

# for brand in mycol.distinct("motorbikebrand", {}):
#     if brand is None:
#         continue
#     print("get brand: ", brand)
#     data[brand] = {}
#     for model in mycol.distinct("motorbikemodel", {"motorbikebrand": brand}):
#         if model is None:
#             continue
#         data[brand][model] = {}
#         for year in mycol.distinct("regdate", {"motorbikebrand": brand, "motorbikemodel": model}):
#             if year is None:
#                 continue
#             data[brand][model][year] = {}
#     break   
# # print(data)

# # dict to json file
# json_object = json.dumps(data, indent = 4)
# print("json ",json_object)
# # save json file
# with open("sample.json", "w") as outfile:
#     json.dump(data, outfile)

# # read json file
# f_json = open("chotot.json")

# # data_chotot = json.load(f_json)

# # for x in data_chotot:
# #     print(x)

# print(f_json)

with open('chotot.json', 'r') as f:
  data = json.load(f)

# for brand, data_brand in data.items():
#     for model, data_model in data_brand.items():
        

# for key in data.keys():
#     value = data[key]
myquery = {}
my_projection = {"price"}
# mydoc = mycol.find(filter = myquery, projection = my_projection)

# for x in mydoc:
#     print(x['price']) 
#     break

# mydoc = mycol.find(filter = myquery)


def statistic_prices(prices):
    # print(prices)
    max_price = max(prices)
    min_price = min(prices)
    count_price = len(prices)
    avg_price = sum(prices)/count_price
    median_price = median(prices)
    return {
        'max': max_price,
        'min': min_price,
        'average': avg_price, 
        'median': median_price,
        'count': count_price
    }

csv_file = open('test.csv', 'w', encoding='utf8')

for brand, data_brand in data.items():
    for model, data_model in data_brand.items():
        for regdate, data_regdate in data_model.items():
            if data[brand][model][regdate]:
                pass
            prices = []
            try:
                regdate = int(regdate)
            except:
                pass
            query = {"motorbikebrand" : brand, "motorbikemodel" : model, "regdate": regdate}
            # print(query)
            prices_resultset = mycol.find(filter=query, projection = {"price"})
            for price in prices_resultset:
                if 'price' not in price:
                    print(price)
                    continue
                prices.append(price['price'])
            if len(prices) == 0:
                continue
            report = statistic_prices(prices)
            # data[brand][model][regdate] = report

            # json_object = json.dumps(data)
            # save json file
            # with open("sample_chotot.json", "w") as outfile:
                # json.dump(data, outfile)
            # print(report)
            line_csv = f'"{brand}","{model}","{regdate}","{report["max"]}","{report["min"]}","{report["count"]}","{report["average"]}","{report["median"]}"\n'
            csv_file.write(line_csv)

csv_file.close()

# dict to json file
json_object = json.dumps(data)
print("json ",json_object)
# save json file
with open("sample_chotot_1.json", "w") as outfile:
    json.dump(data, outfile)



