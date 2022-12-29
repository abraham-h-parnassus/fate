from criticalpath import Node

from output import print_csv, print_html
from tree import TREE

# Умова в методичці по ПЗ.
OVERHEAD_COST_CONSTANT = 400


def total_cost(tree):
    """
    Calculates total cost of the project.
    """
    nodes = tree.values()
    return sum([n["normal_cost"] * n["_delegate"].duration for n in nodes])


def recreate_project(nodes):
    """
    Creates the `criticalpath` graph anew.

    Due to an issue in the library, you can do calculation only once per tree.
    If you want to update duration and re-calculate, you need to create the new one.
    """
    root = Node('project')
    node_map = {}
    for name, node in nodes.items():
        duration = node["duration"]
        _delegate = root.add(Node(name, duration=duration))
        _delegate.crash_duration = node["crash_duration"]
        _delegate.crash_cost = node["crash_cost"]
        _delegate.normal_cost = node["normal_cost"]
        node["_delegate"] = _delegate
        node_map[name] = _delegate
    for name, node in nodes.items():
        _delegate = node_map[name]
        for dep_name in node["depends_on"]:
            dependency = node_map[dep_name]
            root.link(_delegate, dependency)
    return root


if __name__ == '__main__':
    project = recreate_project(TREE)

    # Does forward and backward passes
    project.update_all()

    print("Critical path: ")
    print(project.get_critical_path())

    for node in TREE.values():
        node["_delegate"].print_times()

    result = list()

    overhead_cost = project.duration * OVERHEAD_COST_CONSTANT
    direct_cost = total_cost(TREE)
    initial_run = {
        "cost": 0,
        "savings": 0,
        "duration": project.duration,
        "total_overhead": overhead_cost,
        "direct_cost": direct_cost,
        "project_cost": overhead_cost + direct_cost
    }
    for name, node in TREE.items():
        node["saved_days"] = 0
        initial_run[name] = {
            "duration": node["_delegate"].duration,
            "crash_duration": node["crash_duration"],
            "crash_cost": node["crash_cost"],
            "normal_cost": node["normal_cost"],
            "tf": node["_delegate"].ls - node["_delegate"].es
        }
    result.append(initial_run)

    for _ in range(0, len(TREE)):
        crashables = [n for n in project.get_critical_path() if TREE[n.name]["crash_duration"] != n.duration]
        if len(crashables) == 0:
            break
        node_to_crash = min(crashables, key=lambda n: TREE[n.name]["crash_cost"])
        original_node = TREE[node_to_crash.name]
        original_node["duration"] -= 1
        original_node["saved_days"] += 1
        project = recreate_project(TREE)
        project.update_all()
        run = {}
        for name, node in TREE.items():
            run[name] = {
                "saved_days": node["saved_days"],
                "duration": node["_delegate"].duration
            }
        run["cost"] = original_node["crash_cost"]
        run["savings"] = (result[-1]["duration"] - project.duration) * OVERHEAD_COST_CONSTANT
        run["total_overhead"] = project.duration * OVERHEAD_COST_CONSTANT
        run["direct_cost"] = total_cost(TREE)
        run["project_cost"] = run["total_overhead"] + run["direct_cost"]
        run["duration"] = project.duration
        result.append(run)
    print_csv(result)
    print_html(result)
