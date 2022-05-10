import os
import json
from py2neo import Graph, Node, Relationship

class MovieGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'prepare_data/data.json')
        self.graph = Graph('http://localhost:7474', username='neo4j', password='926909')

    #读取文件
    def read_nodes(self):
        #节点
        movies = []
        genres = []
        dates = []      #上映时间
        categories = []
        times = []      #电影时长
        languages = []
        directors = []  #导演
        casts = []     #演员
        synopses = []  #电影简介

        movie_info = []  # 电影信息

        # 节点之间的关系
        movie_and_genre = []
        movie_and_date = []
        movie_and_category = []
        movie_and_time = []
        movie_and_language = []
        movie_and_director = []
        movie_and_cast = []
        movie_and_synopsis = []

        f = open(self.data_path, 'r', encoding='utf-8')
        data_jsons = json.load(f)  # data_json:list类型数据

        for data_json in data_jsons:
            movie_dict = {}

            movie_dict['movie'] = ''
            movie_dict['genre'] = ''
            movie_dict['date'] = ''
            movie_dict['category'] = ''
            movie_dict['time'] = ''
            movie_dict['language'] = ''
            movie_dict['director'] = ''
            movie_dict['cast'] = ''
            movie_dict['synopsis'] = ''

            # 将movies,genres,...列表数据转为集合数据(集合不能有重复数据)
            s_movies = set(movies)
            s_genres = set(genres)
            s_dates = set(dates)
            s_categories = set(categories)
            s_times = set(times)
            s_languages = set(languages)
            s_directors = set(directors)
            s_casts = set(casts)
            s_synopses = set(synopses)

            if 'movie' in data_json:
                movies += data_json['movie']
                for movie in data_json['movie']:
                    print(movie)
                movie_dict['movie'] = data_json['movie']
            if 'genre' in data_json:
                genres += data_json['genre']
                for genre in data_json['genre']:
                    movie_and_genre.append([movie, genre])
                movie_dict['genre'] = data_json['genre']
            if 'date' in data_json:
                dates += data_json['date']
                for date in data_json['date']:
                    movie_and_date.append([movie, date])
                movie_dict['date'] = data_json['date']
            if 'category' in data_json:
                categories += data_json['category']
                for category in data_json['category']:
                    movie_and_category.append([movie, category])
                movie_dict['category'] = data_json['category']
            if 'time' in data_json:
                times += data_json['time']
                for time in data_json['time']:
                    movie_and_time.append([movie, time])
                movie_dict['time'] = data_json['time']
            if 'language' in data_json:
                languages += data_json['language']
                for language in data_json['language']:
                    movie_and_language.append([movie, language])
                movie_dict['language'] = data_json['language']
            if 'director_name' in data_json:
                directors += data_json['director_name']
                for director in data_json['director_name']:
                    movie_and_director.append([movie, director])
                movie_dict['director'] = data_json['director_name']
            if 'cast' in data_json:
                casts += data_json['cast']
                for cast in data_json['cast']:
                    movie_and_cast.append([movie, cast])
                movie_dict['cast'] = data_json['cast']
            if 'synopsis' in data_json:
                synopses += data_json['synopsis']
                for synopsis in data_json['synopsis']:
                    movie_and_synopsis.append([movie, synopsis])
                movie_dict['synopsis'] = data_json['synopsis']

            movie_info.append(movie_dict)

        return movies, genres, dates, categories, times, languages, directors, casts, synopses, movie_info, \
               movie_and_genre, movie_and_date, movie_and_category, movie_and_time, movie_and_language, movie_and_director, movie_and_cast, movie_and_synopsis

    #建立节点
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''''
    #创建知识图谱中心的节点
    def create_movies_nodes(self, movie_info):
        count = 0
        for movie_dict in movie_info:
            node = Node('Movie', name=movie_dict['movie'], genre=movie_dict['genre'], date=movie_dict['date'], category=movie_dict['category'],
                        time=movie_dict['time'], language=movie_dict['language'], director=movie_dict['director'], cast=movie_dict['cast'], synopsis=movie_dict['synopsis'])
            self.graph.create(node)
            count += 1
            print(count)
        return
    '''''


    #创建知识图谱其他实体节点
    def create_graphnodes(self):
        movies, genres, dates, categories, times, languages, directors, casts, synopses, movie_info, movie_and_genre, movie_and_date, movie_and_category, movie_and_time,  movie_and_language, movie_and_director, movie_and_cast, movie_and_synopsis = self.read_nodes()
        #self.create_movies_nodes(movie_info)
        self.create_node('Movie', movies)
        self.create_node('Genre', genres)
        self.create_node('Date', dates)
        self.create_node('Category', categories)
        self.create_node('Time', times)
        self.create_node('Language', languages)
        self.create_node('Director', directors)
        self.create_node('Cast', casts)
        self.create_node('Synopsis', synopses)
        return

    #创建实体关系边

    def create_graphrels(self):
        movies, genres, dates, categories, times, languages, directors, casts, synopses, movie_info, movie_and_genre, movie_and_date, movie_and_category, movie_and_time,  movie_and_language, movie_and_director, movie_and_cast, movie_and_synopsis = self.read_nodes()
        self.create_relationship('Movie', 'Genre', movie_and_genre, 'movie_and_genre', '类型')
        self.create_relationship('Movie', 'Date', movie_and_date, 'movie_and_date', '上映时间')
        self.create_relationship('Movie', 'Category', movie_and_category, 'movie_and_category', '类别')
        self.create_relationship('Movie', 'Time', movie_and_time, 'movie_and_time', '时长')
        self.create_relationship('Movie', 'Language', movie_and_language, 'movie_and_language', '语言')
        self.create_relationship('Movie', 'Director', movie_and_director, 'movie_and_director', '导演')
        self.create_relationship('Movie', 'Cast', movie_and_cast, 'movie_and_cast', '演员')
        self.create_relationship('Movie', 'Synopsis', movie_and_synopsis, 'movie_and_synopsis', '剧情')

    #建立关联
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query ="match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            print(query)
            try:
                self.graph.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    #导出数据
    def export_data(self):
        movies, genres, dates, categories, times, languages, directors, casts, synopses, movie_info, movie_and_genre, movie_and_date, movie_and_category, movie_and_time,  movie_and_language, movie_and_director, movie_and_cast, movie_and_synopsis = self.read_nodes()
        f_movie = open('data/movie.txt', 'w+')
        f_genre = open('data/genre.txt', 'w+')
        f_date = open('data/date.txt', 'w+')
        f_category = open('data/category.txt', 'w+')
        f_time = open('data/time.txt', 'w+')
        f_language = open('data/language.txt', 'w+')
        f_director = open('data/director.txt', 'w+')
        f_cast = open('data/cast.txt', 'w+')
        f_synopsis = open('data/synopsis.txt', 'w+')

        f_movie.write('\n'.join(list(movies)))
        f_genre.write('\n'.join(list(genres)))
        f_date.write('\n'.join(list(dates)))
        f_category.write('\n'.join(list(categories)))
        f_time.write('\n'.join(list(times)))
        f_language.write('\n'.join(list(languages)))
        f_director.write('\n'.join(list(directors)))
        f_cast.write('\n'.join(list(casts)))
        f_synopsis.write('\n'.join(list(synopses)))

        f_movie.close()
        f_genre.close()
        f_date.close()
        f_category.close()
        f_time.close()
        f_language.close()
        f_director.close()
        f_cast.close()
        f_synopsis.close()
        return


if __name__ == '__main__':
    handler = MovieGraph()
    print("step1:导入图谱节点中")
    handler.create_graphnodes()
    print("step2:导入图谱边中")
    handler.create_graphrels()
    print("step3:把数据分类导入txt文件中")
    handler.export_data()


