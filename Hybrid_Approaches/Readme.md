# Hybrid Multi-Agent Path Finding (MAPF) Approaches

This document outlines three hybrid methods that combine **Network Flow**, **Linear Programming (LP) Relaxation**, and **Mixed-Integer Linear Programming (MILP)** for scalable and near-optimal multi-agent path planning.

---

## Hybrid A: LP Relaxation → MILP Refinement

### Concept
This approach first computes an approximate solution using a Network Flow LP relaxation, then refines it with a MILP that resolves only the remaining conflicts and enforces integer feasibility.  
It leverages the speed of LP for global reasoning and the precision of MILP for local correction.

---

### Process

#### Step 1: Network Flow LP
An LP relaxation of the multi-agent flow problem is solved, treating agent flows as fractional.  
This provides a near-optimal set of flow values for each agent across the space-time graph.

#### Step 2: Path Extraction
Paths are extracted by rounding the fractional LP flow values.  
Some agents may appear "split" across edges or collide in time due to the relaxation.

#### Step 3: MILP Refinement
A smaller MILP is formulated only for the conflicting agents or regions identified after the LP phase.  
All other paths remain fixed.  
The MILP resolves vertex and edge collisions, producing a discrete, collision-free solution.

---

### Why It Works
- LP captures global optimality structure efficiently.  
- Most of the solution is already correct after the LP phase.  
- The MILP only focuses on the remaining conflicts, reducing problem complexity.  
This hybrid combines the **global efficiency** of LP with the **local exactness** of MILP.

---

## Hybrid B: Flow-Generated Path Candidates → MILP Column Generation

### Concept
This approach uses Network Flow to generate multiple feasible path candidates per agent, and then a MILP selects a conflict-free combination.  
It decouples **path generation** from **path selection**, simplifying the optimization process.

---

### Process

#### Step 1: Candidate Path Generation
Each agent independently computes several diverse paths using shortest-path searches on a time-expanded graph.  
Edge costs are updated after each path to promote diversity.  
This produces a small set of high-quality candidate paths for each agent.

#### Step 2: Path Selection MILP
A MILP is then defined where each variable represents the selection of one candidate path for a specific agent.  
Constraints ensure:
- Each agent selects exactly one path.  
- No two selected paths share a vertex or edge at the same time.  

The objective minimizes the total path cost while maintaining collision-free operation.

#### Step 3: Column Generation (Optional)
If no feasible combination exists, additional candidate paths are generated using dual information from the MILP and added iteratively.  
This expands the solution space only as needed.

---

### Why It Works
- The combinatorial explosion of full MILP formulations is avoided.  
- Flow-generated paths provide near-optimal options upfront.  
- The MILP only decides **which** pre-computed path to assign per agent.  
This creates a compact, tractable optimization problem that retains optimality guarantees through column generation.

---

## Hybrid C: Regional Decomposition (MILP Bottlenecks + Flow Elsewhere)

### Concept
This method decomposes the map into **congested regions** and **sparse regions**, applying MILP in dense bottlenecks and faster Network Flow or heuristic planning in open spaces.  
It combines local optimality with global scalability.

---

### Process

#### Step 1: Congestion Detection
The environment is analyzed to detect regions where multiple agents interact or where paths intersect heavily (bottlenecks).  
These are identified as high-conflict zones requiring exact resolution.

#### Step 2: Regional Planning
- **Congested regions** are solved using MILP for guaranteed collision-free routing.  
- **Sparse regions** are handled using Network Flow LP or prioritized heuristics, as conflicts are rare there.  

Each region is solved independently, leveraging the most appropriate technique for its density.

#### Step 3: Interface Coordination
The interaction between regions is managed by exchanging entry and exit times.  
MILP regions specify safe time windows for transitions, which are then used to guide flow-based or heuristic planning in adjacent regions.

---

### Why It Works
- Real-world maps exhibit localized congestion rather than uniform density.  
- Solving each region with the right level of precision avoids unnecessary computational effort.  
- The integration of regional solvers ensures both local optimality and global consistency.  

This hybrid reflects a **divide-and-conquer** strategy: apply exact methods only where necessary, and lightweight methods elsewhere.

---

## Comparison of the Three Hybrids

| Hybrid | Core Idea | Main Strategy |
|--------|------------|----------------|
| A: LP → MILP | Start with LP, refine with MILP | Use LP for approximation, MILP for conflict repair |
| B: Path Pool | Generate candidate paths, then select | Flow creates path options; MILP selects collision-free subset |
| C: Regional | Combine local MILP with global flow | Use MILP in bottlenecks, flow elsewhere |

---

## Implementation Roadmap

| Phase | Focus | Description |
|-------|--------|-------------|
| **Phase 1** | Hybrid A | Establish LP → MILP pipeline; foundation for hybrid solving |
| **Phase 2** | Hybrid B | Integrate candidate path generation and selection MILP |
| **Phase 3** | Hybrid C | Extend solver with regional decomposition for realistic maps |

---

## Summary

Traditional methods face a trade-off between **optimality** (MILP) and **scalability** (Network Flow).  
These hybrid methods bridge that gap by combining fast approximate solvers with targeted exact refinements.  

- **LP provides global efficiency**  
- **MILP ensures local exactness**  
- **Regional and candidate-based strategies enhance scalability**  

Together, they define a practical framework for real-world multi-agent path finding.
