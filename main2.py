import random
import graph2 as gp
import streamlit as st
import gen_alg2 as ga
import numpy as np

# Main function
def main():
    # Create UI sidebar
    sidebar = st.sidebar
    # Create a container for the tabs
    tabs_container = st.sidebar.container()

    # Create tabs using st.tabs
    genetic_algorithm_tab, other_tab = tabs_container.tabs(["Genetic Algorithm", "Other Tab"])

    # Initialize Genetic Algorithm variables
    ga_paths = None

    # Sidebar header
    with sidebar:

        # Genetic Algorithm tab content
        with genetic_algorithm_tab:
            # Tab header
            st.header('Genetic Algorithm')

            # Number of drones slider
            num_drones = st.slider(label='Number of Drones', min_value=1, max_value=10, value=1)
            # Mutation rate slider
            mutation_rate = st.slider(label='Mutation Rate %', min_value=0, max_value=100, value=2, step=1)

            # Tell user source node
            st.text_input(
                "Source:",
                disabled=True,
                placeholder='Hub',
            )

            # Generate goals button
            generate_goals_button = st.button('Randomly Select Destination Nodes')

            # Randomly select 10 nodes as goals
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
                # Create drones object
                drones = ga.Drones('Drones', st.session_state.graph, st.session_state.graph.nodes['Hub'],
                                   [st.session_state.graph.nodes[goal] for goal in st.session_state.goals],
                                   num_drones, mutation_rate / 100)
                # Perform Genetic Algorithm
                ga_paths, cost = drones.genetic_alg()
                # Display drone paths on streamlit
                for drone in ga_paths:
                    st.write(f'**Drone {drone.name} '
                             f'Path:** {[node.name for node in drone.locations]} '
                             f'*Cost:* {drone.cost}')

                # Display total cost on streamlit
                st.write(f'*Total Cost:* {cost}')

    # Generate plot from graph with drone paths if Genetic Algorithm is run
    if generate_goals_button or gen_alg_button:
        # Generate plot from graph
        plot = st.session_state.graph.plot_graph(st.session_state.goals, None, None, ga_paths)

        # Display plot on streamlit
        st.pyplot(plot)

    # Otherwise, generate default graph plot
    else:
        # Generate plot from graph
        plot = st.session_state.graph.plot_graph()

        # Display plot on streamlit
        st.pyplot(plot)


# Run main function
if __name__ == '__main__':
    main()