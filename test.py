import json

with open('Reply_Message.json', 'r') as f: 
    message_dict = json.load(fp = f)

for i in range(1,len(message_dict)):
    print(message_dict[f'message{i}']['text'])


# print(message_dict['message2'])

f.close()