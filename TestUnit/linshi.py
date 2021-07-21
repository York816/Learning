import json

if __name__ == '__main__':
    raw_data = {
        "startTime": "2021-06-08 14:57:13",
        "params": "{\"number\":106.22154780,\"address\":\"8\",\"actualPayment\":\"card\",\"money\":700.00,\"rate\":\"6.590000000000\",\"orderId\":\"TS202106080656582345\",\"currency\":\"CNY\",\"remark\":\"8商户\",\"coinName\":\"USDT\"}",
        "message": "success",
        "body": "{\"code\":200,\"data\":{\"orderType\":\"0\",\"orderSn\":\"458284054347300864\",\"orderId\":\"TS202106080656582345\",\"tradeToUsername\":\"u1611916082211\",\"remark\":\"8商户\",\"localCurrency\":\"CNY\",\"advertiseId\":389,\"makerPhone\":\"13598044022\",\"number\":106.22154779,\"actualPayment\":\"card\",\"payRefer\":\"168573\",\"price\":6.590000000000,\"customerId\":16,\"merchantPrice\":6.590000000000,\"cashierUrl\":\"http://www.private-station.cc/cashier/#/web/home?orderSn=458284054347300864\",\"tradeType\":1,\"memberId\":14,\"address\":\"8\",\"payMode\":\"card\",\"timeLimit\":15,\"merchantNumber\":106.22154779,\"money\":700.00,\"createTime\":1623135433062,\"merchantCommission\":1.06221547,\"coinName\":\"USDT\",\"payData\":\"[{\\\"bank\\\":\\\"中国农业银行\\\",\\\"branch\\\":\\\"郑州马寨支行\\\",\\\"createTime\\\":1611916990000,\\\"id\\\":41,\\\"memberId\\\":14,\\\"payAddress\\\":\\\"6230520710119143370\\\",\\\"payType\\\":\\\"card\\\",\\\"realName\\\":\\\"王德印\\\",\\\"status\\\":1,\\\"updateTime\\\":1611916990000}]\",\"status\":1},\"responseString\":\"200~SUCCESS\",\"message\":\"下单成功\"}"
    }
    key_list = [
        "busiId",
        "coinName",
        "amount",
        "merchantAmount",
        "money",
        "fee",
        "address",
        "orderId",
        "orderType",
        "callbackType",
    ]
    result = {}
    use_data = {**json.loads(raw_data['params']), **json.loads(raw_data['body'])}
    # print(use_data)
    use_data = {**use_data, **use_data['data']}
    # print("去除嵌套后的对象", use_data)
    # for key in key_list:
    #     if use_data.get(key):
    #         result[key] = use_data[key]
    #     else:
    #         result[key] = None
    # print(json.dumps(result, indent=4))
    test1 = 'orderNo=TS202106291024116736&channel=null&pay=AdapterFlashEXpay&bank=&channel_id=4c28-6e595a451&usd_amount=100.00&transfer_amount='
    oo = {}
    for item in test1.split('&'):
        temp = item.split('=')
        print("temp", temp)
        oo[temp[0]] = temp[1]
        print(temp[1], oo[temp[0]])

    print(oo)

    test2 = 'orderNo=TS202106291024116736&channel=null&pay=AdapterFlashEXpay&bank=&channel_id=4c28-6e595a451&usd_amount=100.00&transfer_amount='
    o1 = []
    for item in test2.split('&'):
        temp = item.replace('=', ':')
        o1.append(temp)

    print('\n'.join(oo))

    temp = '111'
    data = {
        "params": json.dumps(
            {"merchant_ref": "DP202107060651453223", "system_ref": temp, "amount": "4062.38", "pay_amount": "4062.38",
             "fee": "105.73", "satus": 1, "success_time": "1624242070"})
    }
    print(json.dumps(data))
