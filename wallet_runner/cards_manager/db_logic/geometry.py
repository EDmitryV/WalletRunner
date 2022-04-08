

def is_in_area(coords, center_coords, area_radius):
    dist = ((coords[0] - center_coords[0])**2+(coords[1] - center_coords[1])**2)**0.5
    return dist <= area_radius