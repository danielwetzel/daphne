# Copyright 2023 The DAPHNE Consortium
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from api.python.context.daphne_context import DaphneContext
import torch as torch
import numpy as np

dc = DaphneContext()

# Example usage for a 3x3 tensor
tensor2d = torch.tensor(np.arange(15).reshape((5, 3)))

# Print the tensor
print("How the 2d Tensor looks in Python:")
print(tensor2d)

T2D = dc.from_pytorch(tensor2d, verbose=True)

print("\nHow DAPHNE sees the 2d tensor from tensorflow:")
T2D.print().compute(isPytroch=True, verbose=True)


# Example usage for a 3x3x3 tensor
tensor3d = torch.tensor(np.arange(27).reshape((3, 3, 3)))

# Print the tensor
print("How the 3d Tensor looks in Python:")

# Example usage for a 4x3x3x3 tensor
tensor4d = torch.tensor(np.arange(108).reshape((4, 3, 3, 3)))

# Print the tensor
print("How the 4d Tensor looks in Python:")