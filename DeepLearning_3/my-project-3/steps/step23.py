import numpy as np
from ..dezero.core_simple import Variable

x = Variable(np.array(1.0))
print(x)

# cannot Compile Thie Code By "Python step23.py"
# you will get the following error:
#
# Traceback (most recent call last):
#   File "/Users/moritakoki/PythonProjects/DeepLearning_3/my-project-3/steps/step23.py", line 2, in <module>
#     from ..dezero.core_simple import Variable
# ImportError: attempted relative import with no known parent package


# これはstep23.pyをメインモジュールとしてコンパイルすることになり、メインモジュールでは相対インポートが使えないから
