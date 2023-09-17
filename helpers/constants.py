from collections import defaultdict

class Format:
    DEFAULT_PAGE_SIZE = 10
    SIZE_PPREV = -5
    SIZE_PREV = -1
    SIZE_NEXT = 1
    SIZE_NNEXT = 5
    EMBED_INLINE_THRESHOLD = 150

class Color:
    ROYAL_BLUE = 0x0072BD
    BURNT_ORANGE = 0xD95319
    GOLDEN_YELLOW = 0xEDB120
    DEEP_PURPLE = 0x7E2F8E
    LIME_GREEN = 0x77AC30
    DODGER_BLUE = 0x4DBEEE
    CRIMSON_RED = 0xA2142F
    CERULEAN_BLUE = 0x2A52BE

class SpecialChars:
    AMOGUS = 'ඞ'
    LENNY = '( ͡° ͜ʖ ͡°)'
    CHARMAP = {
        'amogus': AMOGUS,
        'lenny': LENNY
    }

class Emojis:
    PREV = '\U000025C0'
    PPREV = '\U000023EA'
    NEXT = '\U000025B6'
    NNEXT= '\U000023E9'

class Link:
    INVITE = 'https://discord.com/api/oauth2/authorize?client_id=1134186264430649404&permissions=534925277248&scope=bot'

class Attach:
    class External:
        THATSROUGHBUDDY = 'https://tenor.com/view/my-first-girlfriend-turned-into-the-moon-thats-rough-that-rough-buddy-avatar-avatar-the-last-airbender-gif-5710468'
        RATJAM = 'https://cdn.discordapp.com/emojis/792904817479122944.gif?v=1'
    class File:
        RATTOSPACE = 'assets/fun/rat_to_space.mp4'
        BOUNCE = 'assets/fun/bounce.webm'

class UnitConversion:
    mi_km = 1.609344

class Wows:
    class Emojis:
        logo = '<:wows_logo:1147753092599779439>'
        silver = '<:wows_credits:1147753069543706734>'
        gold = '<:wows_gold:1147753079958143056>'
        xp = '<:wows_xp:1147753117950152744>'
        damage_caused = '<:wows_damage_caused:1147761900961144882>'
        damage_spotting = '<:wows_damage_spotting:1147761898599747615>'
        damage_tanked = '<:wows_damage_potential:1147761899908382741>'
        kill_ribbon = '<:wows_ribbon_kill:1147946461120712755>'
        mainbattery_ribbon = '<:wows_ribbon_mainbattery:1147946462412546208>'
        secondary_ribbon = '<:wows_ribbon_secondary:1147946458679619695>'
        torpedo_ribbon = '<:wows_ribbon_torpedo:1147946463930875955>'
        spotted_ribbon = '<:wows_ribbon_spotted:1147753136119885965>'
        captured_ribbon = '<:wows_ribbon_captured:1147755076459450458>'
        defended_ribbon = '<:wows_ribbon_defended:1147755090770411540>'
        planekill_ribbon = '<:wows_ribbon_planekill:1147757790954266726>'
        randoms = '<:wows_randombattle:1147753107393089617>'
    
    ship_index = defaultdict(str)
    ship_id_index = defaultdict(str)
    tier_roman = {
        1: 'I',
        2: 'II',
        3: 'III',
        4: 'IV',
        5: 'V',
        6: 'VI',
        7: 'VII',
        8: 'VIII',
        9: 'IX',
        10: 'X',
        11: '★',
    }
    ship_nationality = {
        "commonwealth": "Commonwealth",
        "europe": "European",
        "netherlands": "Dutch",
        "italy": "Italian",
        "usa": "American",
        "pan_asia": "Pan-Asian",
        "france": "French",
        "ussr": "Soviet",
        "germany": "German",
        "uk": "British",
        "japan": "Japanese",
        "spain": "Spanish",
        "pan_america": "Pan-American"
    }
    ship_nation = {
        "commonwealth": "Commonwealth",
        "europe": "Europe",
        "netherlands": "The Netherlands",
        "italy": "Italy",
        "usa": "U.S.A.",
        "pan_asia": "Pan-Asia",
        "france": "France",
        "ussr": "U.S.S.R.",
        "germany": "Germany",
        "uk": "U.K.",
        "japan": "Japan",
        "spain": "Spain",
        "pan_america": "Pan-America"
    }
    ship_type = {
        "Destroyer": "Destroyer",
        "AirCarrier": "Aircraft Carrier",
        "Battleship": "Battleship",
        "Cruiser": "Cruiser",
        "Submarine": "Submarine"
    }
    ship_type_image = {
        "Destroyer": {
            "image_premium": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Destroyer/premium_9ffc494df739f989c98f2dd3a4e40887299a30d3dfd5b146e85d7ddd08f63744.png",
            "image": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Destroyer/standard_357acc9fc0e2f7d98f047c99edffad359a8c45f2093024400fef2b9abbaf3a59.png",
            "image_elite": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Destroyer/elite_d4fa1bfbf1f8ca4c5a9ae5e92ccfd4ba66369d93b4e6e3f3880551059cecda22.png"
        },
        "AirCarrier": {
            "image_premium": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/AirCarrier/premium_4516ee494bb0396e51796cebff5e45c3f448d9790e0a58082057b8949ed9a3f8.png",
            "image": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/AirCarrier/standard_9f372d47b4fa5b5bbd79a3aaac816cb8d5343fa93949cce8934d94b84751b88e.png",
            "image_elite": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/AirCarrier/elite_8c5dbbe68e07b0a72c57a04a3d98baadc528f058be3a2e7b198fabeb07172330.png"
        },
        "Battleship": {
            "image_premium": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Battleship/premium_1d0cabf1997104fd727039ab9c09819260343ab3a9e862f361434d7f42270eb3.png",
            "image": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Battleship/standard_1468cf2ed1dc129ec4db4d9d18306bd06abb0d6b08c805dc94fe23ce6187c119.png",
            "image_elite": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Battleship/elite_9fe36e82e214ad6f8dcc305bf8d10d3d0fe35c64628611d9a39f3af01382a567.png"
        },
        "Cruiser": {
            "image_premium": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Cruiser/premium_1114542bcd311c388080eea3a4d54a7ea6fdc8706b019fcbf16ace9951f3a000.png",
            "image": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Cruiser/standard_44b68c918edc534e1367cb6512e9e8cc4d28aa54d237db820f1bbba867266742.png",
            "image_elite": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Cruiser/elite_127b2a5f66ce04425e45721020a88ed6d6cad202e186f39577cbcd91dd205fe3.png"
        },
        "Submarine": {
            "image_premium": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Submarine/premium_2da34d2e1f5f4934406d60eb020c1b107857405618c03bbe7710d502b24a5b8b.png",
            "image": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Submarine/standard_261525e5aae827700eaad3b5c3ab72d1721446ecab80226394fd30e9186d8a2d.png",
            "image_elite": "https://wows-gloss-icons.wgcdn.co/icons/vehicle/types/Submarine/elite_48fb6cc4ac86f63e8833e16ac1f7e996f86da5884c3e1b87da9b5ea324f3d5e4.png"
        }
    }