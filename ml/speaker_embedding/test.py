from pyannote.audio import Inference
from pyannote.core import Segment
from scipy.spatial.distance import cdist
from datetime import datetime


inference = Inference("pyannote/embedding", window="sliding")
# Кастует в массив [1, 512]
embedding1 = inference("/home/user/Downloads/same.wav")
embedding2 = inference("/home/user/Downloads/2.wav")
# `embeddingX` is (1 x D) numpy array extracted from the file as a whole.
# а тут хочет массив размерности 2
distance = cdist(embedding1, embedding2, metric="cosine")[0, 0]
print(distance)
# `distance` is a `float` describing how dissimilar speakers 1 and 2 are.
