from distances import euclidean


def knn(classified, for_classification, weights, k):
    classes = [0, 1]
    if len(classes) == 1:
        return [classes[0]]
    res = list()
    for i, obj_for_classification in enumerate(for_classification):
        distances = list()
        for classified_obj, klas in classified.items():
            distances.append((euclidean(obj_for_classification, classified_obj, weights), klas))
        sorted_distances = sorted(distances, key=lambda x: x[0])
        distances = sorted_distances[:k]
        for i in range(k, len(sorted_distances)):
            if sorted_distances[i][0] == distances[i - 1][0]:
                distances.append(sorted_distances[i])
            else:
                break
        sorted_classes = [i[1] for i in distances]
        if sorted_classes.count(1) > sorted_classes.count(0) + 2:
            res.append(1)
        elif sorted_classes.count(0) >= sorted_classes.count(1) + 5:
            res.append(0)
        else:
            res.append(2)
    return res
