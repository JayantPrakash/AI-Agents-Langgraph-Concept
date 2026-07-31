from pathlib import Path
from typing import Literal
from typing_extensions import NotRequired, TypedDict, Optional
from langgraph.graph import END, START, StateGraph
from IPython.display import Image, display


class CalculatorState(TypedDict):
    operation: str
    number_a: float
    number_b: float
    result: Optional[float]
    error: NotRequired[str]


def add_node(state: CalculatorState) -> dict:
    state["result"] = state["number_a"] + state["number_b"]
    return state


def multiply_node(state: CalculatorState) -> dict:
    #return {"result": state["number_a"] * state["number_b"]}
    state["result"] = state["number_a"] * state["number_b"]
    return state

def invalid_node(state: CalculatorState) -> dict:
    return {"error": "Supported operations are add and multiply"}


def route_operation(
    state: CalculatorState,
) -> Literal["add", "multiply", "invalid"]:
    operation = state["operation"].lower().strip()

    if operation == "add":
        return "add"
    if operation == "multiply":
        return "multiply"
    return "invalid"


graph = StateGraph(CalculatorState)

graph.add_node("add", add_node)
graph.add_node("multiply", multiply_node)
graph.add_node("invalid", invalid_node)

graph.add_conditional_edges(
    START,
    route_operation,
    {
        "add": "add",
        "multiply": "multiply",
        "invalid": "invalid",
    },
)

graph.add_edge("add", END)
graph.add_edge("multiply", END)
graph.add_edge("invalid", END)

app = graph.compile()


def display_graph() -> None:
    """Display the graph inline in Jupyter, or print its path in a terminal."""
    graph_path = Path(__file__).with_name("calculator_graph.svg")

    try:
        from IPython import get_ipython
        from IPython.display import SVG, display

        if get_ipython() is not None:
            display(SVG(filename=str(graph_path)))
            return
    except ImportError:
        pass

    print(f"Graph: {graph_path.resolve()}")
    print(app.get_graph().draw_mermaid())


if __name__ == "__main__":
    display_graph()

    output = app.invoke(
        {
            "operation": "multiply",
            "number_a": 6,
            "number_b": 7,
        }
    )

    print(output)
    print(output["result"])

