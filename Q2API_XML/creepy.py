# XML Parser/Data Access Object C:\Users\KVOll\PycharmProjects\Adventure\Q2API_XML\creepy.py
"""AUTO-GENERATED Source file for C:\\Users\\KVOll\\PycharmProjects\\Adventure\\Q2API_XML\\creepy.py"""
import xml.sax
import Queue
import Q2API.xml.base_xml

rewrite_name_list = ("name", "value", "attrs", "flatten_self", "flatten_self_safe_sql_attrs", "flatten_self_to_utf8", "children")

def process_attrs(attrs):
    """Process sax attribute data into local class namespaces"""
    if attrs.getLength() == 0:
        return {}
    tmp_dict = {}
    for name in attrs.getNames():
        tmp_dict[name] = attrs.getValue(name)
    return tmp_dict

def clean_node_name(node_name):
    clean_name = node_name.replace(":", "_").replace("-", "_").replace(".", "_")

    if clean_name in rewrite_name_list:
        clean_name = "_" + clean_name + "_"

    return clean_name

class postreq_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 8
        self.path = [None, u'house', u'room', u'item', u'item', u'item', u'item', u'requirement']
        Q2API.xml.base_xml.XMLNode.__init__(self, "postreq", attrs, None, [])

class prereq_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 6
        self.path = [None, u'house', u'room', u'item', u'item', u'requirement']
        Q2API.xml.base_xml.XMLNode.__init__(self, "prereq", attrs, None, [])

class requirement_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 5
        self.path = [None, u'house', u'room', u'item', u'item']
        self.postreq = []
        self.prereq = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "requirement", attrs, None, [])

class history_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'house', u'room', u'item']
        Q2API.xml.base_xml.XMLNode.__init__(self, "history", attrs, None, [])

class visible_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'house', u'room', u'item']
        Q2API.xml.base_xml.XMLNode.__init__(self, "visible", attrs, None, [])

class desc_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'house', u'room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "desc", attrs, None, [])

class inventory_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'house', u'player']
        Q2API.xml.base_xml.XMLNode.__init__(self, "inventory", attrs, None, [])

class item_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'house', u'room']
        self.requirement = []
        self.item = []
        self.visible = []
        self.l = []
        self.o = []
        self.t = []
        self.history = []
        self.desc = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "item", attrs, None, [])

class l_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'house', u'room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "l", attrs, None, [])

class o_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'house', u'room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "o", attrs, None, [])

class room_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'house', u'player']
        self.item = []
        self.l = []
        self.o = []
        self.t = []
        self.desc = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "room", attrs, None, [])

class score_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'house', u'player']
        Q2API.xml.base_xml.XMLNode.__init__(self, "score", attrs, None, [])

class t_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'house', u'room']
        Q2API.xml.base_xml.XMLNode.__init__(self, "t", attrs, None, [])

class intro_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'house']
        Q2API.xml.base_xml.XMLNode.__init__(self, "intro", attrs, None, [])

class player_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'house']
        self.score = []
        self.inventory = []
        self.room = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "player", attrs, None, [])

class tip_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'house']
        Q2API.xml.base_xml.XMLNode.__init__(self, "tip", attrs, None, [])

class house_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 1
        self.path = [None]
        self.tip = []
        self.player = []
        self.intro = []
        self.room = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "house", attrs, None, [])

class NodeHandler(xml.sax.handler.ContentHandler):
    """SAX ContentHandler to map XML input class/object"""
    def __init__(self, return_q):     # overridden in subclass
        self.obj_depth = [None]
        self.return_q = return_q
        self.last_processed = None
        self.char_buffer = []
        xml.sax.handler.ContentHandler.__init__(self)   # superclass init

    def startElement(self, name, attrs): # creating the node along the path being tracked
        """Override base class ContentHandler method"""
        name = clean_node_name(name)
        p_attrs = process_attrs(attrs)

        if name == "":
            raise ValueError, "XML Node name cannot be empty"

        elif name == "postreq":
            self.obj_depth.append(postreq_q2class(p_attrs))

        elif name == "requirement":
            self.obj_depth.append(requirement_q2class(p_attrs))

        elif name == "prereq":
            self.obj_depth.append(prereq_q2class(p_attrs))

        elif name == "score":
            self.obj_depth.append(score_q2class(p_attrs))

        elif name == "item":
            self.obj_depth.append(item_q2class(p_attrs))

        elif name == "house":
            self.obj_depth.append(house_q2class(p_attrs))

        elif name == "visible":
            self.obj_depth.append(visible_q2class(p_attrs))

        elif name == "tip":
            self.obj_depth.append(tip_q2class(p_attrs))

        elif name == "l":
            self.obj_depth.append(l_q2class(p_attrs))

        elif name == "o":
            self.obj_depth.append(o_q2class(p_attrs))

        elif name == "t":
            self.obj_depth.append(t_q2class(p_attrs))

        elif name == "player":
            self.obj_depth.append(player_q2class(p_attrs))

        elif name == "intro":
            self.obj_depth.append(intro_q2class(p_attrs))

        elif name == "inventory":
            self.obj_depth.append(inventory_q2class(p_attrs))

        elif name == "history":
            self.obj_depth.append(history_q2class(p_attrs))

        elif name == "desc":
            self.obj_depth.append(desc_q2class(p_attrs))

        elif name == "room":
            self.obj_depth.append(room_q2class(p_attrs))

        self.char_buffer = []
        self.last_processed = "start"

    def endElement(self, name): # need to append the node that is closing in the right place
        """Override base class ContentHandler method"""
        name = clean_node_name(name)

        if (len(self.char_buffer) != 0) and (self.last_processed == "start"):
            self.obj_depth[-1].value = "".join(self.char_buffer)

        if name == "":
            raise ValueError, "XML Node name cannot be empty"

        elif name == "postreq":
            self.obj_depth[-2].postreq.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "requirement":
            self.obj_depth[-2].requirement.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "prereq":
            self.obj_depth[-2].prereq.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "score":
            self.obj_depth[-2].score.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "item":
            self.obj_depth[-2].item.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "house":
            # root node is not added to a parent; stays on the "stack" for the return_object
            self.char_buffer = []
            self.last_processed = "end"
            return

        elif name == "visible":
            self.obj_depth[-2].visible.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "tip":
            self.obj_depth[-2].tip.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "l":
            self.obj_depth[-2].l.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "o":
            self.obj_depth[-2].o.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "t":
            self.obj_depth[-2].t.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "player":
            self.obj_depth[-2].player.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "intro":
            self.obj_depth[-2].intro.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "inventory":
            self.obj_depth[-2].inventory.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "history":
            self.obj_depth[-2].history.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "desc":
            self.obj_depth[-2].desc.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "room":
            self.obj_depth[-2].room.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        self.last_processed = "end"


    def characters(self, in_chars):
        """Override base class ContentHandler method"""
        self.char_buffer.append(in_chars)

    def endDocument(self):
        """Override base class ContentHandler method"""
        self.return_q.put(self.obj_depth[-1])

def obj_wrapper(xml_stream):
    """Call the handler against the XML, then get the returned object and pass it back up"""
    try:
        return_q = Queue.Queue()
        xml.sax.parseString(xml_stream, NodeHandler(return_q))
        return (True, return_q.get())
    except Exception, e:
        return (False, (Exception, e))


