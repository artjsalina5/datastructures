# Graph Search

```python {cmd id="graph" hide}
from ds2.graph import AdjacencySetGraph as Graph
```

Now that we have a vocabulary for dealing with graphs, we can revisit some previous topics.
For example, a tree can now be viewed as a graph with edges directed from parents to children.
Given a graph that represents a rooted tree, we could rewrite our preorder traversal using the Graph ADT.
Let's say we just want to print all the vertices.

```python {cmd id="graphprintall1" continue="graph"}
def printall(G, v):
    print(v)
    for n in G.nbrs(v):
        printall(G, n)
```

```python {cmd continue="graphprintall1"}
G = Graph({1,2,3,4}, {(1,2), (1,3), (1,4)})
printall(G, 1)
```

This is fine for a tree, but it quickly gets very bad as soon as there is a cycle.
In that case, there is nothing in the code to keep us from going around and around the cycle.
We will get a `RecursionError`.
We will take the same approach as Hansel and Gretel: we're going to leave bread crumbs to see where we've been.
The easiest way to do this is to just keep around a set that stores the vertices that have been already visited in the search.
Thus, our `printall` method becomes the following.

```python {cmd id="graphprintall2" continue="graph"}
def printall(G, v, visited):
    visited.add(v)
    print(v)
    for n in G.nbrs(v):
        if n not in visited:
            printall(G, n, visited)
```

```python {cmd continue="graphprintall2"}
G = Graph({1,2,3,4}, {(1,2), (2,3), (3,4), (4,1)})
printall(G, 1, set())
```


This is the most direct generalization of a recursive tree traversal into something that also traverses the vertices of a graph.
Unlike with (rooted) trees, we have to specify the starting vertex, because there is no specially marked "root" vertex in a graph.
Also, this code will not necessarily print all the vertices in a graph.
In this case, it will only print those vertices that are connected to the starting vertex.
This pattern can be made to work more generally.

## Depth-First Search

A **depth-first search** (or **DFS**) of a graph $G$ starting from a vertex $v$ will visit all the vertices connected to $v$.
It will always prioritize moving "outward" in the direction of new vertices, backtracking as little as possible.
The `printall` method above prints the vertices in a **depth-first order**.
Below is the general form of this algorithm.

```python {cmd id="graphdfs_01" continue="graph"}
def dfs(G, v):
    visited = {v}
    _dfs(G, v, visited)
    return visited

def _dfs(G, v, visited):
    for n in G.nbrs(v):
        if n not in visited:
            visited.add(n)
            _dfs(G, n, visited)
```

```python {cmd continue="graphdfs_01"}
G = Graph({1,2,3,4}, {(1,2), (2,3), (3,4), (4,2)})
print('reachable from 1:', dfs(G, 1))
print('reachable from 2:', dfs(G, 2))
```

With this code, it will be easy to check if two vertices are connected.
For example, one could write the following.

```python {cmd id="graphconnected_01" continue="graphdfs_01"}
def connected(G, u, v):
    return v in dfs(G, u)
```

We can try this code on a small example to see.
Notice that it is operating on a directed graph.

```python {cmd continue="graphconnected_01"}
G = Graph({1,2,3,4}, {(1,2), (2,3), (3,4), (4,2)})

print("1 is connected to 4:", connected(G, 1, 4))
print("4 is connected to 3:", connected(G, 4, 3))
print("4 is connected to 1:", connected(G, 4, 1))
```

It's possible to modify our `dfs` code to provide not only the set of connected vertices, but also the paths used in the search.
The idea is to store a dictionary that maps vertices to the previous vertex in the path from the starting vertex.
This is really encoding a tree as a dictionary that maps nodes to their parent.
The root is the starting vertex.

It differs from the trees we've seen previously in that it naturally goes up the tree from the leaves to the root rather than the reverse.
The resulting tree is called the **depth-first search tree**.
It requires only a small change to generate it.
We use the convention that the starting vertex maps to `None`.

```python {cmd id="graphdfs_02" continue="graph"}
def dfs(G, v):
    tree = {v: None}
    _dfs(G, v, tree)
    return tree

def _dfs(G, v, tree):
    for n in G.nbrs(v):
        if n not in tree:
            tree[n] = v
            _dfs(G, n, tree)
```

