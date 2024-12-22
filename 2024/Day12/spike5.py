import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon

class GridCell():
    def __init__(self, cell, value):
        self.cells = [cell]
        self.value = value
        self.borders = 4
        self.area = 1
        self.poly = Polygon()

def plot_polygons(grid):

    # Collect all polygons
    polygons = [cell.poly for cell in grid if not cell.poly.is_empty]

    # Create a MultiPolygon
    multi_poly = MultiPolygon(polygons)

    # Plot the MultiPolygon
    fig, ax = plt.subplots()
    for geom in multi_poly.geoms:
        x, y = geom.exterior.xy
        ax.plot(x, y, linestyle='--')
        # Add labels to each polygon
        centroid = geom.centroid
        ax.text(centroid.x, centroid.y, 'Polygon', fontsize=12, ha='center')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Merged MultiPolygon Visualization')
    plt.show()

polygons = [
    Polygon([(0, 0), (0, 1), (1, 1), (1,2), (2,2), (2,0)]),  # Polygon A
    Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),  # Polygon B
    Polygon([(3, 3), (4, 3), (4, 4), (3, 4)]),  # Polygon C
    Polygon([(2, 0), (2, 1), (3, 1), (3, 0)])
    
]

cell = GridCell((0,0), 1)
cell.poly = polygons[0]


cell.poly = cell.poly.union(polygons[1])
cell.poly = cell.poly.union(polygons[3])

if cell.poly.touches(polygons[2]):
    cell.poly = cell.poly.union(polygons[2])
new_poly = [cell]

# new_poly = [polygons[0].union(polygons[1]).union(polygons[2])]




plot_polygons(new_poly)