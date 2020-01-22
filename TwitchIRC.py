import socket

SERVER = "irc.twitch.tv"
PORT = 6667
PASSWORD = "oauth:iyfocmwnear1sox4m65g7d1rbjq61x"
USERNAME = "twitchplaystrackmania"
CHANNEL = USERNAME
IRC = socket.socket()


def connect():
    Connecting = True
    IRC.connect((SERVER, PORT))
    IRC.send(
        (
            "PASS " + PASSWORD + "\n" +
            "NICK " + USERNAME + "\n" +
            "JOIN #" + CHANNEL + "\n"
        )
        .encode()
    )
    while Connecting:
        readbuffer_join = IRC.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        for line in readbuffer_join.split("\n")[0:-1]:
            if ("End of /NAMES list" in line):
                print("Connected")
                Connecting = False


def send(message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    IRC.send((messageTemp + "\n").encode())


def get_user(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user


def get_message(line):
    try:
        message = line.split(":", 2)[2]
    except:
        message = ""
    return message


def is_user_message(line):
    if "PRIVMSG" in line:
        return True
    else:
        return False


def run():
    while True:
        try:
            readbuffer = IRC.recv(1024).decode()
        except:
            readbuffer = ""
        for line in readbuffer.split("\r\n"):
            if is_user_message(line):
                user = get_user(line)
                message = get_message(line)
                print(user + ": " + message)
            elif "PING" in line:
                print("Received a PING")
                message = "PONG tmi.twitch.tv\r\n".encode()
                IRC.send(message)
                print("Sent a PONG")


connect()
run()
