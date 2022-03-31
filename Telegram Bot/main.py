import requests
import json
import time

tokenn="5261206107:AAFYjjoYoFpa0j3P_MSVwyuv7"
idi = -1001534803074
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

message = "Hello! Welcome to Covid Platform!"
# read token file
with open('token.txt', 'r') as f:
    TOKEN = f.read()

base_url = "https://api.telegram.org/bot"+TOKEN
send_url = "https://api.telegram.org/bot"+TOKEN+"/sendMessage"
send_photo = "https://api.telegram.org/bot"+TOKEN+"/sendPhoto"

send_notification = False

urls = [
            "https://drive.google.com/file/d/1KunYh-60sS-6UB7trWIklLBUgn3TkMMe/view?usp=sharing",
            "https://drive.google.com/file/d/1mCz8GqMSECX4wwRUkPzQe0TCti1uLs83/view?usp=sharing",
            "https://drive.google.com/file/d/1Ij1-FfFt2n03-838ViWo-oZ1TQtqA0W9/view?usp=sharing",
            "https://drive.google.com/file/d/1Fa8jSh2eEBVBt617mT7QE9xqyrLp8--0/view?usp=sharing",
            "https://drive.google.com/file/d/13ghoErKPmtAOpJDlOWVZD58e0mKGjOFx/view?usp=sharing",
            "https://drive.google.com/file/d/1GPhR6yo1e0QhPBfQraLH2Lv_JN_W9rLp/view?usp=sharing",
            "https://drive.google.com/file/d/1EoYL8ZrdzFpatKhKsZLV5zbBYRYvpY36/view?usp=sharing",
            "https://drive.google.com/file/d/1NBgCm520RGSsKBfYi4BRw1tzpQJciBTi/view?usp=sharing",
            "https://drive.google.com/file/d/1_5TuW4XUQiLV18nxvF-WIpfrWb_C5e2R/view?usp=sharing",
        ]

captions = [
    "State wise Analysis", "COVID 19 : Pandemic In India",
    "State wise Confirmed/Death/Recovered Stacked",
    "State wise Cases per 100 confirmed",
    "7 days Mean Confirmed",
    "Recovered",
    "Death Report",
    "Total Cases Statistics",
    "Top21 Confirmed/Death/Recovered Stacked"
]

def read_msg(offset) :
    parameters = {
        "offset": offset
    }

    resp = requests.get(base_url + "/getUpdates", data=parameters)
    data = resp.json()

    print(data)

    for result in data["result"]:
        send_msg(result)
        print(result)

    if data["result"]:
        return data["result"][-1]["update_id"] + 1



