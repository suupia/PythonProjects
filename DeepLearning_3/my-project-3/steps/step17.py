import numpy as np
import weakref

class Variable:
      def __init__(self, data):
            if data is not None:
                  if not isinstance(data, np.ndarray):
                        raise TypeError('{} is not supported'.format(type(data)))

            self.data = data
            self.grad = None
            self.creator = None
            self.generation = 0

      def set_creator(self, func):
            self.creator = func
            self.generation = func.generation + 1

      def backward(self):
            if self.grad is None:
                  self.grad = np.ones_like(self.data)

            funcs = []
            seen_set = set()

            def add_func(f):
                  if f not in seen_set:
                        funcs.append(f)
                        seen_set.add(f)
                        funcs.sort(key=lambda x: x.generation)

            add_func(self.creator)

            while funcs:  # 再帰処理をループで置き換えた
                f = funcs.pop() # 関数を取得
                # gys = [output.grad for output in f.outputs]
                gys = [output().grad for output in f.outputs]  # outputを弱参照に変えたため()が必要
                gxs = f.backward(*gys)  # アンパッキング Functionのbackwardであることに注意！
                if not isinstance(gxs, tuple):
                      gxs = (gxs, )

                for x , gx in zip(f.inputs, gxs):
                      if x.grad is None:
                            x.grad = gx
                      else:  # Noneでない時は同じ変数であるということだから加算する
                            x.grad = x.grad + gx

                      if x.creator is not None:
                            add_func(x.creator)

      def cleargrad(self):
            self.grad = None


class Function:
      def __call__(self,*inputs):
            xs = [x.data for x in inputs]
            ys = self.forward(*xs)  # アスタリスクをつけてアンパッキング
            # xs = [x0, x1]の場合、self.forward(*xs)とすれば、それはself.forward(x0, x1)として呼び出すことと同じになる
            if not isinstance(ys, tuple):  # タプルではない場合の追加対応
                  ys = (ys, )
            outputs = [Variable(as_array(y)) for y in ys]

            self.generation = max([x.generation for x in inputs])
            for output in outputs:
                  output.set_creator(self)
            self.inputs = inputs
            self.outputs = [weakref.ref(output) for output in outputs]

            return outputs if len(outputs) > 1 else outputs[0]

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
            x = self.inputs[0].data
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

class Add(Function):
      def forward(self, x0, x1):
            y = x0 + x1
            return y

      def backward(self, gy):
            return gy, gy

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

def add(x0, x1):
      return Add()(x0, x1)


for i in range(10):
      x = Variable(np.random.randn(10000))  # 巨大なデータ
      y = square(square(square(x)))  # 複雑な計算をする
