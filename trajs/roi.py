import math
import numpy as np
from pyproj import Proj 

# Coordinate of KDFW
KDFW = [-96.973496106, 32.584330996] # lon, lat

# Convert lons and lats flat earth coordinates
p = Proj(proj='utm', zone=14, ellps='WGS84') # UTM zone 14N, WGS84
KDFW_x, KDFW_y = p(KDFW[0], KDFW[1]) # lon, lat -> x, y, in meters
KDFW_x, KDFW_y = KDFW_x / 1000, KDFW_y / 1000 # in km

# WXR region of interest, check the _plotting_and_roi.ipynb for details
# WX_ROI = [(-103, -90.5), (26.5, 38)] # lon, lat
wx_roi = [(KDFW[0] - 3, KDFW[0] + 3), (KDFW[1] - 3, KDFW[1] + 3)] # lon, lat

# Radius of the TMA
ROI_RADIUS = 200 # in km

# Occupancy grid resolution
# Note that the grid is in longitudes and latitudes, not in flat earth coordinates, although the four corners of the grid are in flat earth coordinates
RESOLUTION = 3 # in km, which is a quarter of 3nm (12km), the standard separation between two aircrafts

square_edge_size = ROI_RADIUS * 2 / math.sqrt(2) # in km

# UTM coordinates of the four corners of the square of the occupancy grid
# The order is: upper left, upper right, lower right, lower left
grid_ul_xy = [KDFW_x - ROI_RADIUS / math.sqrt(2), KDFW_y + ROI_RADIUS / math.sqrt(2)]
grid_ur_xy = [KDFW_x + ROI_RADIUS / math.sqrt(2), KDFW_y + ROI_RADIUS / math.sqrt(2)]
grid_lr_xy = [KDFW_x + ROI_RADIUS / math.sqrt(2), KDFW_y - ROI_RADIUS / math.sqrt(2)]
grid_ll_xy = [KDFW_x - ROI_RADIUS / math.sqrt(2), KDFW_y - ROI_RADIUS / math.sqrt(2)]

# Number of grid cells in the occupancy grid
lat_grid_cells = int(math.ceil(square_edge_size / RESOLUTION))
lon_grid_cells = int(math.ceil(square_edge_size / RESOLUTION))

# Convert UTM coordinates to flat earth coordinates
grid_ul = p(grid_ul_xy[0] * 1000, grid_ul_xy[1] * 1000, inverse=True) # x, y (in meters) -> lon, lat
grid_ur = p(grid_ur_xy[0] * 1000, grid_ur_xy[1] * 1000, inverse=True) # x, y -> lon, lat
grid_lr = p(grid_lr_xy[0] * 1000, grid_lr_xy[1] * 1000, inverse=True) # x, y -> lon, lat
grid_ll = p(grid_ll_xy[0] * 1000, grid_ll_xy[1] * 1000, inverse=True) # x, y -> lon, lat

# Longitudes and latitudes of the gridlines
grid_lons = np.linspace(grid_ul[0], grid_ur[0], lon_grid_cells + 1)
grid_lats = np.linspace(grid_ul[1], grid_ll[1], lat_grid_cells + 1)