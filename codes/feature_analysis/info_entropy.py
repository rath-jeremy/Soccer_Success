import numpy as np

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
    
# Information entropy -----------------------------------------------------
def info_entropy(y,C):
    entropy = 0
    
    if len(y) == 0:
        return entropy

    for i in range(C):      # Loop through class values
        ind_i = y == i
        y_i = y[ind_i]
        
        P_i = len(y_i)/len(y)   # P(y = i)
        
        if P_i == 0:
            pass
        else:
            entropy -= P_i*np.log2(P_i)
        
    return entropy

def cond_entropy(X,y,C,variable_names):
    entropies = np.zeros(len(variable_names))
    thresholds = np.zeros(len(variable_names))

    for i in range(len(variable_names)):    # Loop through attributes
        variable_name = variable_names[i]
        x = X[i]
        x_sort = np.sort(x)
        
        entropy_min = np.inf
        threshold_min = np.inf
        
        for j in range(len(x)-1):           # Loop through attribute values
            x_th = np.mean([x_sort[j],x_sort[j+1]]) # Threshold
            ind_l = x <= x_th
            ind_u = x > x_th

            y_l = y[ind_l]
            y_u = y[ind_u]
            
            P_l = len(y_l)/len(y)   # P(x <= x_th)
            P_u = len(y_u)/len(y)   # P(x > x_th)
            
            H_l = info_entropy(y_l,C)   # H(y|x <= x_th)
            H_u = info_entropy(y_u,C)   # H(y|x > x_th)
            
            entropy_remain = P_l*H_l + P_u*H_u
            
            if entropy_remain < entropy_min:
                entropy_min = entropy_remain
                threshold_min = x_th
                
        entropies[i] = entropy_min
        thresholds[i] = threshold_min

    return entropies, thresholds
            
            
# Output ------------------------------------------------------------------

def saveentropy(variable_names,entropy,threshold,prior_ent,outputfile='entropy.csv'):
    # Reshape arrays
    variable_array = np.array(variable_names)
    variable_list = np.reshape(variable_array,[variable_array.size,1])
    entropy = np.reshape(entropy,[entropy.size,1])
    threshold = np.reshape(threshold,[threshold.size,1])
    
    # Combine
    combined = np.hstack((variable_list,entropy,threshold))
    
    # Write
    hdr = 'Variable, entropy gain (prior entropy = ' + str(prior_ent) + ') , threshold'
    np.savetxt(outputfile,combined,delimiter=',',header=hdr,fmt='%s')
    
if __name__=="__main__":
    inputfile = 'results_2016-2017_esp-primera-division.arff'
    outputfile = 'entropy_2016-2017_esp-primera-division.csv'
    
    X, y, C, variable_names = load_data(inputfile)
    variable_names = variable_names[:-1]    # Remove outcome
    y = np.squeeze(y)   # Convert to array
    
    entropy_prior = info_entropy(y,C)
    
    entropy_remain, thresholds = cond_entropy(X,y,C,variable_names)
    
    entropies_gain = entropy_prior - entropy_remain
    
    saveentropy(variable_names,entropies_gain,thresholds,entropy_prior,outputfile)