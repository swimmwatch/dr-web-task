from container import Container

if __name__ == "__main__":
    container = Container()
    container.wire(packages=["commands"])

    repl = container.repl()
    repl.execute()
