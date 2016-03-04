import flask
import json

app = flask.Flask(__name__)

@app.route("/app/ws/wsClasses.php", methods=["GET"])
def www_page():
    data = {}
    if flask.request.args.get("login") is None:
        data = {
            "faultstring" : "\nElement 'token': [facet 'minLength'] The value has a length of '0'; this underruns the allowed minimum length of '1'.\nElement 'token': '' is not a valid value of the atomic type '{http:\/\/extranet.lusis.fr\/moneo\/schemas\/moneo.xsd}TypeAN32'.\nElement 'cardHolderId': '' is not a valid value of the atomic type '{http:\/\/extranet.lusis.fr\/moneo\/schemas\/moneo.xsd}TypeCardHolderId'.\n     ",
            "faultcode" : "SOAP-ENV:Server"
        }
    elif flask.request.args.get("pwd") is None:
        # TODO
        pass
    elif flask.request.args.get("q") is None:
        # TODO
        pass
    elif flask.request.args.get('q') == "getHistoryNewCardH":
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
    elif flask.request.args.get('q') == "getBalanceCardH":
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

    content = "(%s);" % json.dumps(data)
    return content

if __name__ == "__main__":
    app.debug = True
    app.run(host="172.17.42.1", port=7412)

