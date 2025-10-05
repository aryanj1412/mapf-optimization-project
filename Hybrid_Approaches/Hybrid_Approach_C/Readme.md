# 🧩 Hybrid C: Regional Decomposition for MAPF

This directory implements **Hybrid Approach C: Regional Decomposition**, an intelligent strategy that combines **MILP** (optimal but slow) for congested bottlenecks with **fast prioritized planning** for sparse regions.

> **Core Idea:** Partition the workspace into regions, detect congestion, and apply computational effort where it matters most.

---

## 📚 Research Background

### 🧠 Regional Decomposition Strategy

**Foundation:**  
Hybrid C addresses the fundamental tradeoff in MAPF between solution quality and computational efficiency by *spatially decomposing* the problem.

**Key Insight:**  
Not all regions of a workspace are equally congested. Applying expensive optimal methods (MILP) everywhere is wasteful when many regions have low agent density and can be solved quickly with heuristics.

**Relevant Papers:**
1. **Ma et al. (2017)** – *Multi-Agent Path Finding with Deadlock Detection*  
   *Artificial Intelligence Journal.* [[Link]](https://www.sciencedirect.com/science/article/pii/S0004370216301308)
2. **Gao et al. (2023)** – *Multi-Agent Path Finding with Time Windows*  
   *AAMAS-23.* [[PDF]](https://www.ifaamas.org/Proceedings/aamas2023/pdfs/p2586.pdf)
3. **Cohen et al. (2015)** – *Highway Dimension and Provably Efficient Algorithm*  
   *IJCAI-15.* (Introduces regional decomposition concepts)

---

## 🎯 Algorithm Overview

### ⚙️ Three-Phase Hybrid Approach

#### Phase 1: Regional Decomposition & Congestion Detection
- Partition grid into rectangular cells (e.g., 3×3 regions)
- Analyze agent density in each region
- Classify regions as:
  - **Congested** (≥ threshold agents)
  - **Sparse** (< threshold agents)

#### Phase 2: MILP for Congested Bottlenecks
- Extract agents passing through congested regions
- Formulate regional MILP subproblems
- Solve optimally using **PuLP + CBC**
- Obtain high-quality paths for bottleneck navigation

#### Phase 3: Prioritized Planning for Sparse Regions
- Reserve space-time occupied by MILP solutions
- Apply fast **Space-Time A\*** with priorities
- Solve remaining agents efficiently
- Coordinate at region boundaries

---

### 🧮 Mathematical Formulation

**Regional MILP Subproblem (for congested region \(R\) with agents \(A_R\)):**

\[
\min \sum_{k \in A_R} \sum_{t=1}^{T} t \cdot g_{k,t}
\]

Subject to:
- **Flow conservation:**  
  \(\sum_{v \in R} x_{k,v,t} = a_{k,t}\)
- **Vertex collision:**  
  \(\sum_{k \in A_R} x_{k,v,t} \leq 1\)
- **Movement:**  
  \(x_{k,v,t+1} \leq \sum_{u \in N(v)} x_{k,u,t}\)
- **Goal timing:**  
  \(\sum_t g_{k,t} = 1\)

**Prioritized Planning for Sparse Regions:**
- Use a space-time reservation table \(R_{ST}\)
- Avoid cells occupied by MILP solutions
- Sequential planning with priority ordering

---

## 🛠️ Implementation Architecture

### Class Structure

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Region:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    agents: List[int]  # Agent IDs passing through

class HybridC_Complete:
    def detect_congested_regions(self):
        """Phase 1: Partition & detect congested regions."""
        pass

    def solve_congested_with_milp(self):
        """Phase 2: Solve congested regions with MILP."""
        pass

    def solve_sparse_with_prioritized(self):
        """Phase 3: Solve sparse regions with prioritized planning."""
        pass
