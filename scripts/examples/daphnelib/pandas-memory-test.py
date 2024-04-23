# Copyright 2023 The DAPHNE Consortium
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from api.python.context.daphne_context import DaphneContext
import pandas as pd
import numpy as np

dc = DaphneContext()

df = pd.DataFrame(np.random.randn(20, 5))
F = dc.from_pandas(df)

#F.print().compute()

F = F.setColLabels(["label1", "label2", "label3", "label4", "label5"])
print(F.compute())

F = F.setColLabelsPrefix("F1")
print(F.compute())

M = F.toMatrix()
print(M.compute())

#print(F)

df2 = pd.DataFrame(np.random.randn(20, 3))
F2 = dc.from_pandas(df2)

F2 = F2.setColLabels(["label1", "label2", "label3"])
print(F2.compute())

F2 = F2.setColLabelsPrefix("F2")
print(F2.compute())

F2 = F2.cbind(F)

F.delete()
M.delete()

print(F2.compute())

#print(F2)

