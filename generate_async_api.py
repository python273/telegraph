"""Generate async api from sync api"""
from typing import Optional

import libcst as cst
from libcst._nodes.expression import Await
from libcst._nodes.whitespace import SimpleWhitespace


class SyncToAsyncTransformer(cst.CSTTransformer):
    def __init__(self):
        self.stack = []
        self.fn_should_async = None

    # PATH MAKING
    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.stack.append(node.name.value)

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.CSTNode:
        self.stack.pop()
        return updated_node

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.stack.append(node.name.value)

    # END PATH MAKING

    def leave_ImportAlias(
        self, original_node: cst.ImportAlias, updated_node: cst.ImportAlias
    ) -> cst.CSTNode:
        """Replace requests import with httpx"""

        if original_node.name.value == "requests":
            return updated_node.with_changes(
                name=cst.Name("httpx"),
            )

        return updated_node

    def leave_Attribute(
        self, original_node: cst.Attribute, updated_node: cst.Attribute
    ) -> cst.CSTNode:
        """Replace requests attrs with httpx attrs"""

        if (
            isinstance(original_node.value, cst.Name)
            and original_node.value.value == "requests"
        ):
            mapping = {"Session": "AsyncClient"}

            return updated_node.with_changes(
                value=cst.Name("httpx"),
                attr=cst.Name(mapping[original_node.attr.value]),
            )

        return updated_node

    def leave_Call(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef):
        """Await calls to `method` of TelegraphApi"""
        path = []

        a = original_node.func
        while isinstance(a, cst.Attribute) or isinstance(a, cst.Name):
            if isinstance(a, cst.Attribute):
                path.append(a.attr.value)
            else:
                path.append(a.value)
            a = a.value

        # await the call if it's API class method
        should_await = (
            path[-2:] == ["session", "self"]
            or path[-3:] == [
                "method",
                "_telegraph",
                "self",
            ]
            or path[-3:] == [
                "upload_file",
                "_telegraph",
                "self",
            ]
        )
        if not should_await:
            return updated_node

        self.fn_should_async = self.stack  # mark current fn as async on leave
        # await the call
        return Await(
            updated_node,
            lpar=[cst.LeftParen()],
            rpar=[cst.RightParen()],
        )

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ):
        should_async = self.stack == self.fn_should_async
        self.fn_should_async = None
        self.stack.pop()

        if not should_async:
            return updated_node

        # mark fn as async
        return updated_node.with_changes(
            asynchronous=cst.Asynchronous()
        )


def main():
    with open("telegraph/api.py") as f:
        py_source = f.read()

    source_tree = cst.parse_module(py_source)

    transformer = SyncToAsyncTransformer()
    modified_tree = source_tree.visit(transformer)

    with open("telegraph/aio.py", "w") as f:
        f.write(modified_tree.code)


if __name__ == "__main__":
    main()
