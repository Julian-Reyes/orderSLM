"""A minimal reader for PIZZA's bracketed parses: `(ORDER i want (PIZZAORDER (NUMBER a ) pizza ) )`.

Written for OrderSLM (the dataset's own utils are CC-BY-NC and are not vendored).
A node is a label plus children; a child is a word or another node.
"""

from dataclasses import dataclass, field


@dataclass
class Node:
    label: str
    children: list["Node | str"] = field(default_factory=list)

    def nodes(self, label: str | None = None) -> list["Node"]:
        """Direct child nodes, optionally only those with `label`."""
        return [c for c in self.children if isinstance(c, Node) and (label is None or c.label == label)]

    def words(self) -> list[str]:
        out: list[str] = []
        for c in self.children:
            out.extend([c] if isinstance(c, str) else c.words())
        return out

    def text(self) -> str:
        return " ".join(self.words())


def parse(source: str) -> Node:
    tokens = source.replace("(", " ( ").replace(")", " ) ").split()
    if not tokens or tokens[0] != "(":
        raise ValueError("a parse starts with '('")
    stack: list[Node] = []
    root: Node | None = None
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == "(":
            if i + 1 >= len(tokens) or tokens[i + 1] in "()":
                raise ValueError(f"label expected after '(' at token {i}")
            node = Node(tokens[i + 1])
            if stack:
                stack[-1].children.append(node)
            elif root is not None:
                raise ValueError("more than one top-level node")
            else:
                root = node
            stack.append(node)
            i += 2
            continue
        if tok == ")":
            if not stack:
                raise ValueError(f"unbalanced ')' at token {i}")
            stack.pop()
        elif not stack:
            raise ValueError(f"word {tok!r} outside any node")
        else:
            stack[-1].children.append(tok)
        i += 1
    if stack or root is None:
        raise ValueError("unbalanced parse: missing ')'")
    return root
