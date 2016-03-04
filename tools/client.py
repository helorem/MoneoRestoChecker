import requests

def req(host):
    url = "http://%s/app/ws/wsClasses.php" % host
    data = {
            "q" : "getBalanceCardH",
            "login" : "90008974",
            "pwd" : "4215"
        }
    res = requests.get(url, params=data)
    return (res.status_code, res.content)

#status1, content1 = req("www.moneo-resto.fr")
status2, content2 = req("127.0.0.1:7412")

print content2
