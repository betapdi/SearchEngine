from underthesea import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class Document:
    def __init__(self, data):
        self.data = data
        
    def processData(self, stopWords : set):
        self.tokens = word_tokenize(self.data["content"])
        # print(stopWords)
        
        # remove stopwords and punctation
        self.tokens = [token for token in self.tokens if ((token not in stopWords))]
        self.tokens = [token for token in self.tokens if ((token not in string.punctuation))]
        
class Database:
    def __init__(self, documents):
        self.documents = documents
        
    def calculateTFIDF(self):
        vectorizer = TfidfVectorizer()
        documents = []
        for document in self.documents:
            documents.append(" ".join(document.tokens))
            
        # print(documents)
        
        self.TFIDFMatrix = vectorizer.fit_transform(documents)
        self.feature_names = vectorizer.get_feature_names_out()
        self.denseMatrix = self.TFIDFMatrix.todense()
        
        self.df = pd.DataFrame(self.denseMatrix, columns=self.feature_names)
        
        # print(self.denseMatrix)
        
    def searchWord(self, word):
        numGet = 5
        sortedScores = []
        titles = []
        
        if word in self.df.columns:
            TFIDFScore = self.df[word].tolist()
            for id, score in enumerate(TFIDFScore):
                if (score > 0):
                    sortedScores.append((id, score))
                    
            sortedScores.sort(reverse = True, key=lambda x: x[1])
            for i in range(0, min(numGet, len(sortedScores))):
                titles.append(self.documents[sortedScores[i][0]].data['title'])
        
        return titles
    
    def searchPhrase(self, phrase : str):
        words = phrase.split(' ')
        numGet = 5
        sortedScores = [(id, 1) for id in range(len(self.documents))]
        titles = []
        
        # print(words)
        
        for word in words:
            if (word not in self.df.columns):
                return titles
        
        for word in words:
            TFIDFScore = self.df[word].tolist()
            for id, score in enumerate(TFIDFScore):
                sortedScores[id] = (sortedScores[id][0], sortedScores[id][1] * score)
                    
        sortedScores.sort(reverse = True, key=lambda x: x[1])
        for i in range(0, min(numGet, len(sortedScores))):
            if (sortedScores[i][1] == 0): break
            # print(sortedScores[i][1])
            titles.append(self.documents[sortedScores[i][0]].data['title'])
        
        return titles
        