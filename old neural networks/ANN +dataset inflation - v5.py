# 613 data points now
# Inputs: 7
# Outputs: 6
# The scheme: [time difference][inputs]/[another line of inputs]
# Trying to connect two different points in time

import numpy as np
import tensorflow as tf

def batch_creator(batch_size, dataset):
    # should return randomised X from the train data set
    # an element of batch_x is the input line - array of 22 numbers as a list
    # an element of batch_y is the 'answer' to that line - 6 (originally 7) numbers
    # the whole idea is to pull X random lines out of the train set
    rand_list = np.random.choice(train_list_length, batch_size, False)
    batch_x = []
    batch_y = []
    for index in rand_list:
        batch_line = dataset[index]
        batch_x.append(batch_line[:input_num_units])
        batch_y.append(batch_line[input_num_units:])        
    return batch_x, batch_y

def set_creator(p_start, p_num, dataset):
    # should return p_num examples in order in the normal format starting from p_start
    set_x = []
    set_y = []
    for index in range(p_start, p_start+p_num):
        set_line = dataset[index]
        set_x.append(set_line[:input_num_units])
        set_y.append(set_line[input_num_units:])        
    return set_x, set_y

def noisy_duplicate(dataset):
    new_dataset = []
    # Take existing dataset, unwrap into lines, add (uniform, probably bad) noise to each line, wrap into new list'o'lists
    for old_line in dataset:
        new_line = list(map((1 + noise_factor*(0.5 - np.random.random_sample())).__mul__, old_line))
        new_dataset.append(new_line)
    return new_dataset

print("Initialising...")
# Set RNG
seed = 128
rng = np.random.RandomState(seed)
# Globals in Python... yeah, yeah, I know...
# But it should allow me to easily change I/O structure
global dataset_length   # Real dataset length for train list creation
global valset_length
global input_num_units
global hidden1_num_units
global hidden2_num_units
global hidden3_num_units
global hidden1_func     # Originally all tf.sigmoid
global hidden2_func
global hidden3_func
global output_num_units
# New
global extension_factor     # 19
global noise_factor         # 0.02
global train_list_length   # The one I should use for batch creator
# batch_size => 50
# epochs => 2000
# learning_rate => 0.05
# Static parameters
dataset_length = 400 # Out of 1646 total
valset_length = 200 # ???
input_num_units = 7
output_num_units = 6
# Reading data
f_data = open("Data_extracted_v2.csv", "r")
dataset = []
line_temp = ((f_data.readline()).split(",")) # Skip one
line_temp = ((f_data.readline()).split(","))
while line_temp!=[] and line_temp!=['']:
    dataset.append(line_temp[1:])   # losing the first element (ID)
    line_temp = ((f_data.readline()).split(","))
# Now dataset should be a list of lists, with each containing a line from the data file
# Processing data into a format suitable for set/batch creators
max_val = [0]*(input_num_units)
mean_val = [0]*(input_num_units)
mean_num = [0]*(input_num_units)
for i in range(len(dataset)): # last number has a '\n', but float() does go through it without problem
    dataset[i] = (dataset[i])[:input_num_units]
    for j in range(input_num_units):     # all 14 inputs + outputs
        val_flag = 0
        try:
            dataset[i][j] = float(dataset[i][j])
        except ValueError:
            # Missing values: treat as correctly predicted?.. Still, they have to be approximated somehow in training
            dataset[i][j] = 'E'
            val_flag = 1
        if val_flag == 0:   # Is this a real value or a '?' to be replaced?
            max_val[j] = max(max_val[j], dataset[i][j])
            mean_val[j] = mean_val[j] + dataset[i][j] # calculating mean values to replace '?' with
            mean_num[j] = mean_num[j] + 1
# print(max_val)
for i in range(input_num_units):
    mean_val[i] = mean_val[i]/mean_num[i]
for i in range(len(dataset)):
    for j in range(input_num_units):
        if dataset[i][j] == 'E':
            dataset[i][j] = mean_val[j]
        if max_val[j] != 0:
            dataset[i][j] = dataset[i][j]/max_val[j]    # This should normalize it nicely without the noise
