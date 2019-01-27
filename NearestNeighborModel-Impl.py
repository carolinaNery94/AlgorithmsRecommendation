import pandas as pd
import numpy as np
from scipy.spatial.distance import hamming

dataFile='/home/carolinanery/PycharmProjects/Understanding Algorithms_Recommendation/BX-Book-Ratings.csv'
data=pd.read_csv(dataFile,encoding="ISO-8859-1",sep=";",header=0,names=["user","isbn","rating"])

#print(data.head())

#Books matadata
bookFile='/home/carolinanery/PycharmProjects/Understanding Algorithms_Recommendation/BX-Books.csv'
books=pd.read_csv(bookFile,encoding = "ISO-8859-1",sep=";",header=0,error_bad_lines=False, usecols=[0,1,2],index_col=0,names=['isbn',"title","author"])
#error_bad_lines=False Ignore rows with errors / usecols=[0,1,2] Pick only the 3 columns

#print(books.head())


def bookMeta(isbn):
  title = books.at[isbn, "title"]
  author = books.at[isbn, "author"]
  return title, author

#print(bookMeta("0060973129"))

#Top N favorite book for a user
def faveBooks(user, N):
    userRatings = data[data["user"]==user] #filter data relevant to the user
    sortedRatings = pd.DataFrame.sort_values(userRatings,['rating'],ascending=[0])[:N] #Pick the top N
    sortedRatings["title"] = sortedRatings["isbn"].apply([bookMeta]) #Apply the bookMeta function to the entire ISBN column
    return sortedRatings

#Pandas isin() method is used to filter data frames.
#isin() method helps in selecting rows with having a particular(or Multiple) value in a particular column.
data = data[data["isbn"].isin(books.index)]

#print(data)

#top 5 books for a particular user
#print(faveBooks(204622,5))

#print the number of rows and columns for dataframe
#print(data.shape)

usersPerISBN = data.isbn.value_counts()
#print(usersPerISBN.head(10))
#print(usersPerISBN.shape)

ISBNsPerUser = data.user.value_counts()
#print(ISBNsPerUser.shape)

#isbn read by more than 10 users
data = data[data["isbn"].isin(usersPerISBN[usersPerISBN>10].index)]
#print(data)

#Keep users who have read more than 10 books
data = data[data["user"].isin(ISBNsPerUser[ISBNsPerUser>10].index)]
print(data)

userItemRatingMatrix=pd.pivot_table(data, values='rating',
                                    index=['user'], columns=['isbn'])
#print(userItemRatingMatrix.head())

#Find the K Nearest Neighbors for a given user
#user1 = 204622
#user2 = 255489

#user1Ratings = userItemRatingMatrix.transpose()[user1]
#print(user1Ratings.head())

#user2Ratings = userItemRatingMatrix.transpose()[user2]
#print(user2Ratings.head())

#Compute the distance between user1 and user2
#print(hamming(user1Ratings, user2Ratings))

def distance(user1, user2):
  try:
    user1Ratings = userItemRatingMatrix.transpose()[user1]
    user2Ratings = userItemRatingMatrix.transpose()[user2]
    distance = hamming(user1Ratings, user2Ratings)
  except:
    distance = np.NaN #In caso of error retun NaN
  return distance

#print(distance(204622, 10118))

#Finding Nearest Neighbors

user = 204622
# allUsers = pd.DataFrame(userItemRatingMatrix.index) #get the ids for all users
# allUsers = allUsers[allUsers.user!=user] #remove the actual user (to avoid compare)
# print(allUsers.head())

#distance between the users and the active user
# allUsers["distance"] = allUsers["user"].apply(lambda x: distance(user, x))
# print(allUsers.head())

# K = 10 #The number of nearest neighbors
# KnearestUsers = allUsers.sort_values(["distance"],ascending=True)["user"][:K] #Pick the top K users

# print(KnearestUsers)

def nearestNeighbors(user, K=10):
  allUsers = pd.DataFrame(userItemRatingMatrix.index)
  allUsers = allUsers[allUsers.user!=user]
  allUsers["distance"] = allUsers["user"].apply(lambda x: distance(user, x))
  KnearestUsers = allUsers.sort_values(["distance"], ascending=True)["user"][:K]  # Pick the top K users
  return KnearestUsers

KnearestUsers = nearestNeighbors(user)
print(KnearestUsers)

#Find the top N recommendations
#Each column represents a book
NNRatings = userItemRatingMatrix[userItemRatingMatrix.index.isin(KnearestUsers)] #Get the ratings of the nearest neighbors for all books
#print(NNRatings)

avgRating = NNRatings.apply(np.nanmean).dropna() #Drop books which don't have a rating
#print(avgRating.head())

#Get the ratings of the active user
booksAlreadyRead = userItemRatingMatrix.transpose()[user].dropna().index
print(booksAlreadyRead)

#Remove the average ratings for books already read by the user
avgRating = avgRating[~avgRating.index.isin(booksAlreadyRead)]

N = 3
topNISBNs = avgRating.sort_values(ascending=False).index[:N]

#Get the name
print(pd.Series(topNISBNs).apply(bookMeta))

def topN(user, N=3):
  KnearestUsers = nearestNeighbors(user)
  NNRatings = userItemRatingMatrix[userItemRatingMatrix.index.isin(KnearestUsers)]
  avgRating = NNRatings.apply(np.nanmean).dropna()
  booksAlreadyRead = userItemRatingMatrix.transpose()[user].dropna().index
  avgRating = avgRating[~avgRating.index.isin(booksAlreadyRead)]
  topNISBNs = avgRating.sort_values(ascending=False).index[:N]
  return pd.Series(topNISBNs).apply(bookMeta)

print(faveBooks(204813, 10))
print(topN(204813, 10))