def auto_answer(message):

    if message.startswith("Hello"):
        answer = "Welcome to COVID Platform !!!!! \n\n 1. Type 'Availability of vaccine in DistrictCode on Date' \n\n 2. Type 'State wise Analysis' \n\n3.  Type 'COVID Stats' \n\n4.  Type 'State wise Confirmed/Death/Recovered'\n\n5.  Type 'State wise Cases' \n\n 6.  Type '7 days Mean' \n\n7. Type 'Top21 Confirmed/Death/Recovered Stacked'\n\n 8. Type 'Death Report'\n\n 9. Type 'Recovered Report'\n\n 10. Type 'Total Cases Statistics'"
        return answer

    elif message.startswith("Availability of vaccine"):
        pin=message.split()[3]
        dt=message.split()[4]
        global  send_notification
        send_notification=True
        while (send_notification):
            welcome = base_url + "/sendMessage?chat_id=-1001534803074&text=" + message
            requests.get(welcome)
            # msg = []
            for i in range(362,500):
                    x = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+pin+ "&date="+dt
                    data = requests.get(x, headers=header)
                    results = json.loads(data.text)
                    counts = results["centers"]
                    if (len(counts) > 0):
                        msg = []
                        for centers in counts:
                            # msg=[]
                            msg.append({
                                "district_name": centers["district_name"],
                                # "district_name": centers["district_name"],
                                "name": centers["name"],
                                "fees": centers["fee_type"]
                            })
                            for sessions in centers["sessions"]:
                                msg.append({
                                    "min_age_limit": sessions["min_age_limit"],
                                    "vaccine": sessions["vaccine"],
                                    "slots": sessions["slots"],
                                    "available_capacity_dose1": sessions["available_capacity_dose1"],
                                    "available_capacity_dose2": sessions["available_capacity_dose2"]

                                })
                            parse_data = json.dumps(msg)
                            parse_data = parse_data.replace("{", "")
                            parse_data = parse_data.replace("}", "\n\n")
                            parse_data = parse_data.replace("[", "")
                            parse_data = parse_data.replace("]", "")
                            parse_data = parse_data.replace(",", "\n")
                            print(parse_data)
                            un_url = "https://api.telegram.org/bot5168319038:AAF0lSXx9wTkqaXVHtACppBg7qrpedHvv8I/sendMessage?chat_id=-1001534803074&text=" + parse_data
                            y = requests.get(un_url)
                            print(y)
                            time.sleep(20)
            time.sleep(600)

    elif message.lower()=="stop":
        print(message.lower())
        return "Covid Bot Stopped"

    elif message == "State wise Analysis":
        length = len(urls)
        for i in range(length):
            if captions[i] == message:
                # time.sleep(10)
                parameters = {
                    "chat_id": "-1001534803074",
                    "photo": urls[i],
                    "caption": captions[i]
                }
                resp = requests.get(send_photo, data=parameters)
                print(resp.text)
                break
            else:
                pass
    elif message == "COVID Stats":
            length = len(urls)
            for i in range(length):
                if captions[i] == "COVID 19 : Pandemic In India":
                    # time.sleep(10)
                    parameters = {
                        "chat_id": "-1001534803074",
                        "photo": urls[i],
                        "caption": captions[i]
                    }
                    resp = requests.get(send_photo, data=parameters)
                    print(resp.text)
                    break
                else:
                    pass
    elif message == "State wise Confirmed/Death/Recovered":
            length = len(urls)
            for i in range(length):
                if captions[i] == "State wise Confirmed/Death/Recovered Stacked":
                    # time.sleep(10)
                    parameters = {
                        "chat_id": "-1001534803074",
                        "photo": urls[i],
                        "caption": captions[i]
                    }
                    resp = requests.get(send_photo, data=parameters)
                    print(resp.text)
                    break
                else:
                    pass
    elif message == "State wise Cases":
        length = len(urls)
        for i in range(length):
            if captions[i] == "State wise Cases per 100 confirmed":
                # time.sleep(10)
                parameters = {
                    "chat_id": "-1001534803074",
                    "photo": urls[i],
                    "caption": captions[i]
                }
                resp = requests.get(send_photo, data=parameters)
                print(resp.text)
                break
            else:
                pass
    elif message == "7 days Mean":
        length = len(urls)
        for i in range(length):
            if captions[i] == "7 days Mean Confirmed":
                # time.sleep(10)
                parameters = {
                    "chat_id": "-1001534803074",
                    "photo": urls[i],
                    "caption": captions[i]
                }
                resp = requests.get(send_photo, data=parameters)
                print(resp.text)
                break
            else:
                pass
    elif message == "Recovered Report":
        length = len(urls)
        for i in range(length):
            if captions[i] == "Recovered":
                # time.sleep(10)
                parameters = {
                    "chat_id": "-1001534803074",
                    "photo": urls[i],
                    "caption": captions[i]
                }
                resp = requests.get(send_photo, data=parameters)
                print(resp.text)
                break
            else:
                pass
    elif message == "Death Report":
        length = len(urls)
        for i in range(length):
            if captions[i] == "Death Report":
                # time.sleep(10)
                parameters = {
                    "chat_id": "-1001534803074",
                    "photo": urls[i],
                    "caption": captions[i]
                }
                resp = requests.get(send_photo, data=parameters)
                print(resp.text)
                break
            else:
                pass


    elif message == "Total Cases Statistics":
        length = len(urls)
        for i in range(length):
            if captions[i] == "Total Cases Statistics":
                # time.sleep(10)
                parameters = {
                    "chat_id": "-1001534803074",
                    "photo": urls[i],
                    "caption": captions[i]
                }
                resp = requests.get(send_photo, data=parameters)
                print(resp.text)
                break
            else:
                pass
    elif message == "Top21 Confirmed/Death/Recovered Stacked":
        length = len(urls)
        for i in range(length):
            if captions[i] == "Top21 Confirmed/Death/Recovered Stacked":
                # time.sleep(10)
                parameters = {
                    "chat_id": "-1001534803074",
                    "photo": urls[i],
                    "caption": captions[i]
                }
                resp = requests.get(send_photo, data=parameters)
                print(resp.text)
                break
            else:
                pass
    else:
        return "Sorry, I could not understand you !!! I am still learning and try to get better in answering."







def send_msg(message):
    text = message["message"]["text"]
    message_id = message["message"]["message_id"]
    answer = auto_answer(text)
    parameters = {
        "chat_id": "-1001534803074",
        "text": answer,
        "reply_to_message_id": message_id
    }

    resp = requests.get(base_url + "/sendMessage", data=parameters)
    print(resp.text)




offset = 0
while True:
    offset = read_msg(offset)







