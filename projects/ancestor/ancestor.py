
def earliest_ancestor(ancestors, starting_node):
    for parent, child in ancestors:
        if child is starting_node:
            earliest_parent = earliest_ancestor(ancestors, parent)
            if earliest_parent is not -1:
                return earliest_parent
            else:
                return parent
    return -1
