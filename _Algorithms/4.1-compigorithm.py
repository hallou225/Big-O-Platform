def compute_largest_cc_size_bf(g):
	## type: (Graph) -> int
	## graphimpl: adjlist
	"""
	Inputs: an undirected graph g = (V, E)
	Outputs: the size of the largest connected component of g
	"""
	largestsize = -float('inf')
	visited = {}

	for node in g.nodes():
		for node in g.nodes():
			visited[node] = False
		
		ccsize = 1
		visited[node] = True

		queue = [node]
		while queue:
			i = queue.pop(0)
			for j in g.get_neighbors(i):
				if visited[j] == False:
					visited[j] = True
					ccsize = ccsize + 1
					queue.append(j)
		largestsize = max(largestsize, ccsize)

	return largestsize