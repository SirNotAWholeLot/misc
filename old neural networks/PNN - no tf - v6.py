# NON-TENSORFLOW VERSION
# Total line count: 336
# Training: 230
# Input count: 7+1

import numpy as np

def set_creator(p_start, p_num, dataset):
    # should return p_num examples in order in the normal format starting from p_start
    set_x = []
    set_y = []
    for index in range(p_start, p_start+p_num):
        set_line = dataset[index]
        set_x.append(set_line[:input_num_units])
        set_y.append(set_line[input_num_units:])
        
    return set_x, set_y

print("Initialising...")
# Set RNG
seed = 128
rng = np.random.RandomState(seed)
# Globals in Python... yeah, yeah, I know...
# But it should allow me to easily change I/O structure
global dataset_length
global valset_length
global input_num_units
global hidden_num_units
global output_num_units
global sigma
f_data = open("ecoli_data.csv", "r")
dataset = []
line_temp = ((f_data.readline()).split(","))[1:]
while line_temp!=[]:
    # print(line_temp)
    dataset.append(line_temp)
    line_temp = ((f_data.readline()).split(","))[1:]
# Now dataset should be a list of lists, with each containing a line from the data file
# 230/100 split
dataset_length = 220
valset_length = 100
input_num_units = 7
hidden_num_units = dataset_length  # PNN architecture - number of hidden nodes = number of 'training' examples
output_num_units = 8   # This value is never acually used as a number of outputs, just the count of nodes on the 'out' layer
sigma = 0.006   # The smoothing parameter, ~0.02 seem to be the best
# Data is already normalized, so I don't need to do it myself
# Still, I need to count the outputs to normalize the weights
# Parsing will only be done for dataset_lenght + valset_length
# If there are any errors beyond that point, they will be ignored
for i in range(dataset_length + valset_length): # last number has a '\n', but float() does go through it without problem - not reached anymore
    dataset[i] = (dataset[i])[:input_num_units+output_num_units]
    for j in range(input_num_units+1):     # 7+1 inputs + output value that is not properly parsed yet
        try:
            dataset[i][j] = float(dataset[i][j])
        except ValueError:
            print("Value error:", dataset[i][j], "at", i, j)
            dataset[i][j] = '?'
# for i in range(5):
#     print(dataset[i])

# Randomizing data selection:
# Grab the whole set and shuffle it
# This way test set is different every time and randomly selected while still being 400 pre-selected numbers
# train_list should be a 230x8 matrix
# test_list should be a 100x8 matrix
train_list = []
test_list = []
rand_list = np.random.choice(dataset_length + valset_length, dataset_length + valset_length, False)
for i in range(dataset_length):
    rand_line = dataset[rand_list[i]]
    train_list.append(rand_line)
for i in range(dataset_length, dataset_length + valset_length):
    rand_line = dataset[rand_list[i]]
    test_list.append(rand_line)
# train_list = dataset[:dataset_length]
# test_list = dataset[dataset_length:]

# Actually, there was a problem: type_counter passed the whole dataset, not just the training part
type_counter = [0]*output_num_units
for i in range(dataset_length):
    # Yeah, this type of construct looks kinda meh
    # type[i] = train_list[i][input_num_units]
    # type_counter[type[i]] += 1
    type_counter[int( train_list[i][input_num_units] )] = type_counter[int( train_list[i][input_num_units] )] + 1
print("Parsing complete.")
#input("Press Enter to continue...")

val_x, val_y = set_creator(0, valset_length, test_list)
# for i in range(5):
#     print(val_x[i], val_y[i])

# PNN does not require procedural training unlike an MLP net
# Instead, what we need to do is to set it so:
# Inputs: 100x7 matrix
# weights_hidden: 230x7 matrix
# weights_output: 8x230 matrix
# hidden_layer_big: 100x230x1 matrix
# output_layer_big: 100x8
# Node output = exponent of ( -(square sum of (input line - matrix line)) / smoothing parameter squared )
# Calculating each hidden node individually, then doing a matmul for output

# Actually, I don't need the weights in PNN to be variable

# One really annoying thing about Python list constructor is that [[a]]*b gives b links to list [a] instead of b copies of list [a]
weights_hidden = list()
weights_output = list()

# Basically, weights 'hidden' matrix is exactly the first 8 coloumns of the input data

# 230x7
for i in range(hidden_num_units):
    weights_hidden.append(list())
    for j in range(input_num_units):
        (weights_hidden[i]).append(train_list[i][j])

# 8x230
for i in range(output_num_units):
    weights_output.append(list())
    for j in range(hidden_num_units):
        (weights_output[i]).append(0)

# And weights 'output' are ones for matching nodes and zeroes for non-matching ones
for i in range(hidden_num_units):    # Setting the weight to 1/(type occurance count) for a matching connection between a hidden node and an output node
    # The idea is:
    # 0) All weigths_output are pre-set to "zero" as if all were unconnected
    # 1) Take the output type from the i'th train example: type[i] = train_list[i][input_num_units]
    # 2) Find the type counter value corresponding to it: type_count[i] = type_counter[ type[i] ]
    # 3) Find the output weight corresponding to the output node for this type and i'th train example's node: weights_output[ type[i] ][i]
    # 4) Set the weight for the output to the "normalized one": val = 1/( type_count[i]*sigma )
    # And here is a one-line implementation:
    weights_output[int( train_list[i][input_num_units] )][i] = 1/( type_counter[int( train_list[i][input_num_units] )]*sigma )

