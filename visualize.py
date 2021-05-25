from dataset_utils import load_mnist_dataset, load_dataset
from lstm_model_with_classifcation import LSTM_AE_Classification_Model
from lstm_model import LSTM_AE_Model
import matplotlib.pyplot as plt
import numpy as np
import argparse
import torch


parser = argparse.ArgumentParser(description='visualize lstm auto encoder reconstruction from dataset')
parser.add_argument('--model_path', help='model file path')
parser.add_argument('--prediction', type=bool, default=False, help='is prediction lstm')
parser.add_argument('--dataset_type', help='mnist/synthetic')
parser.add_argument('--hidden_dim', type=int, help='hidden state size')
parser.add_argument('--input_size', type=int, help='input size')


args = parser.parse_args()
model_path = args.model_path
is_prediction = args.prediction
dataset_type = args.dataset_type
hidden_dim = args.hidden_dim
input_size = args.input_size
print(is_prediction)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

if dataset_type == 'mnist':
    seq_len = int(784 / input_size)
    if is_prediction:
        model = LSTM_AE_Classification_Model(device, 10, input_size, hidden_dim=hidden_dim)
        _, _, dataset = load_mnist_dataset(False)
    else:
        model = LSTM_AE_Model(device, input_size, hidden_dim=hidden_dim, seq_len=seq_len)
        _, _, dataset = load_mnist_dataset(False)

if dataset_type == 'synthetic':
    seq_len = int(50 / input_size)
    model = LSTM_AE_Model(device, input_size, hidden_dim=hidden_dim, seq_len=seq_len)
    dataset = load_dataset('{}_{}.pkl'.format('synthetic_dataset', 'test'))
    
model.load_state_dict(torch.load(model_path))

#reconstruction of time series data
with torch.no_grad():
    for i in range(3):
        index = np.random.randint(len(dataset))
        example = dataset[index]
        input = example.view(1, seq_len, input_size)
        if is_prediction:
            output, _ = model(input)
        else:
            output = model(input)
        output = output.view(example.shape)
        if dataset_type == 'mnist':
            plt.figure()
            plt.imshow(example[0], cmap='gray', vmin=0, vmax=1)
            plt.figure()
            plt.imshow(output[0], cmap='gray', vmin=0, vmax=1)
            plt.show()
        else:
            plt.plot(example)
            plt.plot(output)
            plt.show()