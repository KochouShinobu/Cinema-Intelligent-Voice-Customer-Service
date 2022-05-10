import json
import requests
import re


def get_movie(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    }
    resp = requests.get(url, headers=headers)
    page_content = resp.text
    #print(page_content)
    # 解析数据
    obj = re.compile(r'<li.*?class="list-item".*?data-title="(?P<movie_name>.*?)".*?data-showed="True".*?data-subject="(?P<href>.*?)".*?>', re.S)
    # 开始匹配
    result = obj.finditer(page_content)

    all_list = []    #把数据保存到列表，然后结束的时候一次性写入json文件

    for it in result:
        movie = it.group("movie_name")
        print(movie)
        href = it.group("href")  #电影id 用于字符串拼电影的url
        url = "https://movie.douban.com/subject/" + href + "/?from=playing_poster"
        print(url)
        dicts = each_movie(movie, url)
        all_list.append(dicts)
        json_data = json.dumps(all_list, ensure_ascii=False)   # ensure_ascii=False，则返回值可以包含非ascii值
        try:
            with open('data.json', 'w+', encoding="utf-8") as f:
                f.write(json_data)
                f.close()
        except IOError as e:
            print(str(e))
        finally:
            f.close()

def each_movie(movie, href):
    url = href
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    }

    dicts = {}
    movies = []
    genres = []
    dates = []
    categories = []
    times = []
    languages = []
    directors = []
    casts = []
    synopses = []

    movies.append(movie)
    dicts['movie'] = movies

    resp = requests.get(url, headers=headers)
    page_content = resp.text
    #print(page_content)
    # 解析数据
    obj = re.compile(
        r'<div id="info">.*?导演.*?<a href=.*?rel="v:directedBy">(?P<director_name>.*?)'
        r'</a>.*?主演.*?<a href=.*?rel="v:starring">(?P<cast_names>.*?)'
        r'</a>.*?类型.*?<span property="v:genre">(?P<genre>.*?)'
        r'</span>.*?制片国家/地区.*?</span>(?P<category>.*?)'
        r'<br/>.*?语言.*?</span>(?P<language>.*?)'
        r'<br/>.*?上映日期.*?<span property="v:initialReleaseDate" content="(?P<date>.*?)">.*?'
        r'</span>.*?片长.*?<span property="v:runtime".*?>(?P<time>.*?)'
        r'</span>.*?<span property="v:summary" class="">(?P<synopsis>.*?)'
        r'</span>', re.S)


    # 开始匹配
    result = obj.finditer(page_content)
    for it in result:
        print((it.group("director_name")))
        print(it.group("cast_names"))
        print(it.group("genre"))
        print(it.group("category").strip())
        print(it.group("language").strip())
        print(it.group("date"))
        print(it.group("time"))
        print(it.group("synopsis").strip())

        genres.append(it.group("genre").strip())
        dates.append(it.group("date").strip())
        categories.append(it.group("category").strip())
        times.append(it.group("time").strip())
        languages.append(it.group("language").strip())
        directors.append(it.group("director_name").strip())
        casts.append(it.group("cast_names").strip())
        synopses.append(it.group("synopsis").strip())

        dicts['genre'] = genres
        dicts['date'] = dates
        dicts['category'] = categories
        dicts['time'] = times
        dicts['language'] = languages
        dicts['director_name'] = directors
        dicts['cast'] = casts
        dicts['synopsis'] = synopses

        return dicts

if __name__ == '__main__':
    url = 'https://movie.douban.com/cinema/nowplaying/chengdu/'
    get_movie(url)


