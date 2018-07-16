from collections import defaultdict
import heapq
from operator import itemgetter

class SlopeOne(object):

    def __init__(self):
        self.dev = defaultdict(lambda: defaultdict(float))
        self.n = defaultdict(lambda: defaultdict(int))

    def train(self, users_dict):
        for user in users_dict.values():
            for i_id, i_rating in user.items():
                for j_id, j_rating in user.items():
                    self.n[i_id][j_id] += 1
                    self.dev[i_id][j_id] += i_rating - j_rating
        for i_id, i_ratings in self.dev.items():
            for j_id in i_ratings:
                i_ratings[j_id] /= self.n[i_id][j_id]

    def get_recommendations(self, user_ratings, m=5):
        estimated_ps = defaultdict(float)
        n = defaultdict(int)

        for user_id, user_rating in user_ratings.items():
            for model_id, model_ratings in self.dev.items():
                if user_id not in self.n[model_id]:
                    continue
                cross_n = self.n[model_id][user_id]
                estimated_ps[model_id] += cross_n * (model_ratings[user_id] + user_rating)
                n[model_id] += cross_n

        for book_id, p in estimated_ps.items():
            if book_id not in n or book_id in user_ratings:
                estimated_ps[book_id] = 0
            else:
                estimated_ps[book_id] = p / n[book_id]

        m_top = heapq.nlargest(m, estimated_ps.items(), key=itemgetter(1))
        s = [book_id for (book_id, p) in m_top]
        return s
