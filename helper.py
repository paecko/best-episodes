from bs4 import BeautifulSoup as bs4
from urllib2 import Request

def get_tvshow(no_pages):
    """ Returns list of TV shows by scraping them from IMDB, alog"""
    # Will contain dictionaries of tv shows
    link_list = []
    counter = 0
    while counter < no_pages:
        if counter == 0:
            url = "http://www.imdb.com/search/title?title_type=tv_series&view=simple&sort=moviemeter,asc"
        else:
            url = "http://www.imdb.com/search/title?title_type=tv_series&view=simple&sort=moviemeter,asc&page={}&ref_=adv_nxt".format(counter)
        page = Request.urlopen(url)
        soup = bs4(page,"html.parser")
        links = soup.find_all('a')
        ratings = soup.find_all("div", {"class": "col-imdb-rating"})
        rating_list = []
        for rating in ratings:
            rating_list.append(rating.text.strip())
        rating_count = 0
        for link in links:
            # Convert to str becuase link is a bs4 object
            link_str = str(link)
            # Other useless links on page. TV shows are those that contain the word 'title' from index 10:15
            # Other link tags also contain title at same position. So .
            sliced_check = link_str[10:15]
            if sliced_check == "title" and "<span>X</span>" not in link_str and  "<img alt=" not in link_str:
                #Name of tv show is after '>'
                index = link_str.index(">")
                #Till -4 because last substring is '</a>'
                name = link_str[index+1:-4]

                dict = {}
                dict['name'] = name
                dict['imdb_id'] = link_str[16:25]

                dict['rating'] = rating_list[rating_count]
                #Store a dict for each tv show in list
                link_list.append(dict)
                rating_count += 1
        counter += 1
    return link_list

def get_episodes(show):
    url = "http://www.imdb.com/title/{}/eprate".format(show)
    page = Request.urlopen(url)
    soup = bs4(page, "html.parser")

    table1 = soup.find('table')
    table1data = table1.find_all("td",text=True)

    episode_list = []
    dict_pos = -1
    counter=0

    for i in range(0,len(table1data)-1):
        if i % 4 == 0 or i == 0:
            dict = {}
            episode_list.append(dict)
            dict_pos += 1
            counter = 0

        if counter==0:
            data = table1data[i].text
            episode_list[dict_pos]["episode"] = data.replace(u'\xa0', u' ')
        elif counter==1:
            episode_list[dict_pos]["title"] = table1data[i].text
        elif counter==2:
            episode_list[dict_pos]["rating"] = table1data[i].text
        elif counter==3:
            episode_list[dict_pos]["no_votes"] = table1data[i].text
        counter += 1

    return episode_list

def get_link(show,episode):
    show = show.lower()
    show = show.lstrip('the ')

    dot_index = episode.find('.')
    episode_s = "s" + episode[:dot_index].zfill(2)
    episode_e = "e" + episode[dot_index + 1:].zfill(2)
    ep = episode_s + episode_e

    url = "http://www.alluc.ee/stream/{}+{}".format(show.replace(' ', '+'), ep)
    return url


def get_watch_links(show, episode):
    show = show.lower()
    show = show.lstrip('the ')

    dot_index = episode.find('.')
    episode_s = "s" + episode[:dot_index].zfill(2)
    episode_e = "e" + episode[dot_index+1:].zfill(2)
    ep = episode_s + episode_e

    url = "http://www.alluc.ee/stream/{}+{}".format(show.replace(' ', '+'), ep)
    print(url)

    page_req = Request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})
    page_con = Request.urlopen(page_req)
    soup = bs4(page_con, "html.parser")
    sources = soup.find_all("a", {"class": "source"}, limit=5)
    sources_list = []
    for source in sources:
        sources_list.append("www.alluc.ee" +  source['href'].lstrip())
    return sources_list

def format_episode(episode):
    dot_index = episode.find('.')
    return "Season {}, Episode {}".format(episode[0:dot_index], episode[dot_index+1:])

