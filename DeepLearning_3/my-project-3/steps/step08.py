import numpy as np

class Variable:
      def __init__(self, data):
            self.data = data
            self.grad = None
            self.creator = None

      def set_creator(self, func):
            self.creator = func

      def backward(self):
            funcs = [self.creator]
            while funcs:
                f = funcs.pop() # 関数を取得
                x, y = f.input, f.output # 関数の入出力を取得
                x.grad = f.backward(y.grad) # backwardメソッドを呼ぶ

                if x.creator is not None:
                    funcs.append(x.creator) # 1つ前の関数をリストに追加

class Function:
      def __call__(self,input):
            x = input.data
            y = self.forward(x) # 具体的な計算はforwardメソッドで行う
            output = Variable(y)
            output.set_creator(self) # 出力変数に生みの親を覚えさせる
            self.input = input # 入力された変数を覚える
            self.output = output # 出力も覚える
            return output

      def forward(self,x):
            raise NotImplementedError()

      def backward(self,gy):
            raise NotImplementedError()

class Square(Function):
      def forward(self,x):
            y = x **2
            return y

      def backward(self, gy):
            x = self.input.data
            gx = 2 * x * gy
            return gx

class Exp(Function):
      def forward(self, x):
            y = np.exp(x)
            return y

      def backward(self, gy):
            x = self.input.data
            gx = np.exp(x) * gy
            return gx

def numerical_diff(f,x,eps=1e-4):
      x0 = Variable(x.data - eps)
      x1 = Variable(x.data + eps)
      y0 = f(x0)
      y1 = f(x1)
      return (y1.data - y0.data ) / (2 * eps)

A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)
b = B(a)
y = C(b)

# 逆伝搬
y.grad = np.array(1.0)
y.backward()
print(x.grad)

# y.grad = np.array(1.0)
# b.grad = C.backward(y.grad)
# a.grad = B.backward(b.grad)
# x.grad = A.backward(a.grad)
# print(x.grad)
