# LaCAM2 Baseline Implementation

This directory contains the implementation and results of **LaCAM2** (LaCAM*), a state-of-the-art search-based algorithm for Multi-Agent Path Finding (MAPF), serving as the optimal baseline for our project.

## 📚 Research Background

### LaCAM2 Algorithm (IJCAI 2023)

**Paper:** [*Improving LaCAM for Scalable Eventually Optimal Multi-Agent Pathfinding*](https://www.ijcai.org/proceedings/2023/28)  
**Author:** Keisuke Okumura (AIST & University of Cambridge)  
**Conference:** IJCAI-23 (International Joint Conference on Artificial Intelligence)  
**ArXiv:** [2305.03632](https://arxiv.org/abs/2305.03632)

### Algorithm Overview

LaCAM2 (LaCAM*) is an **anytime search-based algorithm** that combines the speed of sub-optimal methods with eventual convergence to optimal solutions. It extends the original LaCAM algorithm with two key enhancements:

#### Key Innovations:

1. **Lazy Successor Generation**
   - Uses adaptive PIBT (Priority Inheritance with Backtracking) to generate configurations
   - Dramatically reduces planning effort by avoiding exhaustive branching
   - Enables handling of 1,000+ agents on standard hardware

2. **Anytime Optimality**
   - Quickly finds initial sub-optimal solutions
   - Continues refining solution quality as computation time allows
   - Guarantees eventual convergence to optimal solutions (for sum-of-costs objective)

3. **Improved Configuration Generation**
   - Enhanced PIBT with "swap" operation detection
   - Prevents search from getting stuck in bottleneck situations
   - Significantly reduces search iterations in narrow passages

### Performance Characteristics

**Strengths:**
- ✅ **Complete:** Always finds a solution if one exists
- ✅ **Eventually Optimal:** Converges to optimal solution given sufficient time
- ✅ **Scalable:** Handles 1,000+ agents within seconds
- ✅ **Anytime:** Returns improving solutions over time

**Benchmark Results:**
- Solved **99% of MAPF benchmark instances** within 10 seconds
- Handles grids up to **128×128** with varying agent counts
- Supports multiple objectives: makespan, sum-of-costs, flowtime



## 📊 Implementation Results

### Problem Setup

<div align="center">
  <img src="lacam2_problem_setup.png" alt="LaCAM2 Problem Setup" width="700"/>
  <p><i>Figure 1: Initial configuration showing 10 agents (colored circles) with their start positions and goals (stars) on a 32×32 grid with obstacles (black squares)</i></p>
</div>

**Instance Details:**
- **Grid Size:** 32×32 (1024 vertices)
- **Agents:** 10 colored agents
- **Obstacles:** Random 10% density
- **Objective:** Minimize sum-of-costs (total timesteps)

### Solution Animation

<div align="center">
  <img src="lacam2_final.gif" alt="LaCAM2 Solution Animation" width="700"/>
  <p><i>Figure 2: Collision-free solution showing all agents reaching their goals. Watch agents navigate around obstacles and each other over 53 timesteps.</i></p>
</div>

### Files in This Directory

- **`MAPF_LaCAM2_Guided_Demo.ipynb`** - Complete implementation with visualization
- **`lacam2_problem_setup.png`** - Initial problem configuration
- **`lacam2_final.gif`** - Animated solution showing collision-free paths
- **`Readme.md`** - This documentation