print("Weights calculated...")
#input("Press Enter to continue...")

# Creating "graph" - a PNN

# 100x230x1
# The last dimention is for matmul to work properly, basically a flip of a line to a coloumn
hidden_layer_big = list()
for i in range(valset_length):
    hidden_layer_big.append(list())
    for j in range(hidden_num_units):
        (hidden_layer_big[i]).append([[0]])

print("Weight matrixes set.")

# Alternative 3:
# The mathematical idea is:
# 1) Take a gaussian hat in every known point
# 2) Sum them up for each output type
# 3) Normalize by type count
# 4) See the value of each type's function in the point in question
# The programming idea is:
# What I have to get at the end would be non-normalized PDF values for each of 100 inputs on each of 8 PDF
# Except the PNN works backwards from that
# So, hidden_layer_big[x][y][0] is the value given to the input X by gaussian hat of example Y, without considering the type of Y
# Next, for each input, I need to sum up all the hats for each output type and normalize them by type count
# This is handles through weights_output, that connect each output node to corresponding pattern nodes calculated here
for input_n in range(valset_length):
    x_single = list()
    for j in range(input_num_units):
        x_single.append(val_x[input_n][j])          # This appeares to speed up the process significantly
    for i in range(hidden_num_units):
        sq_sum = 0                                  # Distance calculation
        for j in range(input_num_units):
            sq_sum = sq_sum + (weights_hidden[i][j] - x_single[j])**2
        hidden_layer_big[input_n][i][0] = np.exp(-sq_sum/sigma**2)
        # There's no 1/type_counter here because it's already implemented in the output layer weights

print("Hidden layer passed.")
#input("Press Enter to continue...")

# This is what defines the shape of weights_output
# This matmul is now a problem. For each of 100 inputs I need to run a proper matmul of 8x230 x 230x1
# The end result should be 100x8

# 100x8
output_layer_big = list()
for input_n in range(valset_length):
    output_layer_big.append(np.matmul(weights_output, hidden_layer_big[input_n]))

print("Output layer passed.")
#input("Press Enter to continue...")

# So, how this works:
# output_layer_big is a matrix of PDF values obtained by the PNN
# output_layer_big[x][y] is the PDF type Y value for sample X
# Basically, I need to get maximal PDF value corresponding to sample X
# As exp(-[...]) flips the distance, bigger value wins
# I do that through a function that compares all values for X and retains the index of the biggest
# output_val is a temporal storage var for PDF values
# output_y is the matrix of results for each of 100 inputs
# val_y is the piece of cropped input matrix containing just the coloumn of 'answers'
output_y = [0]*valset_length
# Here I need to get correct class indexes, calculated class indexes, and class indexes with PDF within 10% of calculated
# For 40 selected (first 40 should do because the list is randomized anyway) inputs
chart_length = 40
chart_var = 0
chart_classes_chosen = [0]*chart_length
chart_pdf_chosen = [0]*chart_length
chart_classes_10perc = [0]*chart_length
chart_classes_50perc = [0]*chart_length
for i in range(chart_length):
    chart_classes_10perc[i] = []
    chart_classes_50perc[i] = []
for input_n in range(valset_length):
    output_val = output_layer_big[input_n][0]
    for i in range(output_num_units):
        if float(output_layer_big[input_n][i])>float(output_val):
           output_y[input_n] = i
           output_val = output_layer_big[input_n][i]
    if chart_var < chart_length:
        chart_classes_chosen[chart_var] = output_y[input_n]
        chart_pdf_chosen = output_layer_big[input_n][ output_y[input_n] ]
        for i in range(output_num_units):
            if float(output_layer_big[input_n][i])>float(output_y[input_n]*0.9) and i!=output_y[input_n]:
                chart_classes_10perc[chart_var].append(i)
            elif float(output_layer_big[input_n][i])>float(output_y[input_n]*0.1) and i!=output_y[input_n]:
                chart_classes_50perc[chart_var].append(i)
        chart_var = chart_var + 1
# print(output_y)
acc = 0
pdf_diff_lin = 0
for i in range(valset_length):
# Predicted PDF value of the chosen - predicted PDF value of the correct
# PDF array [point in valset][chosen class of [point in valset]]
    pdf_diff_lin = pdf_diff_lin + output_layer_big[i][int(output_y[i])] - output_layer_big[i][int(val_y[i][0])]
    if int(output_y[i])==int(val_y[i][0]):
        acc = acc + 1
pdf_diff_lin_abs = pdf_diff_lin/valset_length
pdf_diff_lin_nonzero = pdf_diff_lin/(valset_length-acc)
acc = acc/valset_length
print("Accuracy: ", acc)
print("PDF diff linear average: Abs/nonzero: ", pdf_diff_lin_abs, pdf_diff_lin_nonzero)
# for i in range(chart_length):
#     print(int(val_y[i][0]), chart_classes_chosen[i], chart_classes_10perc[i], chart_classes_50perc[i])
