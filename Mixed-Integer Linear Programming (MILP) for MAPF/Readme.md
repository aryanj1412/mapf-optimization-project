# Mixed-Integer Linear Programming (MILP) for Multi-Agent Path Finding (MAPF)

This directory contains a complete **Mixed-Integer Linear Programming (MILP)** implementation for the **Multi-Agent Path Finding (MAPF)** problem, using **time-indexed binary variables** and the open-source **PuLP** solver.

> **Exact Optimal Solutions:**  
> MILP provides provably optimal solutions with integer decision variables, serving as the gold standard for small to medium MAPF instances.

---

## Research Background

### Time-Indexed MILP Formulation

**Foundation:**  
Based on classical discrete optimization approaches where each agent’s position at every timestep is modeled as a binary decision variable.

**Key References:**

1. **Gao et al. (2023)** – *Multi-Agent Path Finding with Time Windows*, AAMAS-23  
   [PDF](https://www.ifaamas.org/Proceedings/aamas2023/pdfs/p2586.pdf)
2. **Yu & LaValle (2013)** – *Optimal Multirobot Path Planning on Graphs*, IEEE Transactions on Robotics  
   [Link](https://ieeexplore.ieee.org/document/6582929)
3. **Erdem et al. (2013)** – *Integer Programming for Automated Multi-Agent Path Finding*, AAAI-13  
   [Link](https://www.aaai.org/ocs/index.php/AAAI/AAAI13/paper/view/6347)

---

## Algorithm Overview

# Mathematical Formulation

## Variables

$$
x_{i,v,t} =
\begin{cases}
1 & \text{if agent } i \text{ is at vertex } v \text{ at time } t \\
0 & \text{otherwise}
\end{cases}
$$

$$
g_{i,t} =
\begin{cases}
1 & \text{if agent } i \text{ reaches goal at time } t \\
0 & \text{otherwise}
\end{cases}
$$

$$
a_{i,t} =
\begin{cases}
1 & \text{if agent } i \text{ is active at time } t \\
0 & \text{otherwise}
\end{cases}
$$

---

## Objective

$$
\text{Minimize: } \sum_i \sum_{t=1}^{T} t \cdot g_{i,t} \quad \text{(sum-of-costs objective)}
$$

---

## Constraints

1. **Initial Conditions**

    $$x_{i,s_i,0} = 1,\quad a_{i,0} = 1 \quad \forall i$$

2. **Goal Conditions**

    $$\sum_{t=0}^{T} g_{i,t} = 1 \quad \forall i$$

    $$g_{i,t} \le x_{i,\text{goal}_i,t} \quad \forall i,t$$

3. **Flow Conservation**

    $$\sum_{v \in V} x_{i,v,t} = a_{i,t} \quad \forall i,t$$

4. **Movement Constraints**

    $$x_{i,v,t+1} \le \sum_{u \in N(v)} x_{i,u,t} \quad \forall i,v,t$$

5. **Vertex Collision Avoidance**

    $$\sum_{i} x_{i,v,t} \le 1 \quad \forall v,t$$

6. **Edge Collision Avoidance**

    $$x_{i,u,t} + x_{j,v,t} + x_{i,v,t+1} + x_{j,u,t+1} \le 3
    \quad \forall i \ne j,\ (u,v) \in E,\ t$$

    *(Prevents agents from swapping positions.)*

7. **Active Agent Constraints**

    $$a_{i,t+1} \le a_{i,t}$$

    $$a_{i,t} \le 1 - \sum_{s=0}^{t-1} g_{i,s}$$



## Implementation Details

### Architecture Overview

| Class / Function | Description |
|------------------|-------------|
| **Agent** | Dataclass containing `id`, `start`, and `goal` |
| **MAPF_Instance** | Manages grid, agents, obstacles, and graph generation |

### Core Components

| Component | Purpose |
|-----------|----------|
| `gen_vertices()` | Generate free vertices (excluding obstacles) |
| `gen_edges()` | Create 4-connected grid graph |
| `get_nbr()` | Return neighbors (including wait action) |
| `create_vars()` | Initialize binary variables (x, g, a) |
| `create_obj()` | Define the sum-of-costs objective |
| `add_constr()` | Add all constraints to the MILP model |
| `solve()` | Invoke CBC solver with time limit |
| `extract_sol()` | Parse solver output into agent paths |
| `visualize_sol()` | Visualize the resulting paths |

### Constraint Breakdown

1. `initial_conditions()` – Start positions  
2. `goal_conditions()` – Goal timing and uniqueness  
3. `active_agent_constr()` – Agent activation states  
4. `flow_conservation()` – One position per active agent  
5. `mov_constr()` – Valid movement transitions  
6. `vertex_collision_avoid()` – No two agents at same vertex  
7. `edge_collision_avoid()` – No edge swaps  

---

## Tech Stack

| Component | Version | Purpose |
|-----------|----------|---------|
| **Python** | 3.8+ | Core implementation |
| **PuLP** | 2.7+ | MILP modeling |
| **CBC** | 2.10+ | Open-source MILP solver (bundled with PuLP) |
| **NumPy** | 1.21+ | Array operations |
| **Matplotlib** | 3.5+ | Visualization |

### Why PuLP + CBC?

- **Open-source:** No commercial license needed  
- **Simple installation:** `pip install pulp`  
- **Good performance:** CBC is competitive for small–medium MAPF instances  
- **Python-native:** Clean, readable API  

---

## Example: 7 Agents on a 10×10 Grid

### Problem Setup


agents = [
    Agent(id=0, start=(1,0), goal=(3,9)),
    Agent(id=1, start=(9,1), goal=(1,8)),
    Agent(id=2, start=(3,3), goal=(9,8)),
    Agent(id=3, start=(8,5), goal=(3,1)),
    Agent(id=4, start=(5,7), goal=(8,2)),
    Agent(id=5, start=(1,7), goal=(7,0)),
    Agent(id=6, start=(8,9), goal=(0,2))
]

obstacles = [
    (3,0), (8,0), (9,0), (5,1), (1,3), (5,4),
    (6,4), (9,4), (2,5), (3,7), (7,7), (0,8),
    (6,8), (0,9), (5,9), (9,9)
]


### Problem Complexity

Decision Variables:
x-variables: 7 agents × 84 vertices × 16 timesteps = 9,408
g-variables: 7 agents × 16 timesteps = 112
a-variables: 7 agents × 16 timesteps = 112
TOTAL: 9,632 binary variables

Constraints:
Initial conditions: ~600
Goal conditions: ~350
Flow conservation: ~112
Movement: ~9,408
Vertex collisions: ~1,344
Edge collisions: ~50,000+
Active agent: ~350
TOTAL: ~62,000+ constraints


## 🔬 Key Insights

### Advantages Over Network Flow

1. **Integer Solutions**
   - No fractional flows requiring rounding
   - Direct path extraction from binary variables

2. **Simpler Formulation**
   - No multi-commodity routing complexity
   - Clearer constraint structure

3. **Open-Source Friendly**
   - PuLP + CBC = completely free
   - Network Flow typically needs Gurobi

### Why Hybrids Are Needed

**Problem:** MILP optimal but slow, Network Flow fast but approximate, Search scalable but complex.

**Solution: Hybrid Approaches**

1. **Flow LP → MILP Refinement**
   - Network Flow gives initial solution
   - MILP fixes conflicts and improves quality

2. **Regional MILP**
   - MILP for congested bottlenecks (3-5 agents)
   - Fast heuristics for sparse regions

3. **Column Generation**
   - MILP master problem
   - Flow-based subproblems

**See:** [`Hybrid_Approaches/`](../Hybrid_Approaches/) for implementations.

## 📖 Related Publications

### MILP for MAPF

1. **Gao et al. (2023):** ILP formulation with time windows. [[AAMAS]](https://www.ifaamas.org/Proceedings/aamas2023/pdfs/p2586.pdf)
2. **Erdem et al. (2013):** ASP-based MAPF solving. [[AAAI]](https://www.aaai.org/ocs/index.php/AAAI/AAAI13/paper/view/6347)
3. **Yu & LaValle (2013):** ILP and network flow comparison. [[IEEE]](https://ieeexplore.ieee.org/document/6582929)

### Alternative Approaches

4. **Sharon et al. (2015):** CBS (search-based optimal). [[AI Journal]](https://www.sciencedirect.com/science/article/pii/S0004370214001386)
5. **Okumura (2023):** LaCAM2 (anytime search). [[IJCAI]](https://www.ijcai.org/proceedings/2023/28)

## 🔗 Related Directories

- **Network Flow Implementation:** [`Network_Flow_Implementation/`](../Network_Flow_Implementation/) - LP relaxation approach
- **LaCAM2 Baseline:** [`LaCAM2_Baseline/`](../LaCAM2_Baseline/) - Search-based optimal (50+ agents)
- **Classical Network Flow:** [`Classical_Network_Flow_Demo/`](../Classical_Network_Flow_Demo/) - Educational primer
- **Hybrid Approaches:** [`Hybrid_Approaches/`](../Hybrid_Approaches/) - Combined methods (coming soon)

## 🙏 Acknowledgments

- **PuLP Development Team** for the open-source MILP modeling library
- **COIN-OR CBC** for the free solver
- **MAPF research community** for constraint formulations and benchmarks

---

**Status:** Core MILP implementation complete. Hybrid extensions in development.  
**Last Updated:** October 5, 2025
