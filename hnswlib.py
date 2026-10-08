"""Stand-in for the `hnswlib` package, for 
Windows machines that cannot compile it.
Put this file in the SAME FOLDER as the 
notebooks. `import hnswlib` will then pick 
it
up instead of the real package. It 
implements only the calls the workshop 
notebooks
use (Index, init_index, add_items, set_ef, 
knn_query) on top of faiss's HNSW index
(faiss.IndexHNSWFlat), which has the same 
three knobs: M, efConstruction, efSearch.
Requires: pip install faiss-cpu numpy
"""
import numpy as np
import faiss
__all__ = ["Index"]
class Index:
    def __init__(self, space="cosine", 
dim=None):
        if space not in ("cosine", "l2", 
"ip"):
            raise ValueError("space must be 
'cosine', 'l2' or 'ip'")
        self.space = space
        self.dim = dim
        self._index = None
        self._ids = np.zeros(0, 
dtype=np.int64)
        self._ef = 10
    def init_index(self, max_elements=0, 
ef_construction=200, M=16,
                   random_seed=100, 
allow_replace_deleted=False):
        metric = faiss.METRIC_L2 if 
self.space == "l2" else 
faiss.METRIC_INNER_PRODUCT
        self._index = 
faiss.IndexHNSWFlat(self.dim, M, metric)
        self._index.hnsw.efConstruction = 
ef_construction
        self._index.hnsw.efSearch = 
self._ef
norms)
    def _prep(self, data):
        x = 
np.ascontiguousarray(np.asarray(data, 
dtype="float32"))
        if x.ndim == 1:
            x = x.reshape(1, -1)
        if self.space == "cosine":
            norms = 
np.maximum(np.linalg.norm(x, axis=1, 
keepdims=True), 1e-12)
            x = np.ascontiguousarray(x / 
        return x
    def add_items(self, data, ids=None, 
num_threads=-1, replace_deleted=False):
        x = self._prep(data)
        n = len(x)
        if ids is None:
            ids = np.arange(len(self._ids), 
len(self._ids) + n)
        self._ids = 
np.concatenate([self._ids, np.asarray(ids, 
dtype=np.int64).reshape(-1)])
        self._index.add(x)
    def set_ef(self, ef):
        self._ef = int(ef)
        if self._index is not None:
            self._index.hnsw.efSearch = 
self._ef
    def knn_query(self, data, k=1, 
num_threads=-1, filter=None):
        q = self._prep(data)
        sims, pos = self._index.search(q, 
k)
        labels = np.where(pos >= 0, 
self._ids[np.clip(pos, 0, None)], -1)
        # hnswlib reports 1 - similarity 
for cosine/ip, squared distance for l2
        dists = sims if self.space == "l2" 
else 1.0 - sims
        return labels, dists