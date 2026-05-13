import requests

x = 1
for i in range(x, x+5):
    response = requests.post("http://127.0.0.1:5000/advert/",
                             json={"title": "advert", "description": 'Test description', "owner": 'me'},
                             headers={"token": "QWERTY"}
    
                             )
    print(response.status_code)
    print(response.text)
    
    response = requests.get(f"http://127.0.0.1:5000/advert/{i}")
    print(response.status_code)
    print(response.text)
    
    response = requests.patch(f"http://127.0.0.1:5000/advert/{i}",
                             json={"title": "Tenet", "description": "New description"}
                             )
    print(response.status_code)
    print(response.text)
    
    response = requests.delete(f"http://127.0.0.1:5000/advert/{i}")
    print(response.status_code)
    print(response.text)

