def convert_pts_to_2pt(lst_points):
    '''
    Converting the 4-points format of a bounding box to 2 point format
    Convert list point [(x, y), ...] to (x1, y1, x2, y2)
    '''
    x1 = min([point[0] for point in lst_points])
    x2 = max([point[0] for point in lst_points])
    y1 = min([point[1] for point in lst_points])
    y2 = max([point[1] for point in lst_points])

    return (x1, y1, x2, y2)

def ensure_2pt(bbox):
    if all([isinstance(p, int) or isinstance(p, float) for p in bbox]):
        return bbox
    else:
        return convert_pts_to_2pt(bbox)

def compute_overlap(bbox1, bbox2, crite=min):
    '''
        Format: (x1, y1, x2, y2)
    '''
    x1 = max(bbox1[0], bbox2[0])
    x2 = min(bbox1[2], bbox2[2])
    y1 = max(bbox1[1], bbox2[1])
    y2 = min(bbox1[3], bbox2[3])
    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]
    w2 = bbox2[2] - bbox2[0]
    h2 = bbox2[3] - bbox2[1]
    if x2 < x1 or y2 < y1 or w1 * w2 * h1 * h2 == 0:
        return 0

    return (x2 - x1) * (y2 - y1) / crite(w1 * h1, w2 * h2)

def compute_overlap_x(bbox1, bbox2, crite=min):
    '''
        Format: (x1, y1, x2, y2) or [(x, y), ...]
    '''
    bbox1 = ensure_2pt(bbox1)
    bbox2 = ensure_2pt(bbox2)

    dx = min(bbox1[2], bbox2[2]) - max(bbox1[0], bbox2[0])
    if dx < 0 or bbox1[2]-bbox1[0] <= 0 or bbox2[2]-bbox2[0] <= 0:
        return 0

    return dx / crite(bbox1[2]-bbox1[0], bbox2[2]-bbox2[0])

def compute_overlap_y(bbox1, bbox2, crite=min):
    '''
        Format: (x1, y1, x2, y2) or [(x, y), ...]
    '''
    bbox1 = ensure_2pt(bbox1)
    bbox2 = ensure_2pt(bbox2)

    dx = min(bbox1[3], bbox2[3]) - max(bbox1[1], bbox2[1])
    if dx < 0 or bbox1[3]-bbox1[1] <= 0 or bbox2[3]-bbox2[1] <= 0:
        return 0

    return dx / crite(bbox1[3]-bbox1[1], bbox2[3]-bbox2[1])
