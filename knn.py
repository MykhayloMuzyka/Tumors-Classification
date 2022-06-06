from distances import euclidean


def knn(classified, for_classification, weights, k):
    res = list()
    for i, obj_for_classification in enumerate(for_classification):
        distances = list()
        for classified_obj, klas in classified.items():
            distances.append((euclidean(obj_for_classification, classified_obj, weights), klas))
        sorted_distances = sorted(distances, key=lambda x: x[0])
        distances = sorted_distances[:k]
        for j in range(k, len(sorted_distances)):
            if sorted_distances[j][0] == distances[j - 1][0]:
                distances.append(sorted_distances[j])
            else:
                break
        sorted_classes = [j[1] for j in distances]
        if sorted_classes.count(1) >= 0.7*k:
            res.append(1)
        elif sorted_classes.count(0) >= 0.85*k:
            res.append(0)
        else:
            res.append(2)
    return res
