import sklearn
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer;
from sklearn.cluster import KMeans, AgglomerativeClustering;
from sklearn.neighbors import KNeighborsClassifier;
from sklearn import metrics;
from sklearn import model_selection;

def read_dataset(filename):
	array = []
	with open(filename) as f:
		for line in f.readlines():
			split = line.split("\t")
			if split[0] == "ham":
				array.append((0, split[1]));
			else:
				array.append((1, split[1]));
	return array;

def spams_sount(texts):
	c = 0
	for (t, l) in texts:
		if t == 1:
			c+=1;
	return c;

def transform_text(collection):
	labels, messages = zip(*collection)
	vectorizer = TfidfVectorizer(use_idf=True, stop_words='english', max_df=0.2, min_df=2)
	return vectorizer.fit_transform(messages), labels

def exec_kmeans(messages):
	return KMeans(n_clusters=10).fit(messages)

def exec_agglomerative_clusterings(messages):
	return AgglomerativeClustering(n_clusters=10).fir(messages)

def silhouette(X, kmeans):
	return metrics.silhouette_score(X, kmeans.labels_)



dataset = read_dataset("../../../tp2/SMSSpamCollection.txt");
X, Y = transform_text(dataset);

# results = []
# for i in range(2, 11):
# 	kk = exec_kmeans(X[0])
# 	results.append((kk.inertia_, silhouette(X[0], kk)))


X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.33, random_state=42)

#5 5
skf = model_selection.StratifiedKFold(n_splits=5, random_state=1992, shuffle=False)

accuracy = []
Y = np.array(Y)
for train_index, test_index in skf.split(X_train, Y_train):
	# X_train = [X[i] for i in train_index]
	# X_test = [X[i] for i in test_index]
	# y_train = [Y[i] for i in train_index]
	# y_test = [Y[i] for i in test_index]
	X_train, X_test = X[train_index], X[test_index]
	y_train, y_test = Y[train_index], Y[test_index]

	accuracy_fold = []
	for n in np.arange(1, 100, 2):
		model = KNeighborsClassifier(n_neighbors=n)
		model.fit(X_train, y_train)
		prediction = model.predict(X_test)
		accuracy_fold.append(metrics.accuracy_score(y_test, prediction))
	accuracy.append(accuracy_fold)

average = np.mean(np.array(accuracy), 0)

print average
best_k = np.arange(1, 100, 2)[np.argmax(average)]

# import pylab
#
# pylab.plot(average)
# pylab.show()


model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, Y_train)
prediction = model.predict(X_test)
print metrics.accuracy_score(Y_test, prediction)