# Now, restructuring the dataset
for i in range(len(dataset)):
    j = np.random.randint(i, len(dataset))
    dataset[i].extend(dataset[j][1:])
    dataset[i][0] = dataset[j][0] - dataset[i][0]
    # [time difference][inputs]/[another line of inputs]
# Now a line is input_num_units+output_num_units long
# print(dataset[:2])
# print(len(dataset))
# For best results:
SSE_best_val = ['F']*output_num_units
SSE_best_id = [0]*output_num_units
R2_best_val = ['F']*output_num_units
R2_best_id = [0]*output_num_units
# Hyperparameters
hyperparameters_list = [
    [4, 4, 4, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 50, 2000, 0.05],
    [5, 5, 5, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 50, 2000, 0.05],
    [6, 6, 6, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 50, 2000, 0.05],
    [7, 7, 7, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 50, 2000, 0.05],
    [5, 6, 7, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 50, 2000, 0.05],
    [7, 6, 5, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 50, 2000, 0.05],
    [4, 4, 4, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 100, 2000, 0.05],
    [5, 5, 5, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 100, 2000, 0.05],
    [6, 6, 6, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 100, 2000, 0.05],
    [7, 7, 7, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 100, 2000, 0.05],
    [5, 6, 7, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 100, 2000, 0.05],
    [7, 6, 5, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 100, 2000, 0.05],
    [4, 4, 4, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 500, 2000, 0.01],
    [5, 5, 5, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 500, 2000, 0.01],
    [6, 6, 6, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 500, 2000, 0.01],
    [7, 7, 7, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 500, 2000, 0.01],
    [5, 6, 7, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 500, 2000, 0.01],
    [7, 6, 5, tf.sigmoid, tf.sigmoid, tf.sigmoid, 0, 0.02, 500, 2000, 0.01]
    ]
hyperparameters_grid = [
    [3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7],
    [tf.sigmoid, tf.sin, tf.tanh],
    [tf.sigmoid, tf.sin, tf.tanh],
    [tf.sigmoid, tf.sin, tf.tanh],
    [0, 1, 4, 9, 14, 19],
    [0, 0.01, 0.02, 0.03],
    [5, 10],
    [1000, 2000, 5000],
    [0.05, 0.1]
    ]
