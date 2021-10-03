class A1Local:
    def foo(self):
        return 4


class A1Public:
    def qix(self):
        return 0

    def bar(self):
        return A1Local().foo() * self.qix()
