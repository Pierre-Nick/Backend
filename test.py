from urllib.request import urlopen

url = "http://127.0.0.1:8080?command=register&"
while True:
    url = "http://127.0.0.1:8080?command=additem&barcode=%s&sessionkey=2178071641&" % (str(input("Barcode: ")))
    response = urlopen(url).read()
    print(response)
