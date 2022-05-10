class QuestionPaser:
    #构建实体结点
    def build_entity(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    #解析主函数
    def parser_main(self, res_classify):
        #提取出实体
        args = res_classify['args']
        entity_dict = self.build_entity(args)
        #提取出查询类型
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'movie_genre':
                sql = self.sql_transfer(question_type, entity_dict.get('movie'))
            elif question_type == 'genre_movie':
                sql = self.sql_transfer(question_type, entity_dict.get('genre'))
            elif question_type == 'movie_date':
                sql = self.sql_transfer(question_type, entity_dict.get('movie'))
            elif question_type == 'movie_time':
                sql = self.sql_transfer(question_type, entity_dict.get('movie'))
            elif question_type == 'movie_category':
                sql = self.sql_transfer(question_type, entity_dict.get('movie'))
            elif question_type == 'movie_language':
                sql = self.sql_transfer(question_type, entity_dict.get('movie'))
            elif question_type == 'movie_director':
                sql = self.sql_transfer(question_type, entity_dict.get('movie'))
            elif question_type == 'movie_cast':
                sql = self.sql_transfer(question_type, entity_dict.get('movie'))
            elif question_type == 'movie_synopsis':
                sql = self.sql_transfer(question_type, entity_dict.get('movie'))

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        return sqls

    #对不同的问题分开处理
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []
        #查询语句
        sql = []
        #查询电影分类
        if question_type == 'movie_genre':
            sql = ["match (m:Movie)-[r:movie_and_genre]->(n:Genre) where m.name='{0}' return m.name, n.name".format(i) for i in entities]
        #查询某一分类的电影
        elif question_type == 'genre_movie':
            sql = ["match (m:Genre)-[r:movie_and_genre]->(n:Movie) where n.name='{0}' return m.name, n.name".format(i) for i in entities]
        #查询电影上映时间
        elif question_type == 'movie_date':
            sql = ["match (m:Movie)-[r:movie_and_date]->(n:Date) where m.name='{0}' return m.name, n.name".format(i) for i in entities]
        # 查询电影时长
        elif question_type == 'movie_time':
            sql = ["match (m:Movie)-[r:movie_and_time]->(n:Time) where m.name='{0}' return m.name, n.name".format(i) for i in entities]
        # 查询电影产地
        elif question_type == 'movie_category':
            sql = ["match (m:Movie)-[r:movie_and_category]->(n:Category) where m.name='{0}' return m.name, n.name".format(i) for i in entities]
        # 查询电影语言
        elif question_type == 'movie_language':
            sql = ["match (m:Movie)-[r:movie_and_language]->(n:Language) where m.name='{0}' return m.name, n.name".format(i) for i in entities]
        # 查询电影导演
        elif question_type == 'movie_director':
            sql = ["match (m:Movie)-[r:movie_and_director]->(n:Director) where m.name='{0}' return m.name, n.name".format(i) for i in entities]
        # 查询电影演员
        elif question_type == 'movie_cast':
            sql = ["match (m:Movie)-[r:movie_and_cast]->(n:Cast) where m.name='{0}' return m.name, n.name".format(i) for i in entities]
        #查询电影剧情
        elif question_type == 'movie_synopsis':
            sql = ["match (m:Movie)-[r:movie_and_synopsis]->(n:Synopsis) where m.name='{0}' return m.name, n.name".format(i) for i in entities]

        return sql

if __name__ == '__main__':
    handler = QuestionPaser()