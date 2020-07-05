
import praw

# Load user accounts from praw.ini file
new_account = praw.Reddit("new_account")
old_account = praw.Reddit("old_account")

# Load options from praw.ini file
SUBREDDITS = new_account.config.custom['copy_subreddits'] == 'on'
FRIENDS = new_account.config.custom['copy_friends'] == 'on'
SAVED = new_account.config.custom['copy_saved_posts'] == 'on'
# Content Types:
#  0 => NSFW only
#  1 => SFW only
#  2 => NSFW + SFW
#
# This setting applies to subreddits and saved posts
CONTENT_TYPE = int(new_account.config.custom['content_type'])

def filter_nsfw_subreddits(subreddit):
    return subreddit.over18

def filter_nsfw_posts(post):
    return post.over_18


# ====================================================================================
# copy over the subreddits
print("Copy over subreddits: " + str(SUBREDDITS))
if SUBREDDITS:
    print("Fetching subreddits...")
    subreddits_old = list(old_account.user.subreddits(limit=None))

    # filter the nsfw subreddits
    nsfw = list(filter(filter_nsfw_subreddits, subreddits_old))

    print("Found " + str(len(subreddits_old)) + " subreddits including " + str(len(nsfw)) + " nsfw subreddits")

    # by default it is going to copy everything over
    subreddit_list = subreddits_old

    # determine what to subscribe to based on content_type
    if CONTENT_TYPE == 0:   # NSFW content only
        subreddit_list = nsfw
    elif CONTENT_TYPE == 1: # SFW only
        subreddit_list = [x for x in subreddits_old if x not in nsfw]


    # subscribe to the subreddits
    for subreddit in subreddit_list:
        new_account.subreddit(subreddit.display_name).subscribe()
        print("Subscribed to " + subreddit.display_name)


# ====================================================================================
# copy over the followers
# list(new_account.redditors.search('username'))[0].friend()
print("Copy over friends: " + str(FRIENDS))
if FRIENDS:
    print("Fetching friends...")
    friends = list(old_account.user.friends())
    print("Found " + str(len(friends)) + " friends")

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
    print("Fetching saved posts...")
    saved_posts = list(old_account.user.me().saved(limit=None))

    nsfw_posts = list(filter(filter_nsfw_posts, saved_posts))

    print("Found " + str(len(saved_posts)) + " saved posts including " + str(len(nsfw_posts)) + " nsfw saved posts")

    # by default it is going to copy everything over
    posts_list = saved_posts

    # determine what to save to based on content_type
    if CONTENT_TYPE == 0:  # NSFW content only
        posts_list = nsfw_posts
    elif CONTENT_TYPE == 1:  # SFW only
        posts_list = [x for x in saved_posts if x not in nsfw_posts]

    for post in posts_list:
        # Use a try except block in case there is some trouble saving a post
        try:
            new_account.submission(id=post.id).save()
            print("Saved post with id: " + post.id)
        except:
            continue
