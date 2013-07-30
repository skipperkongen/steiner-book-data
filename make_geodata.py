import re
from shapely.geometry import Point, LineString, mapping
from fiona import collection

file_content = open("cities_dk.esmt").read()
file_content = re.sub('\n', ' ', file_content)
arr = file_content.split()

header = arr[:13]
rest = arr[13:]
num_terms = int(header[4])
num_comps = int(header[12])

all_terminals = rest[:num_terms*4]
all_terminals = [(float(x), float(y)) for (i, (x,y)) in enumerate(zip(all_terminals, all_terminals[1:])) if i % 4 == 0]
all_edges = []
all_steiner_pts = []

rest = rest[num_terms*4 + num_terms:]

# states
skip = 0
for i, token in enumerate(rest):
	
	if skip:
		skip -= 1
		continue
	else:
		# READ TERMINALS
		offset = 0
		num_t = int(rest[i + offset])
		t_idx = rest[i+offset+1 : i+offset+1+num_t]
		terminals = map(lambda idx: all_terminals[int(idx)-1], t_idx)
		# ok
		# READ STEINER POINTS
		offset += num_t + 3
		num_s = int(rest[i + offset])
		steiner_segment = rest[i+offset+1: i+offset+1+num_s*4]
		steiner_points = [(float(x), float(y)) for (j, (x, y)) in enumerate(zip(steiner_segment, steiner_segment[1:])) if j % 4 == 0]
		# READ EDGES
		offset += num_s*4 + 1
		num_e = int(rest[i + offset])
		edge_segment = rest[i+offset+1: i+offset+1+num_e*2]
		edges = [
			(
				terminals[int(a)-1] if int(a) > 0 else steiner_points[abs(int(a)) - 1], 
				terminals[int(b)-1] if int(b) > 0 else steiner_points[abs(int(b)) - 1]
			) for (j, (a, b)) in enumerate(zip(edge_segment, edge_segment[1:])) if j % 2 == 0
		]
		# EXTEND COLLECTIONS
		all_edges.extend(edges)
		all_steiner_pts.extend(steiner_points)
		# HOW FAR TO SKIP?
		skip = offset + num_e * 2 + 2

all_terminals = map(lambda coord: Point([coord[0], coord[1]]), all_terminals)
all_steiner_pts = map(lambda coord: Point([coord[0], coord[1]]), all_steiner_pts)
all_edges = map(lambda coords: LineString(coords), all_edges)

#print all_terminals[:10], '\n'
#print all_steiner_pts[:10], '\n'
#print all_edges[:10], '\n'

schema = { 'geometry': 'Point', 'properties': {} }
with collection("all_terminals.shp", "w", "ESRI Shapefile", schema) as output:
	for terminal in all_terminals:
		output.write({'geometry': mapping(terminal), 'properties': {}})

with collection("all_steiner.shp", "w", "ESRI Shapefile", schema) as output:
	for steiner_pt in all_steiner_pts:
		output.write({'geometry': mapping(steiner_pt), 'properties': {}})
	
schema = { 'geometry': 'LineString', 'properties': {} }
with collection("all_edges.shp", "w", "ESRI Shapefile", schema) as output:
	for edge in all_edges:
		output.write({'geometry': mapping(edge), 'properties': {}})
		
		
