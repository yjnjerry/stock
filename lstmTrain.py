#lstm stock prediction using pattern of stock price
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
import numpy as np
import sys

csv_lines = open('600004.csv').readlines()[1:]
print ('day count = ' + str(len(csv_lines)))
print (csv_lines[0])
former_all = []
latter_all = []

for line in csv_lines:
    item = line.split(',')
    F = [float(item[4]), float(item[7])/10000, float(item[8])/10000]
    if len(former_all) == 0:
        F.append(0.00001)
        F.append(0.00001)
        F.append(0.00001)
    else:
        last = former_all[-1]
        F.append((F[0]-last[0])/last[0])
        F.append((F[1]-last[1])/last[1])
        F.append((F[2]-last[2])/last[2])

    former_all.append(F)
    L = F[0]  ###3->0
    latter_all.append(L)

print len(former_all)
print len(latter_all)

former = former_all[:600]
latter = latter_all[:600]
former_test = former_all[600:]
latter_test = latter_all[600:]

maxlen = 40
step = 1
sequences = []
next_days = []

for i in range(0, len(former) - maxlen, step):
    sequences.append(former[i: i+maxlen])
    next_days.append(latter[i+maxlen])
print('number of sequences:', len(sequences))

sequences_test = []
next_days_test = []
#regression for the stock price up/down %chg
for i in range(0, len(former_test) - maxlen, step):
    sequences_test.append(former_test[i: i+maxlen])
    next_days_test.append(latter_test[i+maxlen])
print('number of test sequences:', len(sequences_test))

print next_days_test

print('getting training vector...')
X = np.zeros((len(sequences), maxlen, 6), dtype=np.float32)
y = np.zeros((len(sequences), 1), dtype=np.float32)
for i, sequence in enumerate(sequences):
    for t, day in enumerate(sequence):
        for g in xrange(0,6):
            X[i, t, g] = day[g]
    y[i, 0] = next_days[i]


model = Sequential()
model.add(LSTM(1024, return_sequences = True, input_shape=(maxlen, 6)))
model.add(LSTM(1024, return_sequences = False))
model.add(Dropout(0.3))
model.add(Dense(1))
model.add(Activation('linear'))

model.compile(loss='mse', optimizer='rmsprop')

for iteration in range(1, 10):
    print('------Iteration------', iteration)
    model.fit(X, y, batch_size=128, nb_epoch=5)
    
    for seq,tar in zip(sequences_test[:20], next_days_test[:20]):
        x = np.zeros((1, maxlen, 6))
	for t, day in enumerate(seq):
            for g in xrange(0,6):
	        x[0, t, g] = day[g]
    
        preds = model.predict(x, verbose=0)[0]
        print(preds[0], tar)

