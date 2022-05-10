import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])

        #特征词路径
        self.movie_path = os.path.join(cur_dir, 'data/movie.txt')  #os.path.join()路径拼接
        self.genre_path = os.path.join(cur_dir, 'data/genre.txt')
        self.date_path = os.path.join(cur_dir, 'data/date.txt')
        self.category_path = os.path.join(cur_dir, 'data/category.txt')
        self.time_path = os.path.join(cur_dir, 'data/time.txt')
        self.language_path = os.path.join(cur_dir, 'data/language.txt')
        self.director_path = os.path.join(cur_dir, 'data/director.txt')
        self.cast_path = os.path.join(cur_dir, 'data/cast.txt')
        self.synopsis_path = os.path.join(cur_dir, 'data/synopsis.txt')

        #加载特征词
        self.movie_wds = [str.strip() for str in open(self.movie_path, encoding="utf-8") if str.strip()]  #str.strip([chars])移除字符串头尾指定的字符序列
        self.genre_wds = [str.strip() for str in open(self.genre_path, encoding="utf-8") if str.strip()]
        self.date_wds = [str.strip() for str in open(self.date_path, encoding="utf-8") if str.strip()]
        self.category_wds = [str.strip() for str in open(self.category_path, encoding="utf-8") if str.strip()]
        self.time_wds = [str.strip() for str in open(self.time_path, encoding="utf-8") if str.strip()]
        self.language_wds = [str.strip() for str in open(self.language_path, encoding="utf-8") if str.strip()]
        self.director_wds = [str.strip() for str in open(self.director_path, encoding="utf-8") if str.strip()]
        self.cast_wds = [str.strip() for str in open(self.cast_path, encoding="utf-8") if str.strip()]
        self.synopsis_wds = [str.strip() for str in open(self.synopsis_path, encoding="utf-8") if str.strip()]

        self.region_words = set(self.movie_wds + self.genre_wds + self.date_wds + self.category_wds + self.time_wds + self.language_wds + self.director_wds + self.cast_wds + self.synopsis_wds)

        #构造actree
        self.region_tree = self.build_actree(list(self.region_words))

        #构建词典
        self.wdtype_dict = self.build_wdtype_dict()

        #问句疑问词
        self.movie_qwds = ['电影']
        self.genre_qwds = ['种类', '分类', '类别', "类型"]
        self.date_qwds = ['上映', '上映时间', '上映日期', '首播', '首播时间', '首播日期']
        self.time_qwds = ['时长', '多久', '多长时间', '持续时间']
        self.category_qwds = ['地区', '国家', '地方']
        self.language_qwds = ['语言', '语种']
        self.director_qwds = ['导演', '编导', '执导']
        self.cast_qwds = ['演员', '主演']
        self.synopsis_qwds = ['剧情', '讲述', '情节', '内容']

        print("Model init finished...")
        return

    def classify(self, question):
        data = {}
        question_dict = self.check_question(question)
        if not question_dict:
            return{}
        data['args'] = question_dict
        #收集问句中所涉及到的实体类型
        types = []
        for type_ in question_dict.values():
            types += type_
        #print("types:", types)

        question_types = []

        # 电影分类
        if self.check_words(self.genre_qwds, question) and ('movie' in types):
            question_type = 'movie_genre'
            question_types.append(question_type)
        # 某一分类的电影
        if self.check_words(self.movie_qwds, question) and ('genre' in types):
            question_type = 'genre_movie'
            question_types.append(question_type)
        #电影上映时间
        if self.check_words(self.date_qwds, question) and ('movie' in types):
            question_type = 'movie_date'
            question_types.append(question_type)
        # 电影时长
        if self.check_words(self.time_qwds, question) and ('movie' in types):
            question_type = 'movie_time'
            question_types.append(question_type)
        # 电影产地
        if self.check_words(self.category_qwds, question) and ('movie' in types):
            question_type = 'movie_category'
            question_types.append(question_type)
        # 电影语言
        if self.check_words(self.language_qwds, question) and ('movie' in types):
            question_type = 'movie_language'
            question_types.append(question_type)
        #电影导演
        if self.check_words(self.director_qwds, question) and ('movie' in types):
            question_type = 'movie_director'
            question_types.append(question_type)
        # 电影导演
        if self.check_words(self.cast_qwds, question) and ('movie' in types):
            question_type = 'movie_cast'
            question_types.append(question_type)
        # 电影剧情
        if self.check_words(self.synopsis_qwds, question) and ('movie' in types):
            question_type = 'movie_synopsis'
            question_types.append(question_type)

        #将多个分类结果合并，组装成字典
        data['question_types'] = question_types
        #print("data:", data)
        return data

    #构造词对应的类型
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.movie_wds:
                wd_dict[wd].append('movie')
            if wd in self.genre_wds:
                wd_dict[wd].append('genre')
            if wd in self.date_wds:
                wd_dict[wd].append('date')
            if wd in self.time_wds:
                wd_dict[wd].append('time')
            if wd in self.language_wds:
                wd_dict[wd].append('language')
            if wd in self.director_wds:
                wd_dict[wd].append('director')
            if wd in self.synopsis_wds:
                wd_dict[wd].append('synopsis')
        return wd_dict

    #构造actree,加速过滤
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    #问句过滤：
    def check_question(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}
        #print("final_dict:", final_dict)
        return final_dict

    #基于特征词进行分类
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False

if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
