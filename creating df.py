from image_proccessing import Photo
import os
import cv2
import sys
from pandas import DataFrame

images_dir = 'Dataset_BUSI_with_GT'
classes = ['malignant', 'benign']
df_dict = {
    'radius_mean': list(),
    'radius_se': list(),
    'radius_worst': list(),

    'area_mean': list(),
    'area_se': list(),
    'area_worst': list(),

    'perimeter': list(),

    'compactness_mean': list(),
    'compactness_se': list(),
    'compactness_worst': list(),

    'symmetry_mean': list(),
    'symmetry_se': list(),
    'symmetry_worst': list(),

    'fractal_dimension_mean': list(),
    'fractal_dimension_se': list(),
    'fractal_dimension_worst': list(),

    'diagnosis': list(),
}

for c in classes:
    print(f'\n{c}')
    directory = os.path.join(images_dir, c)
    images = os.listdir(directory)
    for i, image in enumerate(images):
        sys.stdout.write(f'\r{i+1} / {len(images)}')
        img_path = os.path.join(directory, image)
        img = cv2.imread(img_path)
        img = Photo(img)

        df_dict['radius_mean'].append(img.radius_mean)
        df_dict['radius_se'].append(img.radius_se)
        df_dict['radius_worst'].append(img.radius_worst)

        df_dict['area_mean'].append(img.area_mean)
        df_dict['area_se'].append(img.area_se)
        df_dict['area_worst'].append(img.area_worst)

        df_dict['perimeter'].append(img.perimeter)

        df_dict['compactness_mean'].append(img.compactness_mean)
        df_dict['compactness_se'].append(img.compactness_se)
        df_dict['compactness_worst'].append(img.compactness_worst)

        df_dict['symmetry_mean'].append(img.symmetry_mean)
        df_dict['symmetry_se'].append(img.symmetry_se)
        df_dict['symmetry_worst'].append(img.symmetry_worst)

        df_dict['fractal_dimension_mean'].append(img.fractal_dimension_mean)
        df_dict['fractal_dimension_se'].append(img.fractal_dimension_se)
        df_dict['fractal_dimension_worst'].append(img.fractal_dimension_worst)

        if c == 'malignant':
            df_dict['diagnosis'].append(1)
        else:
            df_dict['diagnosis'].append(0)

df = DataFrame.from_dict(df_dict)
df = df.head(len(df)-300)
df.to_csv('data.csv')
