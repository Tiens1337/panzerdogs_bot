import socketio
import json
sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    # sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

headers = {
    'Sec-WebSocket-Version': '13',
    'Sec-WebSocket-Key': 'WJCsw3voPgBNOSVRnMCFSw=='
}

d = {
    "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0OWU0N2ZiZGQ0ZWUyNDE0Nzk2ZDhlMDhjZWY2YjU1ZDA3MDRlNGQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vcGFuemVyZG9ncy1kYzE4NSIsImF1ZCI6InBhbnplcmRvZ3MtZGMxODUiLCJhdXRoX3RpbWUiOjE2OTkwOTM0NDUsInVzZXJfaWQiOiJRVE5xZkpTZVN1Um5PVm01M0dlNDVQZkpjNHoyIiwic3ViIjoiUVROcWZKU2VTdVJuT1ZtNTNHZTQ1UGZKYzR6MiIsImlhdCI6MTY5OTI1OTYxMiwiZXhwIjoxNjk5MjYzMjEyLCJlbWFpbCI6InJhYm90eWFnYTIyOUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmFib3R5YWdhMjI5QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.iU61GYI8szpZltenwPA8u7ymN_oEGVkZouWwFaUQ2WhpJ-g8hgUugndOco2zIVqWexttTLYToCB0GhMJ2yP0-EpZkQProy5IJ12CGR3CfPFKkc-HdZbiPDGAZa0o5NIf1leFoUx6U3NbNGqKikBwGX9iNKBaPrfdxDgQekEK8B97zT8qr9itYM90MI3b09OkIVKtdUZQ97OFlWXTGDW4cK5hxzc0gf9F60Lh1_c8YRQukkBtg0jHbdbPjxycdWc7WIuG2WUwpd6wswAJ-evVtuRbO_7Dpg1NEZeft3Ui4r9f4ukEVMH3MnBvt1WXijaOKvXTYGue7jczlHRrpBONzg"
}

sio.connect('https://lobby2.luckykatgames.net:4000/', headers=headers, transports=['websocket'], wait_timeout=5)
print('my sid is ', sio.sid)
# sio.send('40'+json.dumps(d))


sio.wait()