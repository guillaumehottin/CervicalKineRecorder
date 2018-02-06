import sklearn.svm as svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
import myutils
import numpy as np
import datetime
from approx import compute_acp

#Test and print prediction results
def test_prediction(model, data, target, file):
    preds = model.predict(data)
    
    file.write("\t\t\t accuracy: {0}\n".format(metrics.accuracy_score(target, preds))) 
    file.write("\t\t\t precision: {0}\n".format(metrics.precision_score(target, preds)))
    file.write("\t\t\t recall: {0}\n".format(metrics.recall_score(target, preds)))
    file.write("\t\t\t f1: {0}\n\n".format(metrics.f1_score(target, preds)))  
    
#Testing function for One Class SVM
def test_ocsvm_acp(directory = '../bonnes_mesures/', signal = True):
    files = myutils.fetch_files(dir_name=directory,sub_dir='Normalized')
    with open("test_results.txt","a+") as f:
        date = datetime.datetime.now()
        f.write('##########################\n' + str(date.strftime('%d-%m-%Y %H:%M')) + '\n\n')

	for shuffle in [0,1]:
		f.write('## Shuffle == ' + str(shuffle==1) + ' \n')
		data = []
		for file in files:
		       yaw, pitch, roll = myutils.get_coord(file)
		       vep11,vep12 = compute_acp(yaw,pitch,False)
		       vep21,vep22 = compute_acp(pitch,roll,False)
		       vep31,vep32 = compute_acp(roll,yaw,False)
		
		       data += [np.concatenate((vep11,vep12,vep21,vep22,vep31,vep32))]
			         
		n = len(files)
		train_data, test_data, train_target, test_target = train_test_split(data, 
		                                np.ones(n).astype(int), shuffle=True, train_size = 0.8)
		model = svm.OneClassSVM(kernel='rbf', nu = 0.01)
		model.fit(train_data)
		           
		test_prediction(model, train_data, train_target, f)
		test_prediction(model, test_data, test_target, f)
	f.write('\n\n')

    if signal:
        myutils.audio_signal()
  
##################################################
        
for i in range(0,10):
	test_ocsvm_acp()
