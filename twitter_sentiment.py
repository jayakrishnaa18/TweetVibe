# -*- coding: utf-8 -*-
"""Twitter Sentiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1raksFRhUDjbVR3VgWRkPk2dhWboQ3870

# **Twitter Sentiment Analysis**

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import string
import nltk
import re
from nltk.stem import WordNetLemmatizer

data=pd.read_csv('/content/1Book1.csv') #loading dataset

data.count()

data.head()

data.pop("id")
data.pop("date")
data.pop("NO_QUERY")
data.pop("user")

data.head()

"""**Data Pre-Processing**"""

#This function is for removing the mentions in the tweets
def RemoveMention(input_txt,pattern):
  r=re.findall(pattern,input_txt)
  for word in r:
    input_txt=re.sub(word,"",input_txt)
  return input_txt

#This function is for removing Numbers,Special Characters etc..,
def RemoveSpecialCharacters():
  data['z']=data['cleaned_tweet'].str.replace("[^a-zA-Z#]"," ")

#This function is for StopWord Removal
def StopWordRemoval():
  data['cleaned_tweet']=data['cleaned_tweet'].apply(lambda x:" ".join([w for w in x.split() if len(w)>2]))


#Lemmatizing words present in the tweets

def Lemmatization():
  tokanized_tweet=data['cleaned_tweet'].apply(lambda x:x.split())
  print(tokanized_tweet.head())
  lemmatizer=WordNetLemmatizer()
  tokanized_tweet=tokanized_tweet.apply(lambda sentence: [lemmatizer.lemmatize(word) for word in sentence] )
  for k in range(len(tokanized_tweet)):
    tokanized_tweet[k]=" ".join(tokanized_tweet[k])
  data['cleaned_tweet']=tokanized_tweet


data['cleaned_tweet']=np.vectorize(RemoveMention)(data['text'],"@[\w]*")
RemoveSpecialCharacters()
StopWordRemoval()
Lemmatization()

data.head()

"""**Word Cloud of Words present in the dataset according to The frequency**"""

all_words="".join([word for word in data['cleaned_tweet']])

from wordcloud import WordCloud
wordcloud=WordCloud(width=800,height=500,random_state=42,max_font_size=100).generate(all_words)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

from sklearn.feature_extraction.text import CountVectorizer

bow_vectorizer=CountVectorizer(max_df=0.90,min_df=2,max_features=1000,stop_words='english')
bow=bow_vectorizer.fit_transform(data['cleaned_tweet'])

bow[100].toarray()

from sklearn.metrics import accuracy_score,f1_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

"""**KNN FROM SCRATCH**"""

from scipy.stats import mode
from sklearn import preprocessing

class KNN():
    def __init__( self, K ):
        self.K = K

    def fit( self, X_train, Y_train ):
        self.X_train = X_train
        self.Y_train = Y_train
        self.m, self.n = X_train.shape

    def predict( self, X_test ):
        self.X_test = X_test
        self.m_test, self.n = X_test.shape
        Y_predict = np.zeros( self.m_test )
        for i in range( self.m_test ):
            x = self.X_test[i]
            neighbors = np.zeros( self.K )
            neighbors = self.find_neighbors( x )
            Y_predict[i] = mode(neighbors)[0][0]
        return Y_predict

    def find_neighbors( self, x ):
        euclidean_distances = np.zeros( self.m )
        for i in range( self.m ):
            d = self.euclidean( x, self.X_train[i] )
            euclidean_distances[i] = d
        inds = euclidean_distances.argsort()
        Y_train_sorted = self.Y_train[inds]
        return Y_train_sorted[:self.K]

    def euclidean( self, x, x_train ):
        return np.sqrt( np.sum( np.square( x - x_train ) ) )

    def score(self,Y_test,Y_pred):
        correctclassification = 0
        count = 0
        for count in range( np.size( Y_pred ) ):
            if Y_test[count] == Y_pred[count]:
                correctclassification = correctclassification + 1
        print("Accuracy using KNN: ", (correctclassification/count))

le = preprocessing.LabelEncoder()
X=le.fit_transform(data['cleaned_tweet'])
Y=le.fit_transform(data['target'])
X=X.reshape(-1,1)
X1_train, X1_test, Y1_train, Y1_test = train_test_split(X, Y, test_size = 0.2, random_state = 2)
model = KNN(K = 8)
model.fit(X1_train,Y1_train)
knn_pred = model.predict( X1_test )
model.score(Y1_test,knn_pred)



from sklearn.metrics import confusion_matrix
print("Confusion Matrix of KNN Algorithm: ")
confusion_matrix(Y1_test,knn_pred)

from sklearn import metrics
confusion_matrix = metrics.confusion_matrix(Y1_test,knn_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.title("Confusion Matrix")
plt.show()

print("Performance Metrics for KNN: \n")
print(classification_report(Y1_test,knn_pred))

"""**SVM**"""

Y=data['target']

X2_train, X2_test, Y2_train, Y2_test = train_test_split(bow, Y, test_size = 0.2, random_state = 2)

from sklearn.svm import LinearSVC
SVCModel=LinearSVC()
SVCModel.fit(X2_train,Y2_train)

svc_pred=SVCModel.predict(X2_test)
svc_acc=accuracy_score(svc_pred,Y2_test)

print("Accuracy Using Support Vector Machine is: ")
svc_acc

from sklearn.metrics import confusion_matrix
print("Confusion Matrix of SVM Algorithm: ")
confusion_matrix(Y2_test,svc_pred)

from sklearn import metrics
confusion_matrix = metrics.confusion_matrix(Y2_test,svc_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.title("Confusion Matrix")
plt.show()

print("Performance Metrics for SVM: \n")
print(classification_report(Y2_test,svc_pred))

"""**Naive Bayest**"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
y=data['target']
x3_train, x3_test, y3_train, y3_test = train_test_split(bow, y, test_size = 0.5, random_state = 0)
sc = StandardScaler(with_mean=False)
x3_train = sc.fit_transform(x3_train)
x3_test = sc.transform(x3_test)
classifier = MultinomialNB()
classifier.fit(x3_train, y3_train)
nab_pred = classifier.predict(x3_test)
accuracy_nab = accuracy_score(y3_test,nab_pred)
print("Accuracy using Naive Bayes Algorithm is: ",accuracy_nab)

