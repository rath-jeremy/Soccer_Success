import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time

# Data processing ---------------------------------------------------------

def load_data(filename):
    f = open(filename,'r')
    
    X = []                              # Features
    y = []                              # Classes
    C = None                            # Number of classes
    variable_names = []                 # List of variable names
    
    # Read header
    for line in f:
        if '@data' in line:             # End of headers
            break
        line = line.split("'")
        if '@attribute' in line[0]:     # Attribute name
            variable_names.append(line[1])
            
    # Read data
    for line in f:
        line = line.split(',')
        x_vec = [float(x) for x in line[:-1]]
        X.append(x_vec)
        y.append(int(line[-1]))    
    f.close()
    
    # Convert to matrix/vectors
    X = np.array(X).T
    y = np.array(y)
    y = np.reshape(y,[y.size,1])
    
    C = len(np.unique(y))
    
    return X, y, C, variable_names
    
def random_split(P,K):
    permutated_list = np.random.permutation(np.arange(P))
    folds = np.array_split(permutated_list,K)
    
    return folds
    
def train_val_split(X,y,folds,fold_id):
    N = X.shape[0]      # Number of features
    X_val = X[:,folds[fold_id]]
    y_val = y[folds[fold_id]]
    
    fold_copy = folds[:]
    fold_copy.pop(fold_id)
    fold_train = np.concatenate(fold_copy)
    
    X_train = X[:,fold_train]
    y_train = y[fold_train]
    return X_train, y_train, X_val, y_val
    
# Output ------------------------------------------------------------------
    
def saveweight(W1,W2,outputfile='weight.csv'):
    f = open(outputfile,'wb')
    np.savetxt(f,W1,delimiter=',',header='W1')
    np.savetxt(f,W2,delimiter=',',header='W2')
    f.close()
    
def saveerrors(iter_list,train_err,val_err,outputfile='errors.csv'):
    # Reshape arrays
    iter_list2 = np.reshape(iter_list,[iter_list.size,1])
    train_err2 = np.reshape(train_err,[train_err.size,1])
    val_err2 = np.reshape(val_err,[val_err.size,1])
    
    # Combine
    combined = np.hstack((iter_list2,train_err2,val_err2))
    
    # Write
    hdr = 'Iteration,Train error,Validation error'
    np.savetxt(outputfile,combined,delimiter=',',header=hdr)
    
def ploterr(iter_list,train_err,val_err,H):
    plt.plot(iter_list,train_err,'r',label='Train error')
    plt.plot(iter_list,val_err,'b',label='Validation error')
    plt.ylabel('Error percentage')
    plt.xlabel('Iteration number')
    plt.title('Hidden layer size = ' + str(H))
    plt.ylim([0,1])
    plt.legend()
    plt.show()

# Nonlinear functions -----------------------------------------------------

def d_sigmoid(y):
    return y*(1-y)
        
def sigmoid(x):
    return 1./(1+np.exp(-x))
 
def softmax(Z):
    normalization = np.sum(np.exp(Z),axis=0)
    Y = np.exp(Z)/normalization
    return Y
 
# Machine learning --------------------------------------------------------
        
def forward_prop(X,W1,W2):
    hidden = np.dot(W1,X)           # Hidden layer input
    S = sigmoid(hidden)             # Hidden layer output
    Z = np.dot(W2,S)                # Softmax input
    Y = softmax(Z)                  # Softmax output
    return Y, S
        
def classification_error(X,y,Y_result):
    y_pred = np.reshape(np.argmax(Y_result,axis=0),y.shape)
    corr_num = np.sum(y_pred == y)
    return (y.size - corr_num)/y.size
    
