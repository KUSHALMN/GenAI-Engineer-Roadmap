# Day 07 Notes: Workflow Graphs and Conditional Edges

## 1. Graph Primitives
- **Nodes:** Pure functions that take State and return an updated partial State.
- **Edges:** Unconditional transitions between nodes.
- **Conditional Edges:** Dynamic routers that evaluate current State variables and return the next Node name or `__END__`.
