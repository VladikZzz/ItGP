from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup


class States(Helper):
    PROMO_CODE = ListItem()
    SEND_TO_ALL = ListItem()
    TYPE_DATE = ListItem()
    CHANGE_DATE = ListItem()
    CHANGE_MIN_LIMIT = ListItem()
    COIN_ADDRESS = ListItem()
    NEW_COIN_ADDR = ListItem()
    COIN_AMOUNT_OUT = ListItem()
    CHOOSE_COIN_FOR_TRADE = ListItem()
    NEW_FAKE_AMOUNT = ListItem()
    NEW_FAKE_COUNT = ListItem()
    NEW_FAKE_MAX = ListItem()
    NEW_FAKE_MIN = ListItem()
    FAKE_DES = ListItem()
    FAKE_MAX_LIMIT = ListItem()
    FAKE_MIN_LIMIT = ListItem()
    FAKE_DATE = ListItem()
    FAKE_TRADE_AMOUNT = ListItem()
    FAKE_TRADE_NUMBER = ListItem()
    FAKE_NAME = ListItem()
    MIN_LIMIT_STATE = ListItem()
    TYPE_TRADE_AMOUNT = ListItem()
    TYPE_PERCENT = ListItem()
    AD_DES_STATE = ListItem()
    AD_AMOUNT = ListItem()
    TRX_AMOUNT_OUT = ListItem()
    ADD_TRX_ADDRESS = ListItem()
    USDT_AMOUNT_OUT = ListItem()
    ADD_ADDRESS = ListItem()
    LINK = ListItem()
    TYPE_AMOUNT = ListItem()
    CHOOSE_COIN = ListItem()
    TYPE_LIMIT = ListItem()
    CHANGE_LIMIT = ListItem()
    BANNED = ListItem()
    UNBAN_USR = ListItem()
    BAN_USR = ListItem()
    TYPE_TOKEN = ListItem()
    DEL_COIN = ListItem()
    ADDRESS = ListItem()
    NETWORK = ListItem()
    ADD_TIKER = ListItem()
    mode = HelperMode.snake_case
    UNAUTHORIZED_STATE = ListItem()
    USER_STATE = ListItem()
    ADMIN_STATE = ListItem()
    ADD_TOKEN = ListItem()
    ADD_ID = ListItem()
    LIMIT = ListItem()
    DEL_USR = ListItem()