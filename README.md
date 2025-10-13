# Multi-Agent Path Finding (MAPF) Solver

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gurobi](https://img.shields.io/badge/Gurobi-12.0-green.svg)](https://www.gurobi.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Exact and approximate solutions for Multi-Agent Path Finding using MILP, Network Flow, and Hybrid approaches

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Implemented Methods](#implemented-methods)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Results](#results)
- [Repository Structure](#repository-structure)
- [Roadmap](#roadmap)
- [References](#references)

## 🎯 Overview

The **Multi-Agent Path Finding (MAPF)** problem involves coordinating multiple agents navigating a shared environment without collisions while optimizing objectives like makespan or sum-of-costs. This project implements and compares three complementary approaches:

1. **Mixed-Integer Linear Programming (MILP)** - Exact centralized solutions serving as optimal benchmarks
2. **Network Flow Formulation** - Multi-commodity flow on time-expanded graphs for scalability
3. **Hybrid Approaches** - Combining MILP optimality with Network Flow efficiency

### Project Goals

We study MAPF through three complementary solution techniques. First, we implement a **Mixed-Integer Linear Programming (MILP)** formulation providing exact centralized solutions for small instances, serving as the benchmark for evaluating other methods. Second, we develop a **Network Flow formulation** on time-expanded graphs. While approximate, this method scales to larger instances and can be enhanced with linear programming relaxation and rounding techniques.

The central focus is on **hybrid approaches** combining the strengths of both MILP and Network Flow. We implement multiple hybrid strategies including:

- **Hybrid A**: Flow-based LP relaxation generates feasible approximate solutions, subsequently refined with MILP to resolve collisions and enforce integrality
- **Hybrid B**: Flow-generated candidate paths serve as input to MILP column generation
- **Hybrid C**: MILP applied to congested regions while Network Flow solves sparse areas

This comprehensive approach balances efficiency with solution quality, demonstrating how exact and approximate methods complement one another in solving MAPF across varying problem scales.

### Applications
- Warehouse robotics and automated fulfillment
- Autonomous vehicle coordination
- Airport ground traffic management
- Multi-agent game AI

## Features

- **Complete Network Flow MAPF Solver** using Gurobi LP
- **LaCAM2 Baseline** - State-of-the-art anytime search algorithm
- **Automated Visualization** - Timestep-by-timestep GIF animations
- **Collision Detection** - Comprehensive vertex and edge conflict checking
- **Scalability Analysis** - Performance metrics and computational limits
- **Space-Time A*** - Prioritized planning for larger instances
-  **MILP Formulation**
-  **Hybrid A/B/C Methods** 



