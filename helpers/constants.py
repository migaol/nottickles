from enum import Enum

class Format(Enum):
    WOWS_DEFAULT_PAGE_SIZE = 10
    WOWS_SIZE_PPREV = -5
    WOWS_SIZE_PREV = -1
    WOWS_SIZE_NEXT = 1
    WOWS_SIZE_NNEXT = 5

class Color(Enum):
    ROYAL_BLUE = 0x0072BD
    BURNT_ORANGE = 0xD95319
    GOLDEN_YELLOW = 0xEDB120
    DEEP_PURPLE = 0x7E2F8E
    LIME_GREEN = 0x77AC30
    DODGER_BLUE = 0x4DBEEE
    CRIMSON_RED = 0xA2142F
    CERULEAN_BLUE = 0x2A52BE

class SpecialChars(Enum):
    AMOGUS = 'ඞ'
    LENNY = '( ͡° ͜ʖ ͡°)'

class CharMap(Enum):
    CHARMAP = {
        'amogus': SpecialChars.AMOGUS.value,
        'lenny': SpecialChars.LENNY.value
    }

class Emojis(Enum):
    PREV = '\U000025C0'
    PPREV = '\U000023EA'
    NEXT = '\U000025B6'
    NNEXT= '\U000023E9'

class Link(Enum):
    INVITE = 'https://discord.com/api/oauth2/authorize?client_id=1134186264430649404&permissions=534925277248&scope=bot'

class Attach(Enum):
    BOUNCE = 'https://cdn.discordapp.com/attachments/704613785247154256/1006598759930658928/trim.A3677A18-771B-4390-B9B4-A1570B77FCA5_Bounce.webm'
    THATSROUGHBUDDY = 'https://tenor.com/view/my-first-girlfriend-turned-into-the-moon-thats-rough-that-rough-buddy-avatar-avatar-the-last-airbender-gif-5710468'
    