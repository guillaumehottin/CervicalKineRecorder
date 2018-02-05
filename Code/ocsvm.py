import sklearn.svm as svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
import myutils
import hulls
import numpy as np
import datetime

#Test and print prediction results
def test_prediction(model, data, target, file):
    preds = model.predict(data)
    
    file.write("\t\t\t accuracy: {0}\n".format(metrics.accuracy_score(target, preds))) 
    file.write("\t\t\t precision: {0}\n".format(metrics.precision_score(target, preds)))
    file.write("\t\t\t recall: {0}\n".format(metrics.recall_score(target, preds)))
    file.write("\t\t\t f1: {0}\n\n".format(metrics.f1_score(target, preds)))  
    
#Testing function for One Class SVM
def test_ocsvm(m_list, buff_size_list, alpha_list, directory = 'bonnes_mesures/', signal = True):
    files = myutils.fetch_files(dir_name=directory,sub_dir='Normalized')
    with open("test_results.txt","a+") as f:
        date = datetime.datetime.now()
        f.write('##########################\n' + str(date.strftime('%d-%m-%Y %H:%M')) + '\n\n')
        for m in m_list:
            f.write('m = ' + str(m) + '\n')
            for alpha in alpha_list:
                f.write('\t alpha = ' + str(alpha) + '\n')
                for buff_size in buff_size_list:
                    print('Running: m = {0}, alpha = {1}, buffer = {2}...'.format(m, alpha, buff_size))
                    f.write('\t\t buffer size = ' + str(buff_size) + '\n')
                    data = []
                    for file in files:
                        yaw, pitch, roll = myutils.get_coord(file)
                        grid1 = hulls.hull_grid(pitch, yaw, m, alpha, buff_size)
                        grid2 = hulls.hull_grid(roll, yaw, m, alpha, buff_size)
                        grid3 = hulls.hull_grid(pitch, roll, m, alpha, buff_size)
                        data += [[grid1] + [grid2] + [grid3]]
                        
                    n = len(files)
                    data = np.array(data).reshape(n, 3*m**2)
                    train_data, test_data, train_target, test_target = train_test_split(data, 
                                        np.ones(n).astype(int), shuffle=False, train_size = 0.8)
                    model = svm.OneClassSVM(kernel='rbf', gamma = 1/m**2, nu = 0.01)
                    model.fit(train_data)
                    
                    test_prediction(model, train_data, train_target, f)
                    test_prediction(model, test_data, test_target, f)
        f.write('\n\n')

    if signal:
        myutils.audio_signal()
  
##################################################
        
m_list = [500]
buff_size_list = [0.03, 0.05]
alpha_list = [2, 3]

test_ocsvm(m_list, buff_size_list, alpha_list)