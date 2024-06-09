import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def create_network(num_nodes: int, connection_prob: float) -> nx.Graph:
    """Create a random Erdos-Renyi graph."""
    G = nx.erdos_renyi_graph(num_nodes, connection_prob)
    return G

def initialize_states(G: nx.Graph) -> None:
    """Initialize the strategy of each node."""
    for node in G.nodes():
        G.nodes[node]['strategy'] = np.random.choice(['C', 'D'])

def calculate_payoff(G: nx.Graph, T: float, S: float) -> None:
    """Calculate the payoff of each node."""
    for node in G.nodes():
        strategy = G.nodes[node]['strategy']
        payoff = 0
        for neighbor in G.neighbors(node):
            neighbor_strategy = G.nodes[neighbor]['strategy']
            if strategy == 'C' and neighbor_strategy == 'C':
                payoff += 1
            elif strategy == 'C' and neighbor_strategy == 'D':
                payoff += S
            elif strategy == 'D' and neighbor_strategy == 'C':
                payoff += T
        G.nodes[node]['payoff'] = payoff

def update_strategies(G: nx.Graph) -> None:
    """Update the strategy of each node."""
    for node in G.nodes():
        current_payoff = G.nodes[node]['payoff']
        neighbor = np.random.choice(list(G.neighbors(node)))
        neighbor_payoff = G.nodes[neighbor]['payoff']
        if neighbor_payoff > current_payoff:
            G.nodes[node]['strategy'] = G.nodes[neighbor]['strategy']

def run_simulation(G: nx.Graph, T: float, S: float, num_steps: int) -> list:
    """Run the simulation."""
    initialize_states(G)
    proportions = []
    for _ in range(num_steps):
        calculate_payoff(G, T, S)
        update_strategies(G)
        proportions.append(np.mean([1 if G.nodes[node]['strategy'] == 'C' else 0 for node in G.nodes()]))
    return proportions

def plot_network(G: nx.Graph):
    """Plot the network."""	
    color_map = []
    for node in G.nodes():
        if G.nodes[node]['strategy'] == 'C':
            color_map.append('blue')
        else:
            color_map.append('red')
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.show()

def plot_proportions(proportions: list[float], T: float, S: float) -> None:
    """Plot the evolution of cooperation."""
    plt.figure()
    plt.plot(proportions, label=f'T={T}, S={S}')
    plt.xlabel('Time Step')
    plt.ylabel('Proportion of Cooperators')
    plt.title(f'Evolution of Cooperation (T={T}, S={S})')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    num_nodes = 100
    connection_prob = 0.1
    T_values = np.linspace(1, 2, 10)
    S_values = 2 - T_values
    num_steps = 100

    G = create_network(num_nodes, connection_prob)
    for T, S in zip(T_values, S_values):
        print(f"Running simulation for T={T}, S={S}")
        proportions = run_simulation(G, T, S, num_steps)
        plot_proportions(proportions, T, S)
        plot_network(G)
