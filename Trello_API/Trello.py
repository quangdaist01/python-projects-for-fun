from trello import TrelloClient, Board, List, Card
from datetime import datetime
from config import TRELLO_API, TRELLO_TOKEN
client = TrelloClient(
    api_key=TRELLO_API,
    api_secret='your-secret',
    token=TRELLO_TOKEN,
    token_secret='your-oauth-token-secret'
)


# My 4 lists in Daily board:
## <List 💪💪💪💪>
## <List 📚📚📚📚>
## <List 🥰😂😊😅>
## <List ✅✅✅✅>
## <List Hậu Về Quê>


def get_trello_board_from(client: TrelloClient, board_name: str):
    all_boards = client.list_boards()
    for board in all_boards:
        if board.name == board_name:
            return board


def get_trello_list_from(board: Board, list_name: str):
    for item in board.list_lists():
        if item.name == list_name:
            return item


def add_trello_card_to(client, board_name: str, list_name: str, card_name: str):
    print("Adding a Trello card...")
    trello_board = get_trello_board_from(client, board_name)
    trello_list = get_trello_list_from(trello_board, list_name)
    trello_list.add_card(card_name)
    print("Add successfully!")


def today_is(*days_of_week: str) -> bool:
    week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    week_days_num = {date: index for index, date in enumerate(week_days)}
    today_week_num = datetime.today().weekday()
    return any(today_week_num == week_days_num[d.lower()] for d in days_of_week)


if today_is("Saturday"):
    add_trello_card_to(client, board_name="Daily", list_name="🥰😂😊😅", card_name="Cắt móng tay")

if today_is("Tuesday", "Thursday", "Saturday"):
    add_trello_card_to(client, board_name="Daily", list_name="🥰😂😊😅", card_name="Lau bàn học")

if today_is("Wednesday", "Saturday"):
    add_trello_card_to(client, board_name="Daily", list_name="🥰😂😊😅", card_name="Cho mấy bé uống sữa")
    add_trello_card_to(client, board_name="Daily", list_name="🥰😂😊😅", card_name="Đổ nước vô ấm đun")

# -----------------------