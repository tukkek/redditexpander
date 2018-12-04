# reddit expander

**Requires Python 3.6 (or higher) and urllib3 (`pip install urllib3`).**

## Usage

To use, call this script from a command line with one or more subreddits that you want to find similar ones to. For example:

    python3 redditexpander.py me_irl metal_me_irl anime_irl
    
Another example, if you want to discover new popular subs starting from `r/all`:

    python3 redditexpander.py all

Results will be printed to the command line output and written to an HTML file (`result.html`).

## How it works

The script will look at the front page of each subreddit you provide and from there look at each OP's submission history to see where else they are posting. This has one major benefit and deficit:

* The benefit being that you can run this script often and get new results (as long as new content is being posted in the subs regurlarly)
* The deficit is that this isn't a partiularly smart strategy, so unrelated subreddits may appear as long as any one OP is posting to them

The result set is ordered by upvotes, in an attempt to have the more popular subreddits appear on top (since you probably don't want to waste time looking at subs that don't have a lot of activity). Ideally it would be possible to use subreddit subscriber counts for that but sadly reddit API's data delivery on this seems to be irregular.

