import matplotlib.pyplot as plt
import numpy as np
import sklearn
import sklearn.datasets
import sklearn.linear_model
import matplotlib
import nbadata

input_dim = 11 * 5
batch_size = 48
h1_dim = 256
h2_dim = 32
num_iters = 50
reg_lambda = 0.0005
epsilon = 0.0001

def init(model):
    # xaiver initialization
    np.random.seed(0)
    W1 = np.random.randn(input_dim, h1_dim) / np.sqrt(input_dim)
    b1 = np.zeros((1, h1_dim))
    W2 = np.random.randn(h1_dim, h2_dim) / np.sqrt(h1_dim)
    b2 = np.zeros((1, h2_dim))
    model['W1'], model['W2'], model['b1'], model['b2'] = W1, W2, b1, b2

def forward(model, X, y, visualize=False):
    '''
        input: 
                X -- N by M numpy array 
                y -- N by 1 numpy array of label scores
        output: final score
    '''

    W1, W2, b1, b2 = model['W1'], model['W2'], model['b1'], model['b2']
    H1 = X.dot(W1) + b1
    H1[H1 < 0] = 0      #relu
    if visualize:
        print '[Debugging]:: h1: ', H1
    H2 = H1.dot(W2) + b2
    H2[H2 < 0] = 0      #relu
    if visualize:
        print '[Debugging]:: h2: ', np.nonzero(H2)
        print '[Debugging]:: non-zero entry of h2 -- ', np.count_nonzero(H2)

    # calculate loss function -- RMSE loss or MSE loss
    mean = np.sum(H2.sum(axis=1, keepdims=True) - y) / batch_size
    rmse = np.sqrt(np.sum((H2.sum(axis=1, keepdims=True) - y) ** 2) / batch_size)
    model['H1'] = H1
    model['H2'] = H2
    return rmse, mean

def backprop(model, X, y, loss_grad):
    '''
        X -- N by M ndarray
        y -- N by 1 ndarray
    '''
    W1, W2, b1, b2, H1, H2 = model['W1'], model['W2'], model['b1'], model['b2'], model['H1'], model['H2']

    delta3 = np.ones((batch_size, h2_dim)) * loss_grad
    dH2 = np.zeros(H2.shape)
    dH2[H2 > 0] = 1
    dW2 = np.dot(H1.T, delta3 * dH2)
    # print dW2
    db2 = np.sum(delta3 * dH2, axis=0, keepdims=True)
    dH1 = np.zeros(H1.shape)
    dH1[H1 > 0] = 1
    delta2 = delta3.dot(W2.T) 
    dW1 = np.dot(X.T, delta2 * dH1)
    db1 = np.sum(delta2 * dH1, axis=0, keepdims=True)
    # Add regularization terms (b1 and b2 don't have regularization terms)
    dW2 += reg_lambda * W2
    dW1 += reg_lambda * W1

    # Gradient descent parameter update
    W1 += -epsilon * dW1
    b1 += -epsilon * db1
    W2 += -epsilon * dW2
    b2 += -epsilon * db2


if __name__ == '__main__':

    X, y = nbadata.form_dataset('mystats.txt', 'sample/players.jl')

    cross_valid_ratio = X.shape[0] / 25
    X_valid, X_train = X[:cross_valid_ratio,:], X[cross_valid_ratio:, :]
    y_valid, y_train = y[:cross_valid_ratio,:], y[cross_valid_ratio:, :]
    model = {}
    print '[Debugging]:: Train net initialize...'
    if X.shape[1] != input_dim:
        raise NameError('input dimension not match')
    print '[Debugging]:: Input dim: ', X.shape[1], '    H1: ', h1_dim, '    H2: ', h2_dim
    print '[Debugging]:: Number of training samples: ', X.shape[0] - cross_valid_ratio
    print '[Debugging]:: Number of validation samples: ', cross_valid_ratio
    if X_train.shape[0] % batch_size != 0:
        raise ValueError('batch size not dividable')
    print '[Debugging]:: Batch size: ', batch_size
    print '[Debugging]:: Learning rate: ', epsilon
    init(model)
    for i in xrange(0, num_iters):
        t = i % (X_train.shape[0] / batch_size)
        X_train_batch, y_train_batch = X_train[t * batch_size:t * batch_size + batch_size,:], y[t * batch_size:t * batch_size + batch_size,:]
        rmse, mean = forward(model, X_train_batch, y_train_batch)
        backprop(model, X_train_batch, y_train_batch, mean / rmse)
        v = False
        if i == num_iters - 1:
            v = True
            # print model['W1'], model['W2']

        rmse_valid, mean_valid = forward(model, X_valid[5], y_valid[5], v)
        print 'iteration ', i, ': Train net output = ', rmse
        print '             Test net output = ', rmse_valid

    # nbadata.save_json('model.json', model)

