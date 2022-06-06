from data_class import *
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import heatmap
from numpy import corrcoef, mean
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
# print(len(df))
del df['Unnamed: 0']
# del df['diagnosis']
del df['compactness_se']
del df['compactness_worst']
del df['radius_worst']
del df['radius_se']
del df['area_mean']
del df['fractal_dimension_mean']
del df['fractal_dimension_worst']
del df['area_worst']
del df['perimeter']
# build_heat_map(df)
data = Data(df, 'diagnosis')
# list_of_m = list()
# list_of_b = list()
# for _ in range(50):
train, test, real = data.train_test_split(0.5)
#     errors_malignant = list()
#     errors_benign = list()
#     for k in range(1, 21):
predicted = knn(train, test, [1 for i in range(len(df.columns)-1)], 5)
conf_matrix = confusion_matrix(real, predicted)
    #     try:
    #         errors_malignant.append(conf_matrix[1, 2])
    #         errors_benign.append(conf_matrix[0, 2])
    #     except IndexError:
    #         errors_malignant.append(0)
    #         errors_benign.append(0)
    # list_of_m.append(errors_malignant)
    # list_of_b.append(errors_benign)

# mean_b, mean_m = list(), list()
# for i in range(20):
#     mean_b.append(mean([j[i] for j in list_of_b]))
#     mean_m.append(mean([j[i] for j in list_of_m]))
#
#
# plt.plot([str(i) for i in range(1, 21)], mean_m, c='r', label='malignant')
# plt.plot([str(i) for i in range(1, 21)], mean_b, c='g', label='benign')
# plt.xlabel("k")
# plt.ylabel("Count of second class")
# plt.legend()
# plt.grid()
# plt.show()

plt.subplots(figsize=(6, 6))
ax = sns.heatmap(conf_matrix, annot=True, cmap='Blues')
ax.set_xlabel('Predicted Values')
ax.set_ylabel('Actual Values ')
ax.xaxis.set_ticklabels(['Д', 'З', 'ДО'])
ax.yaxis.set_ticklabels(['Д', 'З', 'ДО'])
plt.show()
