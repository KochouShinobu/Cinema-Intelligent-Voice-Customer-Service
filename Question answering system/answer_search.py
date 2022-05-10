from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.graph = Graph( 'http://localhost:7474', username = 'neo4j' , password ='926909')
        self.num_limit = 20

    #执行cypher查询，并返回相应结果
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.graph.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    #根据对应的qustion_type，调用相应的回复模板
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        if question_type == 'movie_genre':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            #print("subject", subject)
            final_answer = '电影{1}的分类为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'genre_movie':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            print("subject", subject)
            final_answer = '分类为{1}的电影有：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movie_date':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '电影{1}的上映时间为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movie_time':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '电影{1}的时长为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movie_category':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '电影{1}的拍摄地为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movie_language':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '电影{1}的语言为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movie_director':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '电影{1}的导演为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movie_cast':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '电影{1}的演员为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'movie_synopsis':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '电影{1}的剧情为：{0}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()