```python {cmd continue="graphdfs_02"}
G = Graph({1,2,3,4}, {(1,2), (2,3), (3,4), (4,2)})
print('dfs tree from 1:', dfs(G, 1))
print('dfs tree from 2:', dfs(G, 2))
```

## Removing the Recursion

The `dfs` code above uses recursion to keep track of previous vertices, so that we can backtrack (by `return`ing) when we reach a vertex from which we can't move forward.
To remove the recursion, we replace the function call stack with our own stack.

This is not just an academic exercise.
By removing the recursion, we will reveal the structure of the algorithm in a way that will allow us to generalize it to other algorithms.
Here's the code.

```python {cmd id="_graph.graphsearch_00" hide}
from ds2.queue import ListQueue as Queue
from ds2.priorityqueue import PriorityQueue
from ds2.graph import Graph

```

```python {cmd id="_graph.graphsearch_01" continue="_graph.graphsearch_00"}
def dfs(self, v):
    tree = {}
    tovisit = [(None, v)]
    while tovisit:
        a,b = tovisit.pop()
        if b not in tree:
            tree[b] = a
            for n in self.nbrs(b):
                tovisit.append((b,n))
    return tree
```

```python {cmd continue="_graph.graphsearch_01"}
G = Graph({1,2,3,4}, {(1,2), (2,3), (3,4), (4,2)})
print('dfs tree from 1:', dfs(G, 1))
print('dfs tree from 2:', dfs(G, 2))
```

## Breadth-First Search

We get another important traversal by replacing the stack with a queue.
In this case, the search prioritizes breadth over depth, resulting in a **breadth-first search** of **BFS**.

```python {cmd id="_graph.graphsearch_02" continue="_graph.graphsearch_01"}
def bfs(G, v):
    tree = {}
    tovisit = Queue()
    tovisit.enqueue((None, v))
    while tovisit:
        a,b = tovisit.dequeue()
        if b not in tree:
            tree[b] = a
            for n in G.nbrs(b):
                tovisit.enqueue((b,n))
    return tree
```

```python {cmd continue="_graph.graphsearch_02"}
G = Graph({1,2,3,4}, {(1,2), (2,3), (3,4), (4,2)})
print('bfs tree from 1:', bfs(G, 1))
print('bfs tree from 2:', bfs(G, 2))
```


A wonderful property of breadth-first search is that the paths encoded in the resulting **breadth-first search tree** are the shortest paths from each vertex to the starting vertex.
Thus, BFS can be used to find the shortest path connecting pairs of vertices in a graph.

```python {cmd id="_graph.graphsearch_03" continue="_graph.graphsearch_02"}
def distance(G, u, v):
    tree = G.bfs(u)
    if v not in tree:
        return float('inf')
    edgecount = 0
    while v is not u:
        edgecount += 1
        v = tree[v]
    return edgecount
```

```python {cmd continue="_graph.graphsearch_03"}
G = Graph({1,2,3,4,5}, {(1,2), (2,3), (3,4), (4,5)})
print("distance from 1 to 5:", distance(G, 1, 5))
print("distance from 2 to 5:", distance(G, 2, 5))
print("distance from 3 to 4:", distance(G, 3, 4))
```

## Weighted Graphs and Shortest Paths

In the **single source, all shortest paths problem**, the goal is to find the shortest path from every vertex to a given source vertex.
If the edges are assumed to have the same length, then BFS solves this problem.
However, it is common to consider **weighted graphs** in which a (positive) real number called the **weight** is assigned to each edge.
We will augment our graph ADT to support a function `wt(u,v)` that returns the weight of an edge.
Then, the weight of a path is the sum of the weights of the edges on that path.
Now, simple examples make it clear that the shortest path may not be what we get from the BFS tree.

```python {cmd id="_graph.digraph_00"}
from ds2.graph import AdjacencySetGraph
from ds2.priorityqueue import PriorityQueue

class Digraph(AdjacencySetGraph):
    def addedge(self, u, v, weight = 1):
        self._nbrs[u][v] = weight

    def removeedge(self, u, v):
        del self._nbrs[u][v]

    def addvertex(self, v):
        self._V.add(v)
        self._nbrs[v] = {}

    def wt(self, u, v):
        return self._nbrs[u][v]
```

