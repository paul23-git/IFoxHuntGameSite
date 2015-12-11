from math import radians, cos, sin, asin, sqrt




ID_TO_STR = {
    1 : ""
}
EARTH_RADIUS = 6371000
BASE_INACCURACY = 1000
ADMIN_GROUP = "Paul"
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radiansF
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return c * EARTH_RADIUS

def offsetCoordinates(lon1, lat1, distance, direction):
    """
    :param lon1: longitude
    :param lat1: latitude
    :param distance:  distance
    :param direction: direction (0 = to north pole)
    :return: (newlong, newlat)
    """

    dx = distance * cos(direction)
    dy = distance * sin(direction)

    dtheta = dx/EARTH_RADIUS
    r = EARTH_RADIUS * cos((lat1 + dtheta)/2)
    dphi = dy/r
    return (lon1 + dphi, lat1 + dtheta)

