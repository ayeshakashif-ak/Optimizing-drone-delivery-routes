import random
import graph2 as gp
import streamlit as st
import gen_alg2 as ga
import numpy as np

# Predefined graph dimensions
GRAPH_WIDTH = 400
GRAPH_HEIGHT = 400

# Main function
def main():
    # Create UI sidebar
    sidebar = st.sidebar

    # Create tabs in sidebar
    tab1, tab2 = sidebar.tabs(['Graph', 'Genetic Algorithm'])

    # Initialize Genetic Algorithm variables
    ga_paths = None

    # Sidebar header
    with sidebar:

        # Graph tab
        with tab1:
            # Tab header
            st.header('Create Graph')

            num_nodes = st.slider(label='Number of Nodes', min_value=5, max_value=60, value=27)

            # Anytime button is pushed entire script runs again creating a new graph
            # with the same values but different configuration
            create_graph_button = st.button(label='Reset Graph')

    # Check if the create graph button was pressed or if the graph is not in the session state
    if create_graph_button or 'graph' not in st.session_state or 'num_nodes' not in st.session_state or st.session_state.num_nodes != num_nodes:

        # Create graph with predefined dimensions
        graph = gp.Graph(GRAPH_WIDTH, GRAPH_HEIGHT, num_nodes)

        # Save the graph and slider values in the session state
        st.session_state.graph = graph
        st.session_state.num_nodes = num_nodes

    # Check if the genetic algorithm goals have changed
    goals_change = 'goals' not in st.session_state  # or st.session_state.goals != goals

    # If the genetic algorithm goals have changed, update the goals in the session state
    if goals_change:
        st.session_state.goals = []

    # Genetic Algorithm tab
    with tab2:
        # Tab header
        st.header('Genetic Algorithm')

        # Number of drones slider
        num_drones = st.slider(label='Number of Drones', min_value=1, max_value=10, value=1)
        # Mutation rate set to 0.2%
        mutation_rate = 0.002

        # Tell user source node
        st.text_input(
            "Source:",
            disabled=True,
            placeholder='Hub',
        )

        # Generate goals button
        generate_goals_button = st.button('Randomly Select Destination Nodes')

        # randomly select 10 nodes as goals
        if generate_goals_button:
            random_goals = np.random.choice([key for key in st.session_state.graph.nodes if not key == 'Hub'], 10,
                                            replace=False)
            random_goals = list(random_goals)
            st.session_state.goals = list(random_goals)
            for key in st.session_state.goals:
                st.session_state.graph.nodes[key].delivery_urgency = random.randint(1, 5)

        # Display goals on streamlit
        st.write(f'*Goals:* {st.session_state.goals}')

        # Perform Genetic Algorithm button
        gen_alg_button = st.button('Perform Genetic Algorithm')

        # If the Genetic Algorithm button is pressed and the graph and goals are in the session state
        if gen_alg_button:

            html_animation = st.session_state.graph.plot_graph(goals=st.session_state.goals, drones=ga_paths,animate=True)
            st.markdown(html_animation, unsafe_allow_html=True)
            # Create drones object
            drones = ga.Drones('Drones', st.session_state.graph, st.session_state.graph.nodes['Hub'],
                               [st.session_state.graph.nodes[goal] for goal in st.session_state.goals],
                               num_drones, mutation_rate)
            # Perform Genetic Algorithm
            ga_paths, cost = drones.genetic_alg()
            # Display drone paths on streamlit
            for drone in ga_paths:
                st.write(f'**Drone {drone.name} '
                         f'Path:** {[node.name for node in drone.locations]} '
                         f'*Cost:* {drone.cost}')

            # Display total cost on streamlit
            st.write(f'*Total Cost:* {cost}')

    # Graph Visualization: only Genetic Algorithm
    if generate_goals_button or gen_alg_button:
        # Generate plot from graph
        plot = st.session_state.graph.plot_graph(st.session_state.goals, ga_paths)
        # Display plot on streamlit
        st.pyplot(plot)

    # If neither Genetic Algorithm button is pressed, generate plot from graph
    else:
        # Generate plot from graph
        plot = st.session_state.graph.plot_graph(st.session_state.goals, None, True)

        # Display plot on streamlit
        st.pyplot(plot)
# Run main function
if __name__ == '__main__':
    main()
