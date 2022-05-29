from image_proccessing import *
from data_class import *
from knn import *


def create_feature_list(mask_img: Photo) -> list:
    return [
        mask_img.radius_mean, mask_img.radius_se, mask_img.radius_worst,
        mask_img.area_mean, mask_img.area_se, mask_img.area_worst,
        mask_img.perimeter,
        mask_img.compactness_mean, mask_img.compactness_se, mask_img.compactness_worst,
        mask_img.symmetry_mean, mask_img.symmetry_se, mask_img.symmetry_worst,
        mask_img.fractal_dimension_mean, mask_img.fractal_dimension_se, mask_img.fractal_dimension_worst
    ]


df = pd.read_csv('data.csv')
del df['Unnamed: 0']
df = Data(df, 'diagnosis')
train, _, _ = df.train_test_split(0)


def predict(mask):
    # img = cv2.imread('Dataset_BUSI_with_GT/benign/benign (1)_mask.png')
    mask = Photo(mask)
    features = create_feature_list(mask)
    feature_list = df.normalize(features)
    return knn(train, [feature_list], [1 for _ in range(len(feature_list))], 7)[0]


if __name__ == '__main__':
    img = cv2.imread('Dataset_BUSI_with_GT/malignant/malignant (1)_mask.png')
    predicted_class = predict(img)
    print(predicted_class)
