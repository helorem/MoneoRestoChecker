import json
import time
import requests
import re
import threading
import datetime

from DBConsumer import DBConsumer

class MoneoChecker:
    def __init__(self, conf):
        self.conf = conf
        self.looping = False
        self.thread = None
        self.parse_regex = re.compile(r'\((.*)\);')

    def __parse_moneo_json(self, content):
        res = self.parse_regex.sub(r'\1', content)
        return res

    def do_request_balance(self):
        print "[Checker] Check Balance"
        url = "%s/app/ws/wsClasses.php" % self.conf["url"]
        data = {
                "q" : "getBalanceCardH",
                "login" : self.conf["login"],
                "pwd" : self.conf["pwd"]
            }
        res = requests.get(url, params=data)
        json_str = self.__parse_moneo_json(res.content)
        data = json.loads(json_str)

        DBConsumer.get_instance().execute("DELETE FROM balance")
        for item in data["respBody"]["accountBalanceStruct"]:
            amount = int(item["availableBalance"])
            if amount > 0:
                validity = item["expirationDate"]
                DBConsumer.get_instance().execute("INSERT INTO balance ('amount', 'validity') VALUES (?, ?)", (amount, validity))
        DBConsumer.get_instance().execute("UPDATE update_time SET balance = ?", (data["respHeader"]["dateTimeServer"],))

    def do_request_histo(self):
        print "[Checker] Check Histo"
        url = "%s/app/ws/wsClasses.php" % self.conf["url"]
        data = {
                "q" : "getHistoryNewCardH",
                "login" : self.conf["login"],
                "pwd" : self.conf["pwd"]
            }
        res = requests.get(url, params=data)
        json_str = self.__parse_moneo_json(res.content)
        data = json.loads(json_str)

        for item in data["respBody"]["paymentStruct"]:
            amount = int(item["montantTransaction"])
            name = item["nomAdresseAcceptCarte"]
            dt = item["dateHeureTransaction"]
            row = DBConsumer.get_instance().query("SELECT id FROM transact WHERE name = ? AND amount = ? AND dt = ?", (name, amount, dt))
            if not row:
                DBConsumer.get_instance().execute("INSERT INTO transact (name, amount, dt) VALUES (?, ?, ?)", (name, amount, dt))
        DBConsumer.get_instance().execute("UPDATE update_time SET histo = ?", (data["respHeader"]["dateTimeServer"],))

    def __run(self):
        self.looping = True
        while self.looping:
            self.do_request_balance()
            self.do_request_histo()
            DBConsumer.get_instance().execute("UPDATE update_time SET request = ?", (str(datetime.datetime.now()),))
            print "[Checker] Wait %s seconds" % self.conf["interval"]
            for i in xrange(0, self.conf["interval"]):
                if not self.looping:
                    break
                time.sleep(1)

    def start(self):
        if self.thread is not None:
            self.stop()
        self.thread = threading.Thread(None, self.__run)
        self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.looping = False
            self.thread.join()

if __name__ == "__main__":
    conf = {}
    with open("server.conf", "r") as fd:
        conf = json.load(fd)
    inst = MoneoChecker(conf["moneo"])
    inst.start()
    try:
        while True:
            time.sleep(1)
    finally:
        inst.stop()
        DBConsumer.get_instance().stop()
