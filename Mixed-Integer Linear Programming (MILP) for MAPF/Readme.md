# MILP-based Multi-Agent Path Finding (MAPF) Solver

> **Globally Optimal, Collision-Free Path Planning using Mixed Integer Linear Programming**

<div align="center">
  <img src="example_solution_8.png" alt="8-Agent MAPF Solution" width="600"/>
  <br>
  <em>Optimal collision-free trajectories for 8 agents on a 12×12 grid with obstacles.</em>
</div>

---

## Overview

This project implements a **Mixed Integer Linear Programming (MILP)** formulation for the **Multi-Agent Path Finding (MAPF)** problem using **Python** and the **PuLP** optimization library.

It computes **provably optimal**, **collision-free** trajectories for multiple agents moving from unique start to goal positions on a **grid with obstacles**, minimizing the **sum of individual completion times**.

---

## Features

- **Global Optimality** via MILP
- **Vertex & Edge Collision Avoidance** (no swapping)
- **Waiting Actions Allowed**
- **Clean, Modular Code Structure**
- **Built-in Visualization** with `matplotlib`
- **Easy to Extend & Benchmark**

---

## Problem Definition

Given:
- A 2D grid of size `W × H`
- `N` agents with start `(sx, sy)` and goal `(gx, gy)`
- Obstacles (blocked cells)
- Discrete time steps

Find:
- Collision-free paths for all agents
- Minimize **sum of arrival times** at goals

---

## Mathematical Formulation

### Decision Variables

| Variable | Meaning |
|--------|--------|
| `x[i,v,t] ∈ {0,1}` | Agent `i` is at vertex `v` at time `t` |
| `g[i,t] ∈ {0,1}`   | Agent `i` reaches goal at time `t` |
| `a[i,t] ∈ {0,1}`   | Agent `i` is active at time `t` |

### Objective

```math
\min \sum_{i=1}^{N} \sum_{t=1}^{T} t \cdot g_{i,t}
```
Key Constraints

Initial Position:
x[i, start_i, 0] = 1, a[i,0] = 1
Goal Reached Once:
Σ_t g[i,t] = 1, g[i,t] ≤ x[i, goal_i, t]
Movement:
x[i,v,t+1] ≤ Σ_{u ∈ Nbr(v) ∪ {v}} x[i,u,t]
Vertex Collision:
Σ_i x[i,v,t] ≤ 1
Edge Collision (no swap):
x[i,u,t] + x[j,v,t] + x[i,v,t+1] + x[j,u,t+1] ≤ 3
