import matplotlib.pyplot as plt
import shapely
from shapely.geometry import Polygon



data = ['xy', 'yy']




polygons = [
    Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
    Polygon([(1, 0), (2, 0), (2, 1), (1, 1)]),
    Polygon([(0, 1), (1, 1), (1, 2), (0, 2)]),
    Polygon([(1, 1), (2, 1), (2, 2), (1, 2)])
]

for i, poly in enumerate(polygons):
    print(f"Polygon {i}: {poly}")

    merged_polygon = polygons[1].union(polygons[2]).union(polygons[3])
    print(f"Merged Polygon: {merged_polygon}")
    print(f"Area: {merged_polygon.area}")
    print(f"Number of sides: {len(merged_polygon.exterior.coords) - 1}")


def plot_polygons(polygons):
    import matplotlib.pyplot as plt

    merged_polygon = polygons[1].union(polygons[2]).union(polygons[3])
    print(f"Merged Polygon: {merged_polygon}")
    print(f"Area: {merged_polygon.area}")
    print(f"Number of sides: {len(merged_polygon.exterior.coords) - 1}")

    # Plot the merged polygon
    x, y = merged_polygon.exterior.xy
    plt.plot(x, y, label='Merged Polygon')

    # Plot the original polygons for reference
    for i, poly in enumerate(polygons):
        x, y = poly.exterior.xy
        plt.plot(x, y, linestyle='--', label=f'Polygon {i}')

    plt.fill(*merged_polygon.exterior.xy, alpha=0.5, fc='r', ec='none')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Merged Polygon Visualization')
    plt.show()

# Example usage
polygons = [
    Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
    Polygon([(1, 0), (2, 0), (2, 1), (1, 1)]),
    Polygon([(0, 1), (1, 1), (1, 2), (0, 2)]),
    Polygon([(1, 1), (2, 1), (2, 2), (1, 2)])
]

plot_polygons(polygons)