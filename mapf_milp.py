import pulp
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import time

@dataclass
class Agent:
    id: int
    start: Tuple[int, int]
    goal: Tuple[int, int]

class MAPF_Instance:
    def __init__(self, width: int, height: int, agents:List[Agent], obst: List[Tuple[int, int]] = None):
        self.width = width
        self.height = height
        self.agents = agents
        self.obst = set(obst) if obst else set()
        self.vertices = self.gen_vertices()
        self.edges = self.gen_edges()

    def gen_vertices(self) -> List[Tuple[int, int]]:
        vertices = []
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.obst:
                    vertices.append((x, y))
        return vertices

    def gen_edges(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        edges = []
        dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        for vertex in self.vertices:
            x, y = vertex
            for dx, dy in dir:
                nbr = (x + dx, y + dy)
                if nbr in self.vertices:
                    edges.append((vertex, nbr))
        return edges

    def get_nbr(self, vertex: Tuple[int, int]) -> List[Tuple[int ,int]]:
        x, y = vertex
        nbrs = [vertex]
        dir = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        for dx, dy in dir:
            nbr = (x + dx, y + dy)
            if nbr in self.vertices:
                nbrs.append(nbr)
        return nbrs

    def compute_min_individual_paths(self) -> int:
        max_individual_path = 0
        for agent in self.agents:
            min_dist = abs(agent.start[0] - agent.goal[0]) + abs(agent.start[1] - agent.goal[1])
            max_individual_path = max(max_individual_path, min_dist)
        return max_individual_path

class MAPF_MILP_Solver:
    def __init__(self, instance: MAPF_Instance, time_horizon: int  = 15, obj_type: str = "sum_of_costs"):
        self.instance = instance
        self.T = time_horizon
        self.obj_type = obj_type
        self.model = None
        self.x_vars = {}
        self.g_vars = {}
        self.a_vars = {}
        self.sol_paths = {}
        self.sol_time = 0
        self.is_opt = False

    def create_model(self):
        self.model = pulp.LpProblem("MAPF_MILP", pulp.LpMinimize)
        self.create_vars()
        self.create_obj()
        self.add_constr()

    def create_vars(self):
        for i, agent in enumerate(self.instance.agents):
            for v in self.instance.vertices:
                for t in range(self.T + 1):
                    var_name = f"x_{i}_{v[0]}_{v[1]}_{t}"
                    self.x_vars[(i, v, t)] = pulp.LpVariable(var_name, cat= "Binary")

        for i, agent in enumerate(self.instance.agents):
            for t in range(self.T + 1):
                var_name = f"g_{i}_{t}"
                self.g_vars[(i, t)] = pulp.LpVariable(var_name, cat="Binary")

        for i, agent in enumerate(self.instance.agents):
            for t in range(self.T + 1):
                var_name = f"a_{i}_{t}"
                self.a_vars[(i, t)] = pulp.LpVariable(var_name, cat="Binary")

    def create_obj(self):
        obj = pulp.lpSum([
            t * self.g_vars[(i, t)]
            for i, agent in enumerate(self.instance.agents)
            for t in range(1, self.T + 1)
        ])
        self.model += obj

    def add_constr(self):
        self.initial_conditions()
        self.goal_conditions()
        self.active_agent_constr()
        self.flow_conservation()
        self.mov_constr()
        self.vertex_collision_avoid()
        self.edge_collision_avoid()

    def flow_conservation(self):
        for i in range(len(self.instance.agents)):
            for t in range(self.T + 1):
                constr = pulp.lpSum([
                    self.x_vars[(i, v, t)] for v in self.instance.vertices
                ]) == self.a_vars[(i, t)]
                self.model += constr, f"Flow_conservation agent {i} time {t}"

    def initial_conditions(self):
        for i, agent in enumerate(self.instance.agents):
            self.model += self.x_vars[(i, agent.start, 0)] == 1, f"Initial_Agent {i}"

            self.model += self.a_vars[(i, 0)] == 1, f"Initially_active_{i}"

            for v in self.instance.vertices:
                if v!= agent.start:
                    self.model += self.x_vars[(i, v, 0)] == 0, f"Initial agent {i} not {v[0]}_{v[1]}"

    def goal_conditions(self):
        for i, agent in enumerate(self.instance.agents):
            constr = pulp.lpSum([
                self.g_vars[(i, t)] for t in range(self.T + 1)
            ]) == 1
            self.model += constr, f"Goal_reached_once_{i}"

            for t in range(self.T +1):
                self.model += self.g_vars[(i, t)] <= self.x_vars[(i, agent.goal, t)], f"Goal_reached_{i}_{t}"

            for t in range(1, self.T +1):
                prev_goals = pulp.lpSum([self.g_vars[(i, s)] for s in range(t)])
                self.model += self.g_vars[(i, t)] <= 1 - prev_goals, f"goal_reached_once_{i}_{t}"

    def active_agent_constr(self):
        for i, agent in enumerate(self.instance.agents):
            for t in range(1, self.T + 1):
                goal_so_far = pulp.lpSum([self.g_vars[(i, s)] for s in range(t)])
                self.model += (self.a_vars[(i, t)] <= 1 - goal_so_far), f"inactive_after_goal_{i}_{t}"

            for t in range(self.T):
                self.model += self.a_vars[(i, t+1)] <= self.a_vars[(i, t)], f"Stay_inactive_{i}_{t}"

    def mov_constr(self):
        for i in range(len(self.instance.agents)):
            for v in self.instance.vertices:
                for t in range(self.T):
                    nbrs = self.instance.get_nbr(v)
                    constr = self.x_vars[(i, v, t+1)] <= pulp.lpSum([
                        self.x_vars[(i, u, t)] for u in nbrs
                    ])
                    self.model += constr, f"mov_agent {i} vertex ({v[0]}, {v[1]}) time {t}"

    def vertex_collision_avoid(self):
        for v in self.instance.vertices:
            for t in range(self.T +1):
                constr = pulp.lpSum([
                    self.x_vars[(i, v, t)] for i in range(len(self.instance.agents))
                ]) <= 1
                self.model += constr, f"vertex_collision ({v[0]}, {v[1]}) time {t} "

    def edge_collision_avoid(self):
        for u, v in self.instance.edges:
            for t in range(self.T):
                for i in range(len(self.instance.agents)):
                    for j in range(i+1, len(self.instance.agents)):
                        constr = (
                            self.x_vars[(i, u, t)] + self.x_vars[(j, v, t)] +
                            self.x_vars[(i, v, t+1)] + self.x_vars[(j, u, t+1)]
                        ) <= 3
                        self.model += constr, f"edge_collision {i}, {j} _ ({u[0]}, {u[1]}) _ ({v[0]}, {v[1]}) _ time {t}"


    def solve(self, time_limit: int = 300, verbose: bool = True) -> bool:
        if self.model is None:
            self.create_model()

        start_time = time.time()
        if verbose:
            print(f"solving MAPF instance with {len(self.instance.agents)} agents...")
            print(f"Variables: {len(self.x_vars) + len(self.g_vars) + len(self.a_vars)}, Time horizon: {self.T}")

        solver = pulp.PULP_CBC_CMD(timeLimit= time_limit, msg= verbose)
        status = self.model.solve(solver)
        self.solve_time = time.time() - start_time

        if status == pulp.LpStatusOptimal:
            self.is_opt = True
            self.extract_sol()
            if verbose:
                print(f"Optimal solution found in {self.solve_time:.2f} seconds")
                print(f"Objective value: {pulp.value(self.model.objective)}")
            return True
        else:
            if verbose:
                print(f"No optimal solutions found. Status: {pulp.LpStatus[status]}")
            return False

    def extract_sol(self):
        self.sol_paths = {i: [] for i in range(len(self.instance.agents))}
        self.goal_times = {}

        for i in range(len(self.instance.agents)):
            goal_time = None
            for t in range(self.T + 1):
                if self.g_vars[(i, t)].varValue == 1:
                    goal_time = t
                    break

            self.goal_times[i] = goal_time

            if goal_time is not None:
                for t in range(goal_time +1):
                    for v in self.instance.vertices:
                        if self.x_vars[(i, v, t)].varValue == 1:
                            self.sol_paths[i].append(v)
                            break

    def sol_metrics(self) -> Dict[str, float]:
        if not self.sol_paths:
            return {}

        metrics = {}
        sum_of_costs = 0
        for i, agent in enumerate(self.instance.agents):
            path_length = len(self.sol_paths[i]) - 1
            sum_of_costs += path_length

        metrics['sum_of_costs'] = sum_of_costs
        metrics['solve_time'] = self.solve_time

        return metrics

    def visualize_sol(self, save_path: Optional[str] = None):
        if not self.sol_paths:
            print("No Solution to visualize")
            return

        fig, ax = plt.subplots(1, 1, figsize=(12,12))

        for x in range(self.instance.width +1):
            ax.axvline(x-0.5, color='lightgray', linewidth=0.5)
        for y in range(self.instance.height +1):
            ax.axhline(y-0.5, color='lightgray', linewidth=0.5)

        for obs in self.instance.obst:
            ax.add_patch(plt.Rectangle((obs[0]-0.5, obs[1] -0.5), 1, 1,
                                       facecolor='black', alpha=0.8))

        colors = plt.cm.tab10(np.linspace(0, 1, len(self.instance.agents)))

        for i, agent in enumerate(self.instance.agents):
            color = colors[i]
            path = self.sol_paths[i]
            path_length = len(path) - 1

            ax.plot(agent.start[0], agent.start[1], 'o', color=color,
                    markersize=15, label=f'Agent {i} start', markeredgecolor='black', markeredgewidth=2)

            ax.plot(agent.goal[0], agent.goal[1], '*', color=color,
                    markersize=20, label=f'Agent {i} goal', markeredgecolor='black', markeredgewidth=1)

            if path:
                path_x = [pos[0] for pos in path]
                path_y = [pos[1] for pos in path]
                ax.plot(path_x, path_y, '-', color=color, linewidth=3, alpha=0.7,
                        label=f'Agent {i} path')


        ax.set_xlim(-0.5, self.instance.width - 0.5)
        ax.set_ylim(-0.5, self.instance.height - 0.5)
        ax.set_xlabel('X coordinate', fontsize=12)
        ax.set_ylabel('Y coordinate', fontsize=12)
        ax.set_title('MAPF Solution - MILP Approach', fontsize=14, weight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi = 300, bbox_inches='tight')

        return fig

def example() -> MAPF_Instance:
    agents = [
        Agent(id=0, start=(1,0), goal=(3,9)),
        Agent(id=1, start=(9,1), goal=(1,8)),
        Agent(id=2, start=(3,3), goal=(9,8)),
        Agent(id=3, start=(8,5), goal=(3,1)),
        Agent(id=4, start=(5,7), goal=(8,2)),
        Agent(id=5, start=(1,7), goal=(7,0)),
        Agent(id=6, start=(8,9), goal=(0,2))
    ]

    obst = [(3,0), (8,0), (9,0), (5,1), (1,3), (5,4), (6,4), (9,4), (2,5), (3,7), (7,7), (0,8), (6,8), (0,9), (5,9), (9,9)]

    return MAPF_Instance(width=10, height=10, agents=agents, obst=obst)

def run_example():
    print("Running MAPF MILP Example:")
    print("=" * 50)

    instance = example()
    print(f"Problem:{len(instance.agents)} agents, {len(instance.vertices)} vertices, {len(instance.obst)} obstacles")

    solver = MAPF_MILP_Solver(instance)
    success = solver.solve(verbose=True)

    if success:
        metrics = solver.sol_metrics()
        print("\nSolution Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value}")

        print("\nAgent Paths:")
        for i,path in solver.sol_paths.items():
            print(f" Agent {i}: {path}")

        fig = solver.visualize_sol()
        plt.show()
        return solver

    else:
        print("Failed to find solution. Increase time horizon.")
        return None

if __name__ == "__main__":
    solver1 = run_example()
