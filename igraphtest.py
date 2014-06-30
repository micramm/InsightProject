'''Importing igraph'''
import igraph as ig

g = ig.Graph(directed = True)
g.add_vertices(3)
g.add_edges([(0,1),(1,2),(2,1)])
g.vs["name"] = ["Alice","Bob","Charlie"]
visual_style = {"bbox":(300,300),
                "margin":50,
                "vertex_label":g.vs["name"],
                "vertex_size":25,
                "layout": g.layout("kk"),
                "vertex_label_size":15,
                'vertex_label_angle':1,
                "vertex_color": ["orange","red","green"],
                "vertex_label_dist ": [10.0,10.0,10.0]
}
ig.plot(g, **visual_style)