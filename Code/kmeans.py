from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import myutils

###################################################################
#Use kmeans method
def apply_kmeans(n_clusters,data):

	kmeans = KMeans(n_clusters,random_state=0).fit(data)
	centroids = kmeans.cluster_centers_
	#Labels of each point
	labels = kmeans.labels_
	#intra distance - already compute with kmeans
	dist   = kmeans.inertia_ / n_clusters
	return kmeans, centroids,labels,dist


#Barycenter of data
def compute_barycenter(data):
	barycenter = np.zeros(len(data[0]))
	for i in range(0,len(data)):
		barycenter += data[i]
	return barycenter/len(data)


#Give indices of elements in specified cluster
def cluster_indices_data(clust_num,labels):
	return np.where(labels == clust_num)[0]

#Find the coefficient alpha of the function f (see find_best_kmeans)
def alpha(k,former_alpha,Nd):
	if k == 2:
		res = 1-3/4/Nd
	else:
		res = former_alpha+(1-former_alpha)/6
	return res

#Apply several times kmeans to find optimal number of clusters
def find_best_kmeans(max_classes,data):
	f = [1]
	former_alpha = 1
	former_sum_distortions = 0 #sum of clusters distortions with K-1 clusters
	bary = compute_barycenter(data)
	for pt in data:
		former_sum_distortions += np.linalg.norm([bary[0]-pt[0],bary[1]-pt[1]])
	#Iterate over number of clusters K
	for K in range(2,max_classes+1):
		#Apply kmeans with i clusters
		kmeans,centroids,labels,intra_dist = apply_kmeans(K,data)
		pop_classes = []
		sum_distortions = 0 #sum of clusters distortions with K cluster
		#Iterate over clusters
		for i in range(K):
			#Give induces of elements in cluster i
			indices = cluster_indices_data(i,labels)
			#Compute number of elements in indices
			pop_classes.append(len(indices))
			#Compute distortion
			distortion = 0
			#Iterate over population
			for k in range(len(indices)):
				distortion += np.linalg.norm([centroids[i][0]-data[indices[k]][0],centroids[i][1]-data[indices[k]][1]])
			sum_distortions += distortion
		#Compute alphaK
		alph = alpha(k,former_alpha,pop_classes[0])
		#Compute f(K)
		if former_sum_distortions != 0:
			f.append(sum_distortions/alph/former_sum_distortions)
		else:
			f.append(1)
		former_alpha = alph
	return f

#########################################################################
c = [[0,0],[3,7],[-3,4],[-6,-4],[4,-7],[-4,-8]]
r = [4,4,3,3,5,2]
n = 100
x,y,pts = myutils.generate_clusters(c,r,n)

f1 = plt.figure(1)
plt.scatter(x,y)
plt.xlim([-12,12])
plt.ylim([-12,12])
Kmax = 10
res = find_best_kmeans(Kmax,pts)
f2 = plt.figure(2)
plt.plot(range(1,Kmax+1),res,'bo')
