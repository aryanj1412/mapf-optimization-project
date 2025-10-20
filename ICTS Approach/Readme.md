# ICTS Baseline Implementation

This directory contains the implementation and results of ICTS (Increasing Cost Tree Search) — a classical optimal search-based algorithm for Multi-Agent Path Finding (MAPF).
It serves as the foundational optimal baseline for evaluating other MAPF algorithms such as CBS, LaCAM, and PIBT-based methods.

## Research Background
ICTS Algorithm (AAAI 2012)

Paper: Increasing Cost Tree Search for Optimal Multi-Agent Pathfinding
Authors: Guni Sharon, Roni Stern, Ariel Felner, Nathan R. Sturtevant
Conference: AAAI-12 (Association for the Advancement of Artificial Intelligence)
ArXiv / DOI: AAAI-12 Proceedings

## Algorithm Overview

ICTS (Increasing Cost Tree Search) is a two-level optimal MAPF algorithm designed to compute collision-free, minimum-cost paths for multiple agents.
It systematically explores combinations of per-agent path costs and checks whether a joint feasible plan exists for that cost configuration.

## Core Concept

ICTS separates the problem into two layers:

High-Level Search (Increasing Cost Tree – ICT):
Explores combinations of individual agent path costs in non-decreasing total cost order.

Low-Level Search (Feasibility Checking):
For each cost tuple, checks if a set of non-colliding paths exists by enumerating all paths for each agent with that exact cost.

The first feasible combination found corresponds to the optimal joint solution.

## Key Innovations
1️⃣ Two-Level Search Decomposition:

Reduces complexity by decoupling cost generation from path feasibility.

Each agent is planned independently in the low-level search.

2️⃣ Lazy Cost Expansion:

Expands only one agent’s cost by +1 at each tree level.

Avoids exhaustive enumeration of the exponential joint space.

3️⃣ Collision-Free Path Combination:

Uses incremental backtracking to combine per-agent paths.

Checks both vertex and edge conflicts.

## Performance Characteristics
✅ Strengths

Optimality: Always returns the minimal-sum-of-costs solution.

Completeness: Guaranteed to find a solution if one exists.

Structured Search: Cost tuples explored in increasing order ensure systematic coverage.

Modularity: Works with any per-agent shortest path planner (e.g., A*, Dijkstra).

## Limitations

High memory usage for large grids or many agents.

Low-level path enumeration can grow exponentially.
