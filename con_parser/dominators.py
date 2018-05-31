# -*- coding: utf-8 -*-
"""
  Dominator tree
"""

from graph import TreeGraph
from traversals import dfs_postorder_nodes


class DominatorTree(object):
    """
      Handles the dominator trees (dominator/post-dominator), and the
      computation of the dominance/post-dominance frontier.
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.doms = {}
        self.df = {}
        self.build()


    def build(self):
        graph = self.cfg.graph
        entry = self.cfg.entry_node
        self.build_dominators(graph, entry)


    def build_dominators(self, graph, entry):
        """
          Builds the dominator tree based on:
            http://www.cs.rice.edu/~keith/Embed/dom.pdf

          Also used to build the post-dominator tree.
        """
        doms = self.doms
        doms[entry] = entry
        post_order = dfs_postorder_nodes(graph, entry)

        post_order_number = {}
        i = 0
        for n in post_order:
            post_order_number[n] = i
            i += 1

        def intersec(b1, b2):
            finger1 = b1
            finger2 = b2
            po_finger1 = post_order_number[finger1]

            if finger2 in post_order_number.keys():
                po_finger2 = post_order_number[finger2]
            else:
                po_finger2 = None

            while po_finger1 != po_finger2:
                no_solution = False
                while po_finger2 is not None and po_finger1 < po_finger2:
                    finger1 = doms.get(finger1, None)
                    if finger1 is None:
                        no_solution = True
                        break
                    po_finger1 = post_order_number[finger1]
                while po_finger2 is not None and po_finger1 < po_finger1:
                    finger2 = doms.get(finger2, None)
                    if finger2 is None:
                       no_solution = True
                       break
                    po_finger2 = post_order_number[finger2]
                if no_solution:
                    break
            return finger1

        changed = True
        while changed:
            changed = False
            for b in reversed(post_order):
              if b == entry:
                continue
              predecessors = b.predecessors
              new_idom = next(iter(predecessors))
              for p in predecessors:
                if p == new_idom:
                  continue
                if p in doms:
                  new_idom = intersec(p, new_idom)
              if b not in doms or doms[b] != new_idom:
                doms[b] = new_idom
                changed = True
                pass
              pass
        return

    def tree(self):
        """Makes a the dominator tree"""
        t_nodes = {}
        doms = self.doms
        t = TreeGraph()

        for node in doms:
            if node not in t_nodes:
                cur_node = t.make_add_node(node)
                t_nodes[node] = cur_node
            cur_node = t_nodes[node]

            parent = doms.get(node, None)
            if parent is not None and parent != node:
                if parent not in t_nodes:
                    parent_node = t.make_add_node(parent)
                    t_nodes[parent] = parent_node
                parent_node = t_nodes[parent]
                t.make_add_edge(parent_node, cur_node, 'dom-edge')
                pass
            pass
        return t

# Note: this has to be done after calling tree
def build_df(t):
    """
    Builds data flow graph using Depth-First search.
    """

    def dfs(seen, node):
        if node in seen:
            return
        seen.add(node)
        node.bb.doms = node.doms = set([node])
        node.bb.reach_offset = node.reach_offset = node.bb.end_offset
        for n in node.children:
            dfs(seen, n)
            node.doms |= node.doms
            node.bb.doms |= node.doms
            if node.reach_offset < n.reach_offset:
                node.bb.reach_offset = node.reach_offset = n.reach_offset
        # print("node %d has children %s" %
        #       (node.number, [n.number for n in node.children]))

    seen = set([])
    for node in t.nodes:
        if node not in seen:
            dfs(seen, node)
    return
