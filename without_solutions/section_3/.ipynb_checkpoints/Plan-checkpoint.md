Plan:

Source - https://unlimited.ethz.ch/display/IDSIS/Introduction+to+Write+Fast+Code+in+Python
Concepts: 1h45m 
    
* introduce all 4 examples 1-4 from description that we will work on 
    * euclidean distance matrix: see here - https://en.wikipedia.org/wiki/Euclidean_distance_matrix.
    * compute π with Monte Carlo methods: Generate pairs of random x,y coordinates in (-1,1) and check whether they are inside the circle of radius. π ~ 4 * #hits / #pairs.
    * grid search: run same (potentially slow) function on all combinations of specified parameter values and find "best" result.
    * counting words example - idea of scaling on multiple files: see here - https://github.com/minrk/IPython-parallel-tutorial/blob/42ae138529d652d7f18925c619dd305dde579a2f/examples/Counting%20Words.ipynb.
* Big O Notation with examples
    * general concept: definition → implications on scalability
    * examples: sort, binary search, sets/dictionary in python, sum of elements, grid search, dot product, matrix multiplication, gauss elimination, travel salesman, 
* Strategies
    * avoid unnecessary computations: use of dictionaries, caching (lru cache, joblib)
        * lru cache: recursive Fibonnaci (might be a bad idea - need for knowledge about recursion), we need more examples 
    * make use of faster "languages" (cython, numba, ...)
        * high level
    * divide and conquer
        * introduction to idea of map reduce:
            * diagram for each step: distribute/split, process map in parallel, reduce/combine with one axis the time for the computation
        * https://en.wikipedia.org/wiki/Amdahl%27s_law
        * examples 2-4 from description
        * limitations! → map reduce might be not fit → it might be "hard computational science" which is beyond this course
    * algorithms / data structures with examples
        * General introduction as a standalone field in CS
            * raise awareness for main algorithms, e.g. sorting algorithms, combinatorics, graph algorithms, geometrical algorithms
                * many rely on well known data structures that fits the given algorithm: e.g. binary tree, queue, hash tables, 
        * Practical examples:
            * list lookup vs dictionary:
                * example from profiling
            * arrays (NumPy), data frames (Pandas)
                * high level, data frames as a columns of numpy arrays
                * numpy will come later  
            * presorted data
                * binary search
            * optional: (Uwe) binning example as an advanced examples
                * high level with a picture for the understanding of the problem
                * argue why a given data structure
    * reduce memory in case of swapping (→ cpu nodes, hardware, ...)
        * e.g. sparse vectors / matrices
        * 8, 16, 32, 64 bits for real numbers / (signed) integers 
        * offline computation, processing in batches
        * using generators (only mention - advanced topic)
    * hardware: CPU / GPU / Cluster
        * just mention 
        * GPU for some problems (single instruction multiple data)
        * Cluster:
            * use one node: scale up → not so hard; use several nodes efficiently → easy only for a small subset (e.g. map reduce)
            * benefits: multiple cores, fat memory nodes, GPUs, multiple nodes, fast throughput 
            * overhead: get access / libraries, different programming model, CPU on the cluster are not necessary faster than on a PC
 