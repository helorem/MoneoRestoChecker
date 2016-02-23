import sys
sys.path.insert(0, '../')

import fakeserver
import unittest
import requests
import json

class MainTestCase(unittest.TestCase):
    
    def default_server(self, url):
        def callback_histo(args):
            data = {
                "respHeader" : {
                    "resultCode" : 0,
                    "resultDesc" : "Agreement",
                    "dateTimeServer" : "2016-02-19T14:15:15",
                    "serverId" : 2,
                    "transactionId" : 12781234
                },
                "respBody" : {
                    "cardHolderId" : 12345678,
                    "paymentStruct" : [
                        {
                            "dateHeureTransaction" : "2016-02-19T12:58:57",
                            "MTI" : 4010,
                            "montantTransaction" : 920,
                            "nomAdresseAcceptCarte" : "PIZZA HUT"
                        },
                        {
                            "dateHeureTransaction" : "2016-02-18T13:58:16",
                            "MTI" : 4010,
                            "montantTransaction" : 920,
                            "nomAdresseAcceptCarte" : "MC DONALDS"
                        },
                        {
                            "dateHeureTransaction" : "2016-02-14T16:10:59",
                            "MTI" : 4010,
                            "montantTransaction" : 1900,
                            "nomAdresseAcceptCarte" : "KFC"
                        }
                    ],
                    "paymentPage" : {
                        "offset" : 0,
                        "limit" : 10,
                        "totalCount" : 183,
                        "order" : "js.dateHeureTransaction DESC"
                    },
                    "accountMovementStruct" : {
                        "accountMovementId" : 6546751,
                        "accountNumber" : "12345678",
                        "productId" : 10,
                        "expirationDate" : "2017-02-28T23:59:59",
                        "vf" : 1050,
                        "amount" : 19950,
                        "type" : 1,
                        "previousBalance" : 10433,
                        "newBalance" : 30383,
                        "orderId" : 70042953,
                        "dateCreated" : "2016-02-03T12:22:35",
                        "reasonCode" : 2
                    },
                    "accountMovementPage" : {
                        "offset" : 0,
                        "limit" : 1,
                        "totalCount" : 3
                    }
                }
            }
            content = "%s" % json.dumps(data)
            return {"content" : content}

        def callback_balance(args):
            data = {
                "respHeader" : {
                        "resultCode" : 0,
                        "resultDesc" : "Agreement",
                        "dateTimeServer" : "2016-02-19T14:10:25",
                        "serverId" : 2,
                        "transactionId" : 12784872
                },
                "respBody" : {
                    "cardHolderId" : 12345678,
                    "accountBalanceStruct" : [
                        {
                            "accountNumber" : "12345678",
                            "productId" : 10,
                            "expirationDate" : "2016-02-29T23:59:59",
                            "vf" : 1050,
                            "availableBalance" : 0,
                            "ledgerBalance" : 0,
                            "timestampBO" : "2016-02-19T08:52:10",
                            "lastMovement" : 6327999,
                            "dayLimitPayment" : 0
                        },
                        {
                            "accountNumber" : "12345678",
                            "productId" : 10,
                            "expirationDate" : "2017-02-28T23:59:59",
                            "vf" : 1050,
                            "availableBalance" : 11863,
                            "ledgerBalance" : 12345,
                            "timestampBO" : "2016-02-19T08:52:10",
                            "lastMovement" : 6797963,
                            "dayLimitPayment" : 980
                        }
                    ]
                }
            }
            content = "%s" % json.dumps(data)
            return {"content" : content}

        server = fakeserver.FakeServer()
        server.add_url_callback(url, callback_balance, {"q" : "getBalanceCardH"})
        server.add_url_callback(url, callback_histo, {"q" : "getHistoryNewCardH"})

        return server

    def test_init(self):
        url = "/app/ws/wsClasses.php"
        server = self.default_server(url)
        server.start()
        try:
            data = {
                    "q" : "getBalanceCardH",
                    "user" : "user",
                    "pwd" : "pwd"
                }
            res = requests.get("http://127.0.0.1:5000" + url, params=data)
            self.assertEqual(res.status_code, 200)
        finally:
            server.stop()

    def test_histo_simple(self):
        url = "/app/ws/wsClasses.php"
        server = self.default_server(url)
        server.start()
        try:
            data = {
                    "q" : "getHistoryNewCardH",
                    "user" : "user",
                    "pwd" : "pwd"
                }
            res = requests.get("http://127.0.0.1:5000" + url, params=data)
            self.assertEqual(res.status_code, 200)
        finally:
            server.stop()

    def test_balance_simple(self):
        url = "/app/ws/wsClasses.php"
        server = self.default_server(url)
        server.start()
        try:
            data = {
                    "q" : "getBalanceCardH",
                    "user" : "user",
                    "pwd" : "pwd"
                }
            res = requests.get("http://127.0.0.1:5000" + url, params=data)
            self.assertEqual(res.status_code, 200)
        finally:
            server.stop()