def gradient_descent(X,y,C,X_val,y_val,H,W1 = None, W2 = None):
    # Initialization
    N = X.shape[0]  # Number of features
    P = X.shape[1]  # Number of data points

    if W1 == None or W2 == None:       # No initial weight given
        W1 = np.random.randn(H,N)
        W2 = np.random.randn(C,H)
    
    # Stopping conditions
    maxnum_iter = 100     # Maximum number of iterations
    counter = 1

    iter_list = []
    train_err = []
    val_err = []
    while (counter <= maxnum_iter):
        # Stochastic
        alpha = 1/counter       # Steplength
        update_order = np.random.permutation(P)
        for p in update_order:
            x_p = np.reshape(X[:,p],[N,1])
            y_p = y[p]
            # Forward propagation
            Y, S = forward_prop(x_p,W1,W2)
            
            # Calculate gradients
            t = np.zeros([C,1])
            t[y_p] = 1              # Target vector
            
            grad_W1 = np.outer(np.dot(W2.T,Y-t)*d_sigmoid(S),x_p)
            grad_W2 = np.outer(Y-t, S)
        
            # Take gradient steps
            W1 -= alpha*grad_W1
            W2 -= alpha*grad_W2
        
        # Record errors
        iter_list.append(counter)
        train_result,_ = forward_prop(X,W1,W2)
        val_result,_ = forward_prop(X_val,W1,W2)
        train_err.append(classification_error(X,y,train_result))
        val_err.append(classification_error(X_val,y_val,val_result))

        # update counter
        counter += 1

    iter_list = np.array(iter_list)
    train_err = np.array(train_err)
    val_err = np.array(val_err)
    
    return W1, W2, iter_list, train_err, val_err

if __name__=="__main__":
    time_start = time.time()

    inputfile = 'results_train_excl2015-2016.arff'                 # Dataset
    testfile = 'results_test_2015-2016.arff'                      # Test set
    outputfile = 'weight.csv'                   # Weights learned
    outputfile2 = 'errors.csv'                  # Training/CV errors
    K = 10                                      # Number of folds
    H = 30                                      # Number of hidden units
    
    show_output = True
    normalization = True                        # Normalize attributes to lie on [0,1]
    
    # If using job array for high performance computing
    if "MOAB_JOBARRAYINDEX" in os.environ:
        index = int(os.getenv('MOAB_JOBARRAYINDEX'))
        f = open('msc_input.txt')
        lines = f.readlines()
        line = lines[index].split()
        H = float(line[0])
        f.close()
        
        outputfile = 'weight_H=' + str(H) + '.csv'
        outputfile2 = 'errors_H=' + str(H) + '.csv'
        show_output = False

    X,y,C,variable_names = load_data(inputfile) # Read data
    P = X.shape[1]                              # Number of data points
    if normalization:
        X = X/100                                   # Normalization
    X = np.vstack((np.ones(P),X))               # Compact notation
    
    folds = random_split(P,K)                   # Determine folds

    # K-fold cross validation
    for k in range(K):
        # Split to training & validation set
        X_train,y_train,X_val,y_val = train_val_split(X,y,folds,k)
        
        # Gradient descent
        W1,W2,iter_list,train_err1,val_err1 = gradient_descent(X_train,y_train,C,X_val,y_val,H)
        
        # Record errors
        if k == 0:
            train_err = train_err1
            val_err = val_err1
        else:
            train_err = (k*train_err+train_err1)/(k+1)
            val_err = (k*val_err+val_err1)/(k+1)

    # Train final model
    W1,W2,iter_list,_,_ = gradient_descent(X,y,C,X,y,H)
    
    # Test
    X_test,y_test,_,_ = load_data(testfile)                 # Test data
    P_test = X_test.shape[1]
    if normalization:
        X_test = X_test/100                                     # Normalization
    X_test = np.vstack((np.ones(P_test),X_test))            # Compact notation
    
    Y_result,_ = forward_prop(X_test,W1,W2)
    test_err = classification_error(X_test,y_test,Y_result)
    
    time_end = time.time()

    if show_output:
        ploterr(iter_list,train_err,val_err,H)    # Plot error graph
        print('lowest validation error = ' + str(val_err.min()))
        print('final train error = ' + str(train_err[-1]))
        print('final test error = ' + str(test_err))
        print('Runtime = ' + str(time_end - time_start))
    else:
        print(str(H) + '\t' + str(val_err.min()) + '\t' + str(test_err))   # Record lowest CV error and test error
    
    # Save learned weight and errors
    saveweight(W1,W2,outputfile)
    saveerrors(iter_list,train_err,val_err,outputfile2)