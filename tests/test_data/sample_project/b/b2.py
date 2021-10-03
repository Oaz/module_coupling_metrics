from ..a import A1Public, A2Public


class B2Tool(A1Public, A2Public):
    def qix(self):
        return 7

    def qix2(self):
        return 2

    def fizz(self):
        return self.bar() + self.bar2()


class B2(A2Public):
    def qix2(self):
        return 31

    def buzz(self):
        return self.bar2() * B2Tool().fizz()
