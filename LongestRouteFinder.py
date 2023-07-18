import sys

from City import City
from Players.Player import Player


def findLongestRoute(node: City, seen_edges: list, city_connection_map: dict,
                     player: Player, end_needed=None, use_flights=False) -> (int, list, set, City):
    outward_connections = city_connection_map[node]
    valid_outward = []
    for connection in outward_connections:  # Gets just the usable routes
        if connection.flight_connection == use_flights and connection not in seen_edges \
                and connection.getController() == player:
            valid_outward.append(connection)

    nodes_seen = {node}  # The current node is always seen
    if len(valid_outward) == 0:  # No valid continuation from this point
        if end_needed is None:
            return 0, [], nodes_seen, node
        elif node == end_needed:  # Correct node found
            return 0, [], nodes_seen, node
        else:  # If invalid ending use -inf to assure not used later
            return -1 * sys.maxsize, [], nodes_seen, node

    elif len(valid_outward) == 1:  # Only one option
        edges_used = seen_edges + valid_outward
        ends = list(valid_outward[0].getLocations())
        ends.remove(node)
        out = \
            findLongestRoute(ends[0], edges_used, city_connection_map, player, end_needed,
                             use_flights)
        try:
            next_len, next_edges, new_nodes, end = out
        except TypeError as e:
            print(node)
            print(ends[0])
            print(edges_used)
            print(out)
            raise e
        nodes_seen = nodes_seen.union(new_nodes)
        if end == end_needed or end_needed is None:
            return next_len + valid_outward[0].getLength(), next_edges + edges_used, nodes_seen, end
        else:  # If invalid ending use the current node
            return 0, edges_used, nodes_seen, node

    else:  # Go through all the options
        longest = -1
        longest_edges_used = []
        furthest_end = None
        for connection in valid_outward:
            ends = list(connection.getLocations())
            ends.remove(node)
            nodes_seen.add(ends[0])  # Adds the node being checked to the list of nodes seen
            edges_used = seen_edges + [connection]  # Tracks the edges used so far

            length, new_edges_used, new_nodes_seen, end = \
                findLongestRoute(ends[0], edges_used, city_connection_map, player, end_needed,
                                 use_flights)

            length += connection.getLength()
            # Adds the length of the current connection to the follow-on connections
            edges_used += new_edges_used
            nodes_seen = nodes_seen.union(new_nodes_seen)
            if length > longest:
                # Updates with the longest route found
                longest_edges_used = edges_used
                longest = length
                furthest_end = end
            if length == longest and len(longest_edges_used) < len(edges_used):
                # Uses the longest path with the lowest number of edges
                longest_edges_used = edges_used
                longest = length
                furthest_end = end

        return longest, longest_edges_used, nodes_seen, furthest_end
