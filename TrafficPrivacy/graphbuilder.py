import osmium
import kdtree

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.lon = 0.0
        self.lat = 0.0
        self.nexts = []                 # Contains the id of the nodes

class Node_loader(osmium.SimpleHandler):
    def __init__(self, id_dict, loc_dict, loc_tree):
        osmium.SimpleHandler.__init__(self)
        self.id_dict = id_dict
        self.loc_dict = loc_dict
        self.loc_tree = loc_tree
        self.counter = 0

    def node(self, n):
        node = Node(n.id)
        node.lon = n.location.lon
        node.lat = n.location.lat
        self.id_dict [node.id] = node
        self.loc_dict [(node.lon, node.lat)] = node
        self.loc_tree.add ((node.lon, node.lat))
        self.counter += 1

class Way_loader(osmium.SimpleHandler):
    def __init__(self, node_loader):
        osmium.SimpleHandler.__init__(self)
        self.node_loader = node_loader
        self.counter = 0
    def way(self, w):
        if w.tags["highway"] == 'motorway' or w.tags["highway"] == 'residential':
            for i in range (len(w.nodes) - 1):
                cur_n = self.node_loader.loc_dist[(w.nodes[i].lon, w.nodes[i].lat)]
                cur_n.nexts.append(self.node_loader.loc_dist[(w.nodes[i + 1].lon, w.nodes[i + 1].lat)])

class GraphBuilder:
    def __init__(self, file_path):
        self.file_path = file_path
        self.id_dict = dict()
        self.loc_dict = dict()
        self.loc_tree = kdtree.create(dimensions = 2)
    def load_graph(self):
        nl = Node_loader(self.id_dict, self.loc_dict, self.loc_tree)
        nl.apply_file(self.file_path)
        wl = Way_loader(nl)
        wl.apply_file(self.file_path)

