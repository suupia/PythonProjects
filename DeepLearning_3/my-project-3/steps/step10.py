import numpy as np
import unittest

class Variable:
      def __init__(self, data):
            if data is not None:
                  if not isinstance(data, np.ndarray):
                        raise TypeError('{} is not supported'.format(type(data)))

            self.data = data
            self.grad = None
            self.creator = None

      def set_creator(self, func):
            self.creator = func

      def backward(self):
            if self.grad is None:
                  self.grad = np.ones_like(self.data)

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
            output = Variable(as_array(y))
            output.set_creator(self) # 出力変数に生みの親を覚えさせる
            self.input = input # 入力された変数を覚える
            self.output = output # 出力も覚える
            return output

      def forward(self,x):
            raise NotImplementedError()

      def backward(self,gy):
            raise NotImplementedError()

def as_array(x):
      if np.isscalar(x):
            return np.array(x)
      return x

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

def square(x):
      return Square()(x)

def exp(x):
      return Exp()(x)

class SquareTest(unittest.TestCase):
    def test_forward(self):
        x = Variable(np.array(2.0))
        y = square(x)
        expected = np.array(4.0)
        self.assertEqual(y.data, expected)

    def test_backward(self):
          x = Variable(np.array(3.0))
          y = square(x)
          y.backward()
          expected = np.array(6.0)
          self.assertEqual(x.grad, expected)

    # 勾配確認による自動テスト
    def test_gradient_check(self):
          x = Variable(np.random.rand(1))  # ランダムな入力値を生成
          y = square(x)
          y.backward()
          num_grad = numerical_diff(square, x)
          flg = np.allclose(x.grad, num_grad)
          self.assertTrue(flg)