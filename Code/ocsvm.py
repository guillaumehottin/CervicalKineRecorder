import sklearn.svm as svm
from sklearn.model_selection import train_test_split
from sklearn import metrics
import myutils
import hulls
import numpy as np
import datetime

def test_prediction(model, data, target, file):
    """
    Test a model on some data and write the prediction results to a file.
    
    Parameters
    ----------
    model : svm.OneClassSVM
            The model to test.
    data : array
            The data on which to test the model. It must have an (n,m) shape
            where m is the number of features and n the size of the data.
    target : array
            The labels of the data, 1 for the normal class and -1 otherwise.
    file : file
            The file into which the results will be written. 
    """
    preds = model.predict(data)
    
    file.write("\t\t\t accuracy: {0}\n".format(metrics.accuracy_score(target, preds))) 
    file.write("\t\t\t precision: {0}\n".format(metrics.precision_score(target, preds)))
    file.write("\t\t\t recall: {0}\n".format(metrics.recall_score(target, preds)))
    file.write("\t\t\t f1: {0}\n\n".format(metrics.f1_score(target, preds)))  
    
#Testing function for One Class SVM
def test_ocsvm(m_list, buff_size_list, alpha_list, directory = 'bonnes_mesures/', signal = True):
    """
    A function to test the OneClassSVM algorithm using concave hull discretization.
    
    Parameters
    ----------
    m_list : list
            Contains the values of the parameter m to be tested succesively.
    buff_size_list : list
            Contains the values of the parameter buff_size to be tested succesively.
    alpha_list : list
            Contains the values of the parameter alpha to be tested succesively.
    directory : str, optional
            The path to the directory from which the data has to be fetched. By default 'bonnes_mesures/'.
    signal : bool
            Whether to make an audio signal at the end of the execution or not.
    """
    #Fetch the files in which the data will be read
    files = myutils.fetch_files(dir_name=directory,sub_dir='Normalized')
    with open("test_results.txt","a+") as f:
        #Write the date of the beginning of the execution.
        date = datetime.datetime.now()
        f.write('##########################\n' + str(date.strftime('%d-%m-%Y %H:%M')) + '\n\n')
        
        #Loop over the lists of parameters to test and write their values 
        for m in m_list:
            f.write('m = ' + str(m) + '\n')
            for alpha in alpha_list:
                f.write('\t alpha = ' + str(alpha) + '\n')
                for buff_size in buff_size_list:
                    print('Running: m = {0}, alpha = {1}, buffer = {2}...'.format(m, alpha, buff_size))
                    f.write('\t\t buffer size = ' + str(buff_size) + '\n')
                    
                    #Build the dataset
                    data = []
                    for file in files:
                        yaw, pitch, roll = myutils.get_coord(file)
                        
                        #Make a grid for the three combinations of axes.
                        grid1 = hulls.hull_grid(pitch, yaw, m, alpha, buff_size)
                        grid2 = hulls.hull_grid(roll, yaw, m, alpha, buff_size)
                        grid3 = hulls.hull_grid(pitch, roll, m, alpha, buff_size)
                        data += [[grid1] + [grid2] + [grid3]]
                        
                    n = len(files)
                    # Reshape data into the proper shape: n is the number of files 
                    # considered, 3*m**2 is the size of each piece of data.
                    data = np.array(data).reshape(n, 3*m**2)
                    #Split the data
                    train_data, test_data, train_target, test_target = train_test_split(data, 
                                        np.ones(n).astype(int), shuffle=False, train_size = 0.8)
                    #Create and fit the model
                    model = svm.OneClassSVM(kernel='rbf', gamma = 1/(3*m**2), nu = 0.01)
                    model.fit(train_data)
                    
                    #Make a prediction over both the training and testing datasets
                    test_prediction(model, train_data, train_target, f)
                    test_prediction(model, test_data, test_target, f)
        f.write('\n\n')

    #Audio signal if specified
    if signal:
        myutils.audio_signal()
  
##################################################
        
m_list = [500]
buff_size_list = [0.05]
alpha_list = [2.8]

test_ocsvm(m_list, buff_size_list, alpha_list)