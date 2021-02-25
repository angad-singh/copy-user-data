# copy-user-data

A short script to copy your user data from your old Reddit account to your new one. User data includes subreddits, friends and saved posts. This script uses [PRAW](https://praw.readthedocs.io/en/latest/index.html) and Python 3 to interact with the Reddit API.

## Getting Started
To get started, you are going to need a few things:
- Install PRAW on your local machine
- Old Reddit account credentials
- New Reddit account credentials
- client_id and client_secret

### Installing PRAW
To install PRAW, run the following command in your terminal
```
pip3 install -r requirements.txt
```
You can also install PRAW manually by following the instructions given [here](https://github.com/praw-dev/praw#installation)

### Client_id and Client_secret
client_id and client_secret are used to authorize this script to alter accounts and interact with Reddit's API. You can follow the instructions [here](https://redditclient.readthedocs.io/en/latest/oauth/) or [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example) to generate these 2 pieces of information for both the accounts. Take note of these 2 pieces of info on both your accounts.

Rename `praw_sample.ini` to `praw.ini`. Fill in the `client_id` and `client_secret` fields under the `[new_account]` and `[old_account]` sites with the corresponsing pieces of information. 

A less secure way is to use one set of keys and add your other account as a "Developer" on the script.

### Reddit Accounts
Continuing from the above step, fill in the credentials for your Reddit accounts under `[new_account]` and `[old_account]` sites.

## Configuring
Now you are all set to start configuring your migration!

This script provides the option to copy either your subscribed subreddits or your friends or your saved posts or all of these things if you wish. If you look in your `praw.ini` file, you will see the following:
```
# Set the values to off if you don't want to copy that piece of data 
# over to the new account
copy_subreddits=on
copy_friends=on
copy_saved_posts=on
```

You can selectively copy data by changing the value from  `on` to `off`

You can also configure what type of data gets migrated for subreddits and saved posts. You can choose to either copy only the SFW posts or copy only the NSFW posts or both. To select between these, you need to change the content type in the `praw.ini` file:
```
# Select your content type
#  0 => NSFW only
#  1 => SFW only
#  2 => NSFW + SFW
#
# This setting applies to subreddits and saved posts
content_type=1
```

## Usage
Now you are ready to start the migration of your old data to your new Reddit account! Simply open a terminal and navigate to the script's directory. Make sure that `praw.ini` file is in the same directory as the script. Execute the following command:
```
$ python3 copy_user_data.py 
```
