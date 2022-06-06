from image_proccessing import *
from data_class import *
from knn import *


def create_feature_list(mask_img: Photo) -> list:
    return [
        mask_img.radius_mean,
        mask_img.area_se,
        mask_img.compactness_mean,
        mask_img.symmetry_mean, mask_img.symmetry_se, mask_img.symmetry_worst,
        mask_img.fractal_dimension_se
    ]


df = pd.read_csv('data.csv')
del df['Unnamed: 0']
del df['compactness_se']
del df['compactness_worst']
del df['radius_worst']
del df['radius_se']
del df['area_mean']
del df['fractal_dimension_mean']
del df['fractal_dimension_worst']
del df['area_worst']
del df['perimeter']
df = Data(df, 'diagnosis')
train, _, _ = df.train_test_split(0)


def predict(mask):
    mask = Photo(mask)
    features = create_feature_list(mask)
    feature_list = df.normalize(features)
    return knn(train, [feature_list], [1 for _ in range(len(feature_list))], 5)[0]


if __name__ == '__main__':
    img = cv2.imread('Dataset_BUSI_with_GT/malignant/malignant (1)_mask.png')
    predicted_class = predict(img)
    print(predicted_class)
