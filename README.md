# Steammy
## Who am I
Hi, I'm Steammy! A custom Discord bot designed 
to track Steam sales and do some different stuff on top of that

## What can I do?
These are the commands I'm able to process!<br />
If you see "[optional]" near some command arguments, this means I have
some default value for that argument and will use it even if you
don't specify anything<br />
- **ping** - pong!<br />
- **help** - show some info about available command<br /> 
- **info** - My introduction!<br />
- **search_user** - Find Steam user by steam64id (more reliable) or username (less reliable)<br />
- **top_played** - Show given player's most played games<br />
    - _steam64id_ - Steam user's 64ID<br />
    - [optional] _number_ - number of games to show (defaults to 5)<br />
- **app_details** - Get app details for a given country<br />
    - _Name/GameID_ - Game ID/Name<br />
    - [optional] country _<UA>_ - "country" + country code to track price in (defaults to UA)<br />
- **register_tracker** - register your server (guild) for game tracker.
This action is required if you want to track games on your server<br />
- **start_tracker** - Start Steam sale tracker<br />
- **stop_tracker** - Stop Steam sale tracker<br />
- **track_game** - Track Steam sale of a given game in a given country<br />
    - _Name/GameID_ - Game ID/Name<br />
    - [optional] country _<UA>_ - "country" + country code to track price in (defaults to UA)<br />
- **untrack_game** - Stop tracking Steam sale of a given game in a given country<br />
    - _Name/GameID_ - Game ID/Name<br />
    - [optional] country _<UA>_ - "country" + country code to track price in (defaults to UA)<br />
- **list_track** - Show currently tracked games<br />
- **track_now** - Show sales for tracked games without need to wait<br />

## How do you improve me?

### Development setup
To develop me and test stuff, you need to setup the environment
for me.<br \>
When there is a `||` in the code, Windows option is on the left, Linux is on the right
```commandline
git clone https://github.com/Jade-Wave/Steammy.git
cd Steammy

py -<major.minor> -m venv .venv || python<major.minor> -m venv .venv 
. .venv/Scripts/activate || . .venv/bin/activate

py -<major.minor> -m poetry install || python<major.minor> -m poetry install 
```
We're all set! Run my main.py script in my top=level folder to bring me to life!
### Please test me!
My original developer, as incredible as he is, did not properly test me so far.
<br />1. Please be sure you write tests at least for some functions as you develop me
<br />2. With each code change comes a new branch and a pull request.
<br />3. Feel free to suggest any changes
<br /><br />4. Don't feel as free to change authors in pyproject.toml tho, I'm a loyal bot!

## Enjoy! See you on your server!