hyperloop_type = "list"
hyperparameters = hyperparameters_list[0]
hyperloop_count = len(hyperparameters_list)
print("Starting hyperloop...")
for hyperloop_i in range(hyperloop_count):
    print("- ", hyperloop_i+1, "/", hyperloop_count, " -", sep='')
    # Hyperparameters
    hidden1_num_units, hidden2_num_units, hidden3_num_units, hidden1_func, hidden2_func, hidden3_func, extension_factor, noise_factor, batch_size, epochs, learning_rate = hyperparameters
    print("Config: ", hidden1_num_units, "/", hidden2_num_units, "/", hidden3_num_units, " - ", sep='', end = '')
    if hidden1_func == tf.sigmoid:  # Bad, redo if possible
        print("sgm/", end = '')
    elif hidden1_func == tf.sin:
        print("sin/", end = '')
    elif hidden1_func == tf.tanh:
        print("tanh/", end = '')
    if hidden2_func == tf.sigmoid:
        print("sgm/", end = '')
    elif hidden2_func == tf.sin:
        print("sin/", end = '')
    elif hidden2_func == tf.tanh:
        print("tanh/", end = '')
    if hidden3_func == tf.sigmoid:
        print("sgm", end = '')
    elif hidden3_func == tf.sin:
        print("sin", end = '')
    elif hidden3_func == tf.tanh:
        print("tanh", end = '')
    print(", EF/NF ", extension_factor, "/", noise_factor, ", Batch ", batch_size, ", ", epochs, "/", learning_rate, sep='')    
    # Data normalization for the noise
    dataset_norm = dataset.copy()
    if extension_factor > 0:
        for i in range(len(dataset)):
            for j in range(input_num_units+output_num_units):
                dataset_norm[i][j] = dataset_norm[i][j]/(1 + noise_factor)
    stat_repeat_count = 10
    stat_block_SSE = np.array([0]*output_num_units)
    stat_block_R2 = np.array([0]*output_num_units)
    for stat_loop in range(stat_repeat_count):
        # Randomising data selection: grab the whole set and shuffle it
        # This way test set is different every time and randomly selected while still being X pre-selected numbers
        train_list = []
        test_list = []
        rand_list = np.random.choice(dataset_length + valset_length, dataset_length + valset_length, False)
        for i in range(dataset_length): # This is still using real dataset length to pull lines into train list for further extention
            rand_line = dataset_norm[rand_list[i]]
            train_list.append(rand_line)
        for i in range(dataset_length, dataset_length + valset_length):
            rand_line = dataset_norm[rand_list[i]]
            test_list.append(rand_line)
        # Extending dataset with 'noisy' duplicates
        dataset_temp = train_list.copy()
        for i in range(0, extension_factor):
            dataset_temp.extend(noisy_duplicate(train_list))
        train_list = dataset_temp.copy()    # Copy because I'm clearing it, which is probably unnecessary
        dataset_temp[:] = []
        train_list_length = dataset_length*(1 + extension_factor)
        # train_list = dataset[:dataset_length]
        # test_list = dataset[dataset_length:]
        # print(train_list[:2], "\n")
        # print(test_list[:2])

        # Tensorflow stuff
        # Creating graph - simple three-layer NN
        graph_mlp = tf.Graph()
        with graph_mlp.as_default():
            x = tf.placeholder(tf.float32, [None, input_num_units])
            y = tf.placeholder(tf.float32, [None, output_num_units])
            weights = {
                'hidden1': tf.Variable(tf.random_normal([input_num_units, hidden1_num_units], seed=seed)),
                'hidden2': tf.Variable(tf.random_normal([hidden1_num_units, hidden2_num_units], seed=seed)),
                'hidden3': tf.Variable(tf.random_normal([hidden2_num_units, hidden3_num_units], seed=seed)),
                'output': tf.Variable(tf.random_normal([hidden3_num_units, output_num_units], seed=seed))
            }
            biases = {
                'hidden1': tf.Variable(tf.random_normal([hidden1_num_units], seed=seed)),
                'hidden2': tf.Variable(tf.random_normal([hidden2_num_units], seed=seed)),
                'hidden3': tf.Variable(tf.random_normal([hidden3_num_units], seed=seed)),
                'output': tf.Variable(tf.random_normal([output_num_units], seed=seed))
            }
            hidden1_layer = tf.add(tf.matmul(x, weights['hidden1']), biases['hidden1'])
            hidden1_layer = tf.sigmoid(hidden1_layer)
            #
            hidden2_layer = tf.add(tf.matmul(hidden1_layer, weights['hidden2']), biases['hidden2'])
            hidden2_layer = tf.sigmoid(hidden2_layer)
            #
            hidden3_layer = tf.add(tf.matmul(hidden2_layer, weights['hidden3']), biases['hidden3'])
            hidden3_layer = tf.sigmoid(hidden3_layer)
            #
            output_layer = tf.matmul(hidden3_layer, weights['output']) + biases['output']
            # The cost of optimisation
            # cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=output_layer, labels=y))
            cost = tf.reduce_mean(tf.squared_difference(output_layer, y)/tf.reduce_mean(tf.square(y)))   # This second thing is supposed to be just the mean square of y
            # Adam is an optimised Gradient Descend
            # optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost) 
            optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)
            init = tf.global_variables_initializer()
            # End graph
        avg_cost_prev = 0
        #print("Starting...")

        with tf.Session(graph = graph_mlp) as sess:
            # create initialized variables
            sess.run(init)    
            ### for each epoch, do:
            ###   for each batch, do:
            ###     create pre-processed batch
            ###     run optimizer by feeding batch
            ###     find cost and reiterate to minimize
            j = 0
            for epoch in range(epochs):
                avg_cost = 0
                total_batch = int(train_list_length/batch_size)
                for i in range(total_batch):
                    batch_x, batch_y = batch_creator(batch_size, train_list)
                    _, c = sess.run([optimizer, cost], feed_dict = {x: batch_x, y: batch_y})            
                    avg_cost += c / total_batch
                # if avg_cost > avg_cost_prev:
                #     print("Cost spike:", epoch)
                # avg_cost_prev = avg_cost
                j = j + 1
                if j == 1000:
                    #print('-', end='')
                    j = 0
                # print("Epoch:", (epoch+1), "cost =", "{:.5f}".format(avg_cost))    
            #print("\nTraining complete!")
            val_x, val_y = set_creator(0, valset_length, test_list)
            # print(val_y)
            output_y = sess.run([output_layer], feed_dict = {x: val_x, y: val_y})
            # print(output_y)
            # End session
            
        y_mean = [0]*output_num_units   # this all *should* reset them properly
        y_mean_sq = [0]*output_num_units
        sse = [0]*output_num_units
        tss = [0]*output_num_units
        sse_norm = [0]*output_num_units
        R2 = [0]*output_num_units
        y_pred = [0]*output_num_units
        y_eta = [0]*output_num_units
        for i in range(output_num_units):
            y_pred[i] = [0]*valset_length
            y_eta[i] = [0]*valset_length
        for i in range(valset_length):
            for j in range(output_num_units):
                y_pred[j][i] = output_y[0][i][j]
                y_eta[j][i] = val_y[i][j]
                #
                sse[j] = sse[j] + ((output_y[0][i][j] - val_y[i][j])**2)/valset_length    # Numbers are not that big, so it, ahem, 'should not' overflow
                y_mean[j] = y_mean[j] + (output_y[0][i][j])/valset_length
                y_mean_sq[j] = y_mean_sq[j] + (output_y[0][i][j])**2/valset_length
        for i in range(valset_length):
            for j in range(output_num_units):
                tss[j] = tss[j] + ((output_y[0][i][j] - y_mean[j])**2)/valset_length
        for i in range(output_num_units):
            R2[i] = 1 - sse[i]/tss[i]
            sse_norm[i] = sse[i]/((y_mean_sq[i])**0.5)
        #print("SSE:", sse_norm)
        #print("R2:", R2)
        # print("Y predicted:")
        # for i in range(output_num_units):
        #     print(y_pred[i])
        # print("Y eta:")
        # for i in range(output_num_units):
        #     print(y_eta[i])
        # Todo: drop one worst line for each of output
        stat_block_SSE = stat_block_SSE + np.array(sse_norm)/stat_repeat_count
        stat_block_R2 = stat_block_R2 + np.array(R2)/stat_repeat_count
        print('-', end='')
        # End of statistics loop
    print("\nStatistics:")
    print("SSE: ", end='')
    print(np.around(stat_block_SSE, decimals=3))
    print("R2: ", end='')
    print(np.around(stat_block_R2, decimals=3))
    dataset_norm[:] = []
    # Remember best results
    for i in range(output_num_units):
        if SSE_best_val[i] == 'F' or SSE_best_val[i] < stat_block_SSE[i]:
            SSE_best_val[i] = stat_block_SSE[i]
            SSE_best_id[i] = hyperloop_i
        if R2_best_val[i] == 'F' or R2_best_val[i] < stat_block_R2[i]:
            R2_best_val[i] = stat_block_R2[i]
            R2_best_id[i] = hyperloop_i
    # Getting new hyperparameters
    if hyperloop_type == "list":
        hyperparameters = hyperparameters_list[hyperloop_i]
    # End of hyperparameter loop
print("\nBest results:")
print("Best SSE:", end='')
print(np.around(SSE_best_val, decimals=3))
print("Achieved:", end='')
print(SSE_best_id)
print("Best R2:", end='')
print(np.around(R2_best_val, decimals=3))
print("Achieved:", end='')
print(R2_best_id)
