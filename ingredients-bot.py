import praw # you probably know what this is
import prawcore
import os
import requests # for web scraping
import bs4 # for web scraping
reddit = praw.Reddit('ingredients-bot',user_agent = "bot by u/shitpowosting")
mentions = reddit.inbox.stream() # gets inbox mention ids
for mention in mentions:
    if (reddit.inbox.unread() and reddit.inbox.mentions()):
        query = [] # your search keywords
        results = [] # your desired links
        searchstring = "https://www.skincarisma.com/search?utf8=%E2%9C%93&q=" # search
        query = mention.body.split("ingredients-bot")[-1].split() # turns user entered keywords after your mention into a list
        for item in query:  # adds keywords into the string you will use to make a search
            searchstring+=item+"+"
        searchstring = searchstring[:-1] # takes out the last "+"
        soup = bs4.BeautifulSoup(requests.get(searchstring).text,'html.parser') # human readable html
        for link in soup.find_all('a',href = True): # gets all links on page and adds desired links into results
            if str(link['href'])[1:9] == "products":
                results.append("https://www.skincarisma.com"+str((link['href'])))
        replytext = " ".join(query)
        if len(results) > 2: # tells user their search was too vague
            mention.reply("Your search yielded "+ str(int(len(results)/2)) + " results. Did you mean [this]("+(results[0])+")?")
        elif len(results) == 0: # tells user their search did not yield results
            mention.reply("Your search did not yield any results. Please try again with different keywords.")
        else: # responds to user with appropriate link
            mention.reply("["+replytext+"]("+(results[0])+")")
        mention.mark_read() # marks message as read so your bot doesn't keep streaming it
