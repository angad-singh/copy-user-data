
import praw

# Load user accounts from praw.ini file
new_account = praw.Reddit("new_account")
old_account = praw.Reddit("old_account")

# Load options from praw.ini file
SUBREDDITS = new_account.config.custom['copy_subreddits'] == 'on'
FRIENDS = new_account.config.custom['copy_friends'] == 'on'
SAVED = new_account.config.custom['copy_saved_posts'] == 'on'
CONTENT_TYPE = int(new_account.config.custom['content_type'])

def filter_nsfw_subreddits(subreddit):
    return subreddit.over18

def filter_nsfw_posts(post):
    return post.over_18



# ====================================================================================
# copy over the subreddits
print("Copy over subreddits: " + str(SUBREDDITS))
if SUBREDDITS:
    subreddits_old = list(old_account.user.subreddits(limit=None))

    # filter the nsfw subreddits
    nsfw = list(filter(filter_nsfw_subreddits, subreddits_old))

    # subscribe to the subreddits
    for subreddit in nsfw:
        new_account.subreddit(subreddit.display_name).subscribe()
        print("Subscribed to " + subreddit.display_name)


# ====================================================================================
# copy over the followers
# list(new_account.redditors.search('username'))[0].friend()
print("Copy over friends: " + str(FRIENDS))
if FRIENDS:
    friends = list(old_account.user.friends())

    for friend in friends:
        person_list = list(new_account.redditors.search(friend.name))
        # If the account still exists
        if len(person_list) > 0:
            person_list[0].friend()
            print("Started following: " + friend.name)


# ====================================================================================
# copy over the saved stuff
# new_account.submission(id=post.id).save()
print("Copy over saved posts: " + str(SAVED))
if SAVED:
    saved_posts = list(old_account.user.me().saved(limit=None))

    nsfw_posts = list(filter(filter_nsfw_posts, saved_posts))

    for post in nsfw_posts:
        # Use a try except block in case there is some trouble saving a post
        try:
            new_account.submission(id=post.id).save()
            print("Saved post with id: " + post.id)
        except:
            continue
