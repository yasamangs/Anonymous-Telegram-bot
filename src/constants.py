from types import SimpleNamespace
from src.utils.keyboard import create_keyboars

# basic keys for creating a Bot 
# you can add your intended emojis' text along as well
keys = SimpleNamespace(
    start='start:',
    settings='Settings :gear:'
)

keyboards = SimpleNamespace(
    main=create_keyboars(keys.random_connect, keys.settings)
)
