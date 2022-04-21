import math

def is_in_area(coords, center_coords, area_radius):
    #dist = ((coords[0] - center_coords[0])**2+(coords[1] - center_coords[1])**2)**0.5
    dist = get_distance_in_meters(coords, center_coords)
    return dist <= area_radius

def get_distance_in_meters(coords, center_coords):
    a= (float(center_coords[0]), float(center_coords[1]))
    b= (float(coords[0]), float(coords[1]))
    # (lat, lon)

    m_per_longitude_deg = 111.134861111 * 1000
    m_per_latitude_deg = 60871.09000358485 # = math.cos( math.radians(56.8519)) * 111.321377778 * 1000

    d_lat = abs(b[0] - a[0])
    d_lon = abs(b[1] - a[1])

    d_lat_meters = d_lat * m_per_latitude_deg
    d_lon_meters = d_lon * m_per_longitude_deg

    return (math.sqrt(d_lat_meters**2+d_lon_meters**2))

