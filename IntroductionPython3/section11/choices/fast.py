from random import choice

places = ["McDonalds", "KFC", "Burger King", "Taco Bell", "Wendys", "Arbys", "Pizza Hut"]

def pick(): # 下にdocstringがあることに注目
    """ランダムにファーストフード店を選ぶ"""
    return choice(places)
