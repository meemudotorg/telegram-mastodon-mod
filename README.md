# what

a python script that watches a server's timeline using the streaming api and sends messages to a telegram user/chat when the message matches specified criteria

this basically just patches python-telegram-bot and Mastodon.py together

I have 0 idea how this would work with a very large instance, but the instance this is written for is small enough that this is about all we need.

# why

because i'm lazy and can't watch a timeline all day and spammers tend to do the same thing over and over

tangentially inspired by the existence of reddit's automoderator which improved mods lives tenfold.

# how

you have to create your own telegram bot and store your api key in the settings file

you need to fetch the id of the chat you want to interact with, and add that too.

also, create a mastodon account and give it mod rights. I don't recommend making it an admin or using your own account, because I can't guarantee this is particularly good or secure.


then start up the virtual environment and run python masto-mod.py --init and follow the prompts.
it will make two files `pytooter_clientcred.secret` and `pytooter_usercred.secret` for god's sake DO NOT SHARE THESE 

after that, you can run it with python masto-mod.py and let it sit there and do its thing

you could probably run this on heroku or something pretty easily.

# bugs

this script is pretty much written for me, but i'm putting it out here in case anyone else finds it useful
i can't promise timely fixes to bugs or support, but people are welcome to fork/make pull requests/do what they will with it.

# future

Potential future features:
    - Ability to inform a chat when a new instance is discovered
    - Ability to mark all media incoming from particular instances as sensitive
    - Automatically hide specific CWs from the fedi timeline
    - Interactive chat commands for the mod chat.