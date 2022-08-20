from types import SimpleNamespace

from src.utils.keyboard import create_keyboards

# necessary keys for the Bot
# you can add your intended emojis' text along as well
keys = SimpleNamespace(
    connect='Connect :link:',
    settings='Settings :gear:',
    exit='Hang Up :cross_mark:',
    yes="Yes :thumbs_up:",
    no="No :thumbs_down:"
)

keyboards = SimpleNamespace(
    main=create_keyboards(keys.connect, keys.settings),
    discard=create_keyboards(keys.exit),
    options=create_keyboards(keys.yes, keys.no)
)

states = SimpleNamespace(
    random_connect="Searching",
    main="Main",
    connected="Connected"
)
