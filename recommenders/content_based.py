import re
import nltk
from nltk.corpus import stopwords
import pandas as pd
from typing import Dict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .base import BaseModel

class ContentBasedRecommender(BaseModel):
    def __init__(self, train_count: pd.DataFrame, test_count: pd.DataFrame):
        super().__init__(train_count, test_count)
        nltk.download('stopwords')

        self.REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
        self.BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
        self.STOPWORDS = set(stopwords.words('english'))

    def fit(self, train_data: pd.DataFrame, service_data: pd.DataFrame, ngram_range= (1,1)):
        self.train_data = train_data[train_data['description'].notna()]
        self.service_data = service_data[service_data['description'].notna()]

        self.train_data.loc[:, ['description_clean']] = self.train_data['description'].apply(self.clean_text)
        self.service_data.loc[:, ['description_clean']] = self.service_data['description'].apply(self.clean_text)

        self.users = self.train_data['user'].unique()

        self.service_data.reset_index(inplace=True)
        self.index_to_item = self.service_data['objectId'].to_dict()
        self.item_to_index = {value: key for key, value in self.index_to_item.items()}

        self.tfidf = TfidfVectorizer(analyzer="word", ngram_range=ngram_range, min_df=0, stop_words="english")
        self.tfidf_matrix = self.tfidf.fit_transform(self.service_data["description_clean"])
        self.cosine_similarities = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def rank_items(self):
        content_based_rankings = {}
        for user in self.users:
            user_rankings = self.get_user_rankings(user_id=user)
            user_rankings = pd.DataFrame.from_dict(user_rankings, orient="index", columns=["score"])
            user_rankings = user_rankings.sort_values(by="score", ascending=False)
            content_based_rankings[user] = user_rankings.index.values

        return content_based_rankings

    def clean_text(self, text):
        """
            text: a string
            
            return: modified initial string
        """
        text = text.lower() # lowercase text
        text = self.REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
        text = self.BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing. 
        text = ' '.join(word for word in text.split() if word not in self.STOPWORDS) # remove stopwords from text
        return text

    def get_knn(self, item_index: int, k: int = None, cosine_similarities = None):
        assert self.cosine_similarities is not None
        assert item_index >= 0 and item_index < self.cosine_similarities.shape[0]
        if k is None: k = self.cosine_similarities.shape[0]
        assert k >= 0

        if cosine_similarities is None: cosine_similarities = self.cosine_similarities

        score_series = pd.Series(cosine_similarities[item_index]).sort_values(ascending=False)
        top_k_indices = list(score_series.iloc[1 : k + 1].index)
        top_k_scores = list(score_series.iloc[1 : k + 1].values)
        return {index: score for index, score in zip(top_k_indices, top_k_scores)}

    def get_user_rankings(self, user_id: str) -> Dict:
        user_relations = self.train_data[self.train_data["user"] == user_id]
        user_items = user_relations['service'].values
        item_scores = {}
        for item in user_items:
            iid = self.item_to_index[item]
            nearest_indices = self.get_knn(item_index=iid)
            nearest_items = {self.index_to_item[idx]: score for idx, score in nearest_indices.items()}
            for neighbour_item in nearest_items:
                if neighbour_item in item_scores.keys():
                    if item_scores[neighbour_item] < nearest_items[neighbour_item]:
                        item_scores[neighbour_item] = nearest_items[neighbour_item]
                else:
                    item_scores[neighbour_item] = nearest_items[neighbour_item]
        return item_scores