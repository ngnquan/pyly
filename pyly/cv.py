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

def shrink_edge(xy_list, new_xy_list, edge, r, theta, ratio=0.3):
    if ratio == 0.0:
        return
    start_point = edge
    end_point = (edge + 1) % 4
    long_start_sign_x = np.sign(
        xy_list[end_point, 0] - xy_list[start_point, 0])
    new_xy_list[start_point, 0] = \
        xy_list[start_point, 0] + \
        long_start_sign_x * ratio * r[start_point] * np.cos(theta[start_point])
    long_start_sign_y = np.sign(
        xy_list[end_point, 1] - xy_list[start_point, 1])
    new_xy_list[start_point, 1] = \
        xy_list[start_point, 1] + \
        long_start_sign_y * ratio * r[start_point] * np.sin(theta[start_point])
    
    # long edge one, end point
    long_end_sign_x = -1 * long_start_sign_x
    new_xy_list[end_point, 0] = \
        xy_list[end_point, 0] + \
        long_end_sign_x * ratio * r[end_point] * np.cos(theta[start_point])
    long_end_sign_y = -1 * long_start_sign_y
    new_xy_list[end_point, 1] = \
        xy_list[end_point, 1] + \
        long_end_sign_y * ratio * r[end_point] * np.sin(theta[start_point])

def shrink(xy_list, ratio=0.3, epsilon=1e-4):
    if ratio == 0.0:
        return xy_list, xy_list
    
    diff_1to3 = xy_list[:3, :] - xy_list[1:4, :]
    diff_4 = xy_list[3:4, :] - xy_list[0:1, :]
    diff = np.concatenate((diff_1to3, diff_4), axis=0)
    dis = np.sqrt(np.sum(np.square(diff), axis=-1))
    
    # determine which are long or short edges
    long_edge = int(np.argmax(np.sum(np.reshape(dis, (2, 2)), axis=0)))
    short_edge = 1 - long_edge
    # cal r length array
    r = [np.minimum(dis[i], dis[(i + 1) % 4]) for i in range(4)]
    
    # cal theta array
    diff_abs = np.abs(diff)
    diff_abs[:, 0] += epsilon
    theta = np.arctan(diff_abs[:, 1] / diff_abs[:, 0])
    
    # shrink two long edges
    temp_new_xy_list = np.copy(xy_list)
    shrink_edge(xy_list, temp_new_xy_list, long_edge, r, theta, ratio)
    shrink_edge(xy_list, temp_new_xy_list, long_edge + 2, r, theta, ratio)
    
    # shrink two short edges
    new_xy_list = np.copy(temp_new_xy_list)
    shrink_edge(temp_new_xy_list, new_xy_list, short_edge, r, theta, ratio)
    shrink_edge(temp_new_xy_list, new_xy_list, short_edge + 2, r, theta, ratio)
    
    return temp_new_xy_list, new_xy_list, long_edge
