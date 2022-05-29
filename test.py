from data_class import *
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import heatmap
from numpy import corrcoef
from knn import *


def build_heat_map(df):
    heatmap_df = pd.DataFrame()
    heatmap_df.index = list(df.columns)
    for x in heatmap_df.index:
        corr_list = list()
        for y in heatmap_df.index:
            corr_list.append(corrcoef(df[x], df[y])[0][1])
        heatmap_df[x] = corr_list

    plt.subplots(figsize=(10, 7))
    heatmap(heatmap_df, annot=True, fmt=".2f")
    plt.show()


df = pd.read_csv('data.csv')
data = Data(df, 'diagnosis')
train, test, real = data.train_test_split(0.5)
predicted = knn(train, test, [1 for i in range(len(df.columns)-1)], 7)

conf_matrix = confusion_matrix(real, predicted)
plt.subplots(figsize=(6, 6))
ax = sns.heatmap(conf_matrix, annot=True, cmap='Blues')
ax.set_xlabel('Predicted Values')
ax.set_ylabel('Actual Values ')
ax.xaxis.set_ticklabels(['Д', 'З', 'ДО'])
ax.yaxis.set_ticklabels(['Д', 'З', 'ДО'])
plt.show()
