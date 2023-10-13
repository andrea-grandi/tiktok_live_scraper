from multiprocessing.connection import Listener
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent, ViewerCountUpdateEvent
import socket

p1 = False
p2 = False
userOne = ""
userTwo = ""
connected = False
countOne = 100
countTwo = 100
messageError = "Errore di connessione"

client: TikTokLiveClient = TikTokLiveClient(
    unique_id="amy_cutiies", **(
        {
            # Custom Asyncio event loop
            "loop": None,

            # Custom Client params
            "client_params": {},

            # Custom request headers
            "headers": {},

            # Custom timeout for Webcast API requests
            "timeout_ms": 1000,

            # How frequently to make requests the webcast API when long polling
            "ping_interval_ms": 1000,

            # Whether to process initial data (cached chats, etc.)
            "process_initial_data": True,

            # Whether to get extended gift info (Image URLs, etc.)
            "enable_extended_gift_info": True,

            # Whether to trust environment variables that provide proxies to be used in http requests
            "trust_env": False,

            # Set the language for Webcast responses (Changes extended_gift's language)
            "lang": "en-US",

            # Connect info (viewers, stream status, etc.)
            "fetch_room_info_on_connect": True,
            
            # Parameter to increase the amount of connections made per minute via a Sign Server API key. 
            # If you need this, contact the project maintainer.
            "sign_api_key": None
        }
    )
)

# Setto il nome del primo utente che manda una gift 
# per associarlo al player1, stessa cosa per il player2 

def set_name_players(user):
    global connected
    client_socket = socket.socket()  # instantiate
    while(connected == False):
        try:
            client_socket.connect(("127.0.0.1", 5555))  # connect to the server
            connected = True
        except:
            print(messageError)
            return
    client_socket.send(user.encode())  # send message
    client_socket.close()  # close the connection

# Invio il messaggio al server per attaccare, rispettivamente
# per il player1 e per il player2

def send_attack_player1():
    global countOne
    client_socket = socket.socket()  # instantiate
    try:
        client_socket.connect(("127.0.0.1", 5556))  # connect to the server
    except:
        print(messageError)
        return
    client_socket.send(b"atk")  # send message
    countOne -= 1
    client_socket.close()  # close the connection

def send_attack_player2():
    global countTwo
    client_socket = socket.socket()  # instantiate
    try:
        client_socket.connect(("127.0.0.1", 5557))  # connect to the server
    except:
        print(messageError)
        return
    client_socket.send(b"atk")  # send message
    countTwo -= 1
    client_socket.close()  # close the connection

@client.on("gift")
async def on_gift(event: GiftEvent):
    global p1
    global p2
    global userOne
    global userTwo
    global connected
    global countOne
    global countTwo
    
    # If it's type 1 and the streak is over
    if event.gift.streakable:
        if not event.gift.streaking:
            print(f"{event.user.uniqueId} sent {event.gift.repeat_count}x \"{event.gift.extended_gift.name}\"")
            print(f"{event.user.uniqueId} sent a {event.gift.giftId}!")

            if p1 == True and p2 == True:
                if event.gift.giftId == 5655: #Rosa
                    send_attack_player1()     #Quando arriva una rosa il player1 attacca
                if event.gift.giftId == 6093: #GG
                    send_attack_player2()     #Quando arriva GG il player2 attacca
                if countOne == 0 or countTwo == 0:
                    p1 = False
                    p2 = False
                    userOne = ""
                    userTwo = ""

            if p2 == False and p1 == True and userOne != event.user.uniqueId:
                connected = False
                set_name_players(event.user.uniqueId)
                print("Nome giocatore 2!!!")
                p2 = True
                userTwo = event.user.uniqueId

            if p1 == False:
                connected = False
                set_name_players(event.user.uniqueId)
                print("Nome giocatore 1!!!")
                p1 = True
                userOne = event.user.uniqueId
            
    # It's not type 1, which means it can't have a streak & is automatically over
    else:
        print(f"{event.user.uniqueId} sent \"{event.gift.extended_gift.name}\"")
        print(f"{event.user.uniqueId} sent a {event.gift.giftId}!")

        if p1 == True and p2 == True:
            if event.gift.giftId == 5655: #Rosa
                send_attack_player1()     #Quando arriva una rosa il player1 attacca
            if event.gift.giftId == 6093: #GG
                send_attack_player2()     #Quando arriva GG il player2 attacca
            if countOne == 0 or countTwo == 0:
                p1 = False
                p2 = False
                userOne = ""
                userTwo = ""

        if p2 == False and p1 == True and userOne != event.user.uniqueId:
            connected = False
            set_name_players(event.user.uniqueId)
            print("Nome giocatore 2!!!")
            p2 = True
            userTwo = event.user.uniqueId

        if p1 == False:
            connected = False
            set_name_players(event.user.uniqueId)
            print("Nome giocatore 1!!!")
            p1 = True
            userOne = event.user.uniqueId

"""    
@client.on("gift")
async def on_gift(event: GiftEvent):
    print(f"{event.user.uniqueId} sent a {event.gift.giftId}!")
    # Prendo il nome (ID) del primo che manda il gift e lo setto nel player 1,
    # faccio la stessa cosa con il secondo utente che manda il gift e lo setto
    # nel player 2
    global p1
    global p2
    global userOne
    global userTwo
    global connected
    global countOne
    global countTwo
 
    if p1 == True and p2 == True:
        if event.gift.giftId == 5655: #Rosa
            send_attack_player1()     #Quando arriva una rosa il player1 attacca
        if event.gift.giftId == 6093: #GG
            send_attack_player2()     #Quando arriva GG il player2 attacca
        if countOne == 0 or countTwo == 0:
            p1 = False
            p2 = False
            userOne = ""
            userTwo = ""

    if p2 == False and p1 == True and userOne != event.user.uniqueId:
        connected = False
        set_name_players(event.user.uniqueId)
        print("Nome giocatore 2!!!")
        p2 = True
        userTwo = event.user.uniqueId

    if p1 == False:
        connected = False
        set_name_players(event.user.uniqueId)
        print("Nome giocatore 1!!!")
        p1 = True
        userOne = event.user.uniqueId
"""
    
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

@client.on("comment")
async def on_connect(event: CommentEvent):
    print(f"{event.user.uniqueId} -> {event.comment}")

@client.on("like")
async def on_like(event: LikeEvent):
    print(f"{event.user.uniqueId} has liked the stream {event.likeCount} times, there is now {event.totalLikeCount} totals likes!")
    
@client.on("follow")
async def on_follow(event: FollowEvent):
    print(f"{event.user.uniqueId} followed the streamer")

@client.on("share")
async def on_share(event: ShareEvent):
    print(f"{event.user.uniqueId} shared the streamer")

@client.on("viewer_count_update")
async def on_connect(event: ViewerCountUpdateEvent):
    print("Received a new viewer count:", event.viewerCount)
    
if __name__ == '__main__':
    client.run()
    

