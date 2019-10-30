from twilio.rest import Client

account_sid = 'ACb7440de2da723ef77ea132c506c9bfd6'
auth_token = '739ab76d2ce84a917758f7545dc712b4'
client = Client(account_sid, auth_token)


def sendMessage(phone:str, msg:str):
    message = client.messages \
                .create(
                     body=msg,
                     messaging_service_sid='MGdaf06f350a5d3e1fbaf124da4775255d',
                     to=phone
                 )
    return message

if __name__ == "__main__":
#     a=sendMessage('+19494139082', 'Testing msg: [WeTest]Your code fucked up at testcase 1')
#     b=sendMessage('+19495294310', 'Testing msg: [WeTest]Your code fucked up at testcase 1')
#     c=sendMessage('+19492318382', 'Testing msg: [WeTest]Your code fucked up at testcase 1')
    d=sendMessage('+13109482946', 'Testing msg: [WeTest]Your code fucked up at testcase 1')
    print(dict( d))