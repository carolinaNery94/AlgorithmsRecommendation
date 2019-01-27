import pandas as pd
import numpy as np
from scipy.spatial.distance import hamming
from scipy.sparse import coo_matrix
from numpy.linalg import norm

dataFile='/home/carolinanery/PycharmProjects/Understanding Algorithms_Recommendation/BX-Book-Ratings.csv'
data=pd.read_csv(dataFile,encoding="ISO-8859-1",sep=";",header=0,names=["user","isbn","rating"])

#print(data.head())

#Books matadata
bookFile='/home/carolinanery/PycharmProjects/Understanding Algorithms_Recommendation/BX-Books.csv'
books=pd.read_csv(bookFile,encoding = "ISO-8859-1",sep=";",header=0,error_bad_lines=False, usecols=[0,1,2],index_col=0,names=['isbn',"title","author"])
#error_bad_lines=False Ignore rows with errors / usecols=[0,1,2] Pick only the 3 columns

#print(books.head())

# -----------------------------------
data['user'] = data['user'].astype("category")
data['isbn'] = data['isbn'].astype("category")

R = coo_matrix((data['rating'].astype(float),
                (data['user'].cat.codes.copy(),
                 data['isbn'].cat.codes.copy())))


# print(R.shape)
# print(len(R.data))
# print(R.data[0])
# print(R.row[0])
# print(R.col[0])

#Computing the Error Function
M,N = R.shape
K = 3

P = np.random.rand(M, K)
Q = np.random.rand(K, N)

def error(R, P, Q, lamda=0.02):
  ratings = R.data
  rows = R.row
  col = R.col
  e = 0
  for ui in range(len(ratings)):
    rui = ratings[ui]
    u = rows[ui]
    i = col[ui]
    if rui > 0:
      e = e + pow(rui-np.dot(P[u,:],Q[:,i],2)+lamda*(pow(norm(P[u,:]),2)+pow(norm(Q[:,i]),2)))
  return e

print(error(R, R, Q))

#TODO: unfinished