from sklearn.metrics import confusion_matrix
print("Confusion Matrix of Naive Bayes Clasifier Algorithm: ")
confusion_matrix(y3_test,nab_pred)

from sklearn import metrics
confusion_matrix = metrics.confusion_matrix(y3_test,nab_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = [False, True])
cm_display.plot()
plt.title("Confusion Matrix")
plt.show()

print("Performance Metrics for Naive Bayes Classifier: \n")
print(classification_report(y3_test,nab_pred))

#AOC ROC CURVES
from sklearn.metrics import roc_curve, auc

knn_fpr, knn_tpr, threshold = roc_curve(Y1_test,knn_pred)
auc_knn = auc(knn_fpr, knn_tpr)

svm_fpr, svm_tpr, threshold = roc_curve(Y2_test, svc_pred)
auc_svm = auc(svm_fpr, svm_tpr)

nab_fpr, nab_tpr, threshold = roc_curve(y3_test,nab_pred)
auc_nab = auc(nab_fpr, nab_tpr)



plt.figure(figsize=(5, 5), dpi=100)
plt.plot(knn_fpr, knn_tpr, marker='.', label='KNN (auc = %0.3f)' % auc_knn)
plt.plot(svm_fpr, svm_tpr, linestyle='-', label='SVM (auc = %0.3f)' % auc_svm)
plt.plot(nab_fpr, nab_tpr, marker='.', label='Naive Bayes (auc = %0.3f)' % auc_nab)

plt.xlabel('False Positive Rate -->')
plt.ylabel('True Positive Rate -->')

plt.legend()

plt.show()

from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('all')