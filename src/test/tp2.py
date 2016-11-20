import sklearn;
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
	return (vectorizer.fit_transform(messages), labels)

def exec_kmeans(messages):
	return KMeans(n_clusters=10).fit(messages)

def exec_agglomerative_clusterings(messages):
	return AgglomerativeClustering(n_clusters=10).fir(messages)

def silhouette(X, kmeans):
	return metrics.silhouette_score(X, kmeans.labels_)



dataset = read_dataset("SMSSpamCollection.txt");
X = transform_text(dataset);

# results = []
# for i in range(2, 11):
# 	kk = exec_kmeans(X[0])
# 	results.append((kk.inertia_, silhouette(X[0], kk)))


X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X[0], X[1], test_size=0.33, random_state=42)
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, Y_train)
prediction = model.predict(X_test)
print metrics.accuracy_score(Y_test, prediction)
