from nose.tools import *
from TrafficPrivacy import graphbuilder

def test_loading():
    gb = graphbuilder.GraphBuilder("../data/illinois-latest.osm.pbf")
    gb.load_graph()
