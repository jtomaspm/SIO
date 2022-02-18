import json
from time import time

DATA = {}
COOLDOWN = {"login": (10, 3600), "register": (3, 3600), "comment": (5, 900)}  # values: max number, cooldown time
MAX_COOLDOWNS = 3

# html special character tokens
swap_list = [
    ["&", "&#38"],
    ["#", "&#35"],
    ["\"", "&#34"],
    ["'", "&#39"],
    ["(", "&#40"],
    [")", "&#41"],
    ["/", "&#47"],
    [";", "&#59"],
    ["<", "&#60"],
    [">", "&#62"]
]


# transform input into safe string
def swap_sp_char_for_token(string):
    for item in swap_list:
        string = string.replace(item[0], item[1])
    return string


# check for special characters
def check_for_sp_chars(string):
    for item in swap_list:
        if item[0] in string:
            return True
    return False


# Read from data.json
def read_data():
    global DATA

    with open("static/db/data.json", "r") as f:
        obj = f.read()
    DATA = json.loads(obj)


# Write to data.json
def write_data():
    with open("static/db/data.json", "w") as f:
        json.dump(DATA, f)


# Handle request to check the frequency controller
# 1 - login
# 2 - register
# 3 - comment
def handle_check_ip_request(op, ip):
    if ip not in DATA["blacklist"]:
        if ip not in DATA:
            DATA[ip] = {}
            DATA[ip]["login"] = [time(), 0]
            DATA[ip]["register"] = [time(), 0]
            DATA[ip]["comment"] = [time(), 0]
            DATA[ip]["cooldown"] = 0
            DATA[ip]["strikes"] = 0  # number of cooldowns

            # Save changes
            write_data()

            return False
        else:
            # check for perma ban
            if DATA[ip]["strikes"] >= MAX_COOLDOWNS:
                DATA["blacklist"] += [ip]
                DATA.pop(ip)

                # Save changes
                write_data()

            else:

                # Check if a user is currently cooldowned and if the user is, check if the cooldown time is over
                if DATA[ip]["cooldown"] != 0 and DATA[ip]["cooldown"] <= time():
                    DATA[ip]["cooldown"] = 0

                    # Save changes
                    write_data()

                else:
                    if op == 1:
                        # login
                        return check_ip_login(ip)
                    elif op == 2:
                        # register
                        return check_ip_register(ip)

                    elif op == 3:
                        # comment
                        return check_ip_comment(ip)

    return True


def check_ip_login(ip):
    danger = False

    t = time() - DATA[ip]["login"][0]
    if t < 600:
        if DATA[ip]["login"][1] + 1 < COOLDOWN["login"][0]:
            DATA[ip]["login"][1] += 1

        # Within 10 min this ip logged in 10 times
        else:
            danger = True
            DATA[ip]["strikes"] += 1
            DATA[ip]["cooldown"] = time() + COOLDOWN["login"][1]

    # 10 min cooldown passed by
    else:
        DATA.pop(ip)

    # Save changes
    write_data()

    return danger


def check_ip_register(ip):
    danger = False

    t = time() - DATA[ip]["register"][0]
    if t < 600:  # t < 10 min
        if DATA[ip]["register"][1] + 1 < COOLDOWN["register"][0]:
            DATA[ip]["register"][1] += 1

        # Within 10 min this ip registered 3 times
        else:
            danger = True
            DATA[ip]["strikes"] += 1
            DATA[ip]["cooldown"] = time() + COOLDOWN["register"][1]

    # 10 min cooldown passed by
    else:
        DATA[ip]["register"].pop(ip)

    # Save changes
    write_data()

    return danger


def check_ip_comment(ip):
    danger = False

    t = time() - DATA[ip]["comment"][0]
    if t < 600:  # t < 10 min
        if DATA[ip]["comment"][1] + 1 < COOLDOWN["comment"][0]:
            DATA[ip]["comment"][1] += 1

        # Within 10 min this ip commented 5 times
        else:
            danger = True
            DATA[ip]["strikes"] += 0.5
            DATA[ip]["cooldown"] = time() + COOLDOWN["register"][1]

    # 10 min cooldown passed by
    else:
        DATA[ip]["comment"].pop(ip)

    # Save changes
    write_data()

    return danger
