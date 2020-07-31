import sys
import random
import requests

categories_ids = {
    'abarrotes': '5efa4e1e3a39043f733940b1',
    'bebidas': '5efa4e253a39043f733940b2',
    'carnes-aves-y-pescados': '5efa4e173a39043f733940b0',
    'congelados': '5efa4e523a39043f733940b7',
    'cuidado-del-bebe': '5efa4e5a3a39043f733940b8',
    'cuidado-personal': '5efa4e053a39043f733940ae',
    'frutas-y-verduras': '5efa4e0e3a39043f733940af',
    'lacteos-y-huevos': '5efa4dce3a39043f733940ac',
    'limpieza': '5efa4dff3a39043f733940ad',
    'mascotas': '5efa4e343a39043f733940b4',
    'panaderia-pasteleria-y-comidas': '5efa4e2d3a39043f733940b3'
}

def post_request (URI, token, category):
    filepath = f'data/{category}.csv'
    with open(filepath) as f:
        for line in f.readlines()[1:]:
            name, price, content, unitOfMeasurement = line.split(',')
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
            data = { 
                'name': name, 
                'price': price, 
                'content': content,
                'highlight': bool(random.getrandbits(1)), 
                'unitOfMeasurement': unitOfMeasurement.strip(),
                'category': categories_ids[category] 
            }
            print(data)
            res = requests.post(URI, headers=headers, json=data)
            print(res)

def main (token, category):
    with open('url.txt') as f:
        url = f.readline()
    post_request(url, token, category)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        token = sys.argv[1]
        category = sys.argv[2]
        main(token, category)