```python {cmd id="_graph.graph_00"}
from ds2.graph import Digraph

class Graph(Digraph):
    def addedge(self, u, v, weight = 1):
        Digraph.addedge(self, u, v, weight)
        Digraph.addedge(self, v, u, weight)

    def removeedge(self, u, v):
        Digraph.removeedge(self, u, v)
        Digraph.removeedge(self, v, u)

    def edges(self):
        E = {frozenset(e) for e in Digraph.edges(self)}
        return iter(E)
```

One nice algorithm for the single source, all shortest paths problem on weighted graphs is called Dijkstra's algorithm.
It looks a lot like DFS and BFS except now, the stack or queue is replaced by a priority queue.
The vertices will be visited in order of their distance to the source.
These distances will be used as the priorities in the priority queue.

We'll see two different implementations.
The first, although less efficient is very close to DFS and BFS.
Recall that in those algorithms, we visit the vertices, recording the edges used in a dictionary and adding all the neighboring vertices to a stack or a queue to be traversed later.
We'll do the same here except that we'll use a priority queue to store the edges to be searched.
We'll also keep a dictionary of the distances from the start vertex that will be updated when we visit a vertex.
The priority for an edge `(u,v)` will be the distance to `u` plus the weight of `(u,v)`.
So, if we use this edge, the shortest path to `v` will go through `u`.
In this way, the tree will encode all the shortest paths from the start vertex.
Thus, the result will be not only the lengths of all the paths, but also an efficient encoding of the paths themselves.



```python {cmd id="_graph.graphsearch_04" continue="_graph.graphsearch_03"}
def dijkstra(G, v):
    tree = {}
    D = {v: 0}
    tovisit = PriorityQueue()
    tovisit.insert((None,v), 0)
    for a,b in tovisit:
        if b not in tree:
            tree[b] = a
            if a is not None:
                D[b] = D[a] + G.wt(a,b)
            for n in G.nbrs(b):
                tovisit.insert((b,n), D[b] + G.wt(b,n))
    return tree, D
```

Let's write a little code to see how this works.
We'll add a function to write out the path in the tree and then we'll display all the shortest paths found by the algorithm.

```python {cmd id="shortestpaths" continue="_graph.graphsearch_04"}
def path(tree, v):
    path = []
    while v is not None:
        path.append(str(v))
        v = tree[v]
    return ' --> '.join(path)

def shortestpaths(G, v):
    tree, D = dijkstra(G, v)
    for v in G.vertices():
        print('Vertex', v, ':', path(tree, v), ", distance = ", D[v])
```

```python {cmd continue="shortestpaths"}
G = Graph({1,2,3}, {(1,2, 4.6), (2, 3, 9.2), (1, 3, 3.1)})
shortestpaths(G, 1)
print('------------------------')
# Adding an edge creates a shortcut to vertex 2.
G.addedge(3, 2, 1.1)
shortestpaths(G, 1)
```

## Prim's Algorithm for Minimum Spanning Trees

Recall that a subgraph of an undirected graph $G = (V,E)$ is a **spanning tree** if it is a tree with vertex set $V$.
For a weighted graph, the weight of a spanning tree is the sum of the weights of its edges.
The **Minimum Spanning Tree** (**MST**) Problem is to find *a* spanning tree of an input graph with minimum weight.
The problem comes up naturally in many contexts.

To find an algorithm for this problem, we start by trying to describe which edges should appear in the minimum spanning tree.
That is, we should think about the object we want to construct first, and only then can we think about *how* to construct it.
We employed a similar strategy when discussing sorting algorithms.
In that case, we first tried to write a function that would test for correct output.
We won't go that far now, but we will ask, "How would we know if we had the minimum spanning tree?"

One thing that would certainly be true about the minimum spanning tree is that if we removed an edge (resulting in two trees), we couldn't find a lighter weight edge connecting these two trees.
Otherwise, that would be a spanning tree of lower weight.

Something even a little more general is true.
If we split the vertices into any two sets $A$ and $B$, the lowest weight edge with one end in $A$ and the other end in $B$ must be in the MST.
Suppose for contradiction that this edge is not in the MST.
Then, we could add that edge and form a cycle, which would have another edge spanning $A$ and $B$.
That edge could then be removed, leaving us with a lighter spanning tree.
This is a contradiction, because we assumed that we started with the MST.

So, in light of our previous graph algorithms, we can try to always add the lightest edge from the visited vertices to an unvisited vertex.
This can easily be encoded in a priority queue.

```python {cmd id="_graph.graphsearch_05", continue="_graph.graphsearch_04"}
def prim(G):
    v = next(iter(G.vertices()))
    tree = {}
    tovisit = PriorityQueue()
    tovisit.insert((None, v), 0)
    for a, b in tovisit:
        if b not in tree:
            tree[b] = a
            for n in G.nbrs(b):
                tovisit.insert((b,n), G.wt(b,n))
    return tree
```

The following example clearly shows that the minimum spanning tree and the shortest path tree are not the same.

```python {cmd id="msts" continue="_graph.graphsearch_05"}
G = Graph({1,2,3,4,5}, {(1, 2, 1),
                        (2, 3, 1),
                        (1, 3, 2),
                        (3, 4, 1),
                        (3, 5, 3),
                        (4, 5, 2),
                       })
mst = prim(G)
sp, D = dijkstra(G, 1)
print(mst)
print(sp)
```
## An optimization for Priority-First search

The implementation above, although correct, is not technically Dijkstra's Algorithm, but it's close.
By trying to improve its asymptotic running time, we'll get to the real Dijkstra's Algorithm.
When thinking about how to improve an algorithm, an easy first place to look is for wasted work.
In this case, we can see that many edges added to the priority queue are later removed without being used, because they lead to a vertex that has already been visited (by a shorter path).

It would be better to not have to these edges in the priority queue, but we don't know when we first see an edge whether or not a later edge will provide a short cut.
We can avoid adding a new entry to the priority and instead modify the existing entry that is no longer valid.

The idea is to store vertices rather than edges in the priority queue.
Then, we'll use the `changepriority` method to update an entry when we find a new shorter path to a given vertex.
Although we won't know the distances at first, we'll store the shortest distance we've seen so far.
If we find a shortcut to a given vertex, we will reduce it's priority and update the priority queue.
Updating after finding a shortcut is called **edge relaxation**.
It works as follows.
The distances to the source are stored in a dictionary `D` that maps vertices to the distance, based on what we've searched so far.
If we find that `D[n] > D[u] + G.wt(u,n)`, then it would be a shorter path to `n` if we just took the shortest path from the source to `u` and appended the edge `(u,n)`.  In that case, we set `D[n] = D[u] + G.wt(u,n)` and update the priority queue.
*Note that we had this algorithm in mind when we added `changepriority` to our Priority Queue ADT.*

Here's the code.

```python {cmd id="_graph.graphsearch_06" continue="_graph.graphsearch_05"}
def dijkstra2(G, v):
    tree = {v: None}
    D = {u: float('inf') for u in G.vertices()}
    D[v] = 0
    tovisit = PriorityQueue(entries = [(u, D[u]) for u in G.vertices()])
    for u in tovisit:        
        for n in G.nbrs(u):
            if D[u] + G.wt(u,n) < D[n]:
                D[n] = D[u] + G.wt(u,n)
                tree[n] = u
                tovisit.changepriority(n, D[n])
    return tree, D
```

```python {cmd continue="_graph.graphsearch_06"}
from ds2.graph import Digraph

V = {1,2,3,4,5}
E = {(1,2,1),
     (2,3,2),
     (1,3,2),
     (3,4,2),
     (2,5,2)
    }
G = Digraph(V, E)
tree, D = dijkstra2(G, 1)
print(tree, D)
```

An important difference with our DFS/BFS code is that the main data structure now stores vertices, not edges.
Also, we don't have to check if we've already visited a vertex, because if we have already visited it, we won't find an edge to relax (vertices are visited in order of their distance to the source).
