class A2Local:
    def foo(self):
        return 83


class A2Public:
    def qix2(self):
        return 0

    def bar2(self):
        return A2Local().foo() * self.qix2()
