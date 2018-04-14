
class EmitTarget(object):

    __slots__ = ['args', 'kwargs', 'state']

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.state = None

    def emit(self, thing):
        raise NotImplementedError


class AppendToFile(EmitTarget):

    def emit(self, thing):
        if self.state is None:
            if hasattr(self.args[0], 'write'):
                self.state = {"file": self.args[0]}
            else:
                self.state = {"file": open(*self.args, "w+", **self.kwargs)}
        self.state["file"].write(thing)
        self.state["file"].flush()

    def __del__(self):
        if self.state is not None:
            self.state["file"].close()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.args[0]}>"


class SnapshotToFile(AppendToFile):

    def emit(self, thing):
        if self.state is None:
            if hasattr(self.args[0], 'write'):
                self.state = {"file": self.args[0]}
            else:
                self.state = {"file": open(*self.args, "w+", **self.kwargs)}
        self.state["file"].seek(0)
        self.state["file"].write(thing)
        self.state["file"].flush()
        self.state["file"].truncate()


if __name__ == '__main__':
    import sys
    e = AppendToFile(sys.stdout)
    e.emit("Test")
