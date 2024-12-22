from shapely.geometry import Polygon
from shapely.strtree import STRtree
from rtree import index

# Example polygons
polygons = [
    Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),  # Polygon A
    Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),  # Polygon B
    Polygon([(3, 3), (4, 3), (4, 4), (3, 4)]),  # Polygon C
]

# The polygon we want to query
query_polygon = Polygon([(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)])

# Build an R-tree spatial index
spatial_index = index.Index()
for i, poly in enumerate(polygons):
    spatial_index.insert(i, poly.bounds)

# Query the index for polygons intersecting with the query_polygon
candidate_indices = list(spatial_index.intersection(query_polygon.bounds))

# Filter candidates by exact intersection
result = [polygons[i] for i in candidate_indices if polygons[i].intersects(query_polygon)]

print(f"Polygons intersecting with the query polygon: {result}")
