from pyannote.audio import Inference
from pyannote.core import Segment
inference = Inference("pyannote/embedding",
                      window="whole")
# TODO взять большой файл, его разбиение, пройтись по файлу по полученным от voice_activity меткам времени спикеров и
# - тут же посчитать совпадающих спикеров
excerpt = Segment(13.37, 19.81)
embedding = inference.crop("/home/user/Downloads/2.wav", excerpt)
print(embedding)