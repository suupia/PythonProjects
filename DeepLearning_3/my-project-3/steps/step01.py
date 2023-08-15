import numpy as np

class Variable:
      def __init__(self, data):
            self.data = data

data = np.array(1.0)
x = Variable(data)
print(x.data)
x.data = np.array(2.0)
print(x.data)

class Function:
      def __call__(self, input):
            x = input.data
            y = x ** 2
            output = Variable(y)
            return output

x = Variable(np.array(10))
f = Function()
y = f(x)

print(type(y)) # type()を使って、オブジェクトの方を取得
print(y.data)
