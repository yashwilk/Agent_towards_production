"""IntellAgent simulator setup and execution."""

import warnings

import nest_asyncio

import config


def init_executor():
    warnings.filterwarnings(
        "ignore", message="API key must be provided when using hosted LangSmith API"
    )
    nest_asyncio.apply()

    from simulator.simulator_executor import SimulatorExecutor
    from simulator.utils.file_reading import override_config

    sim_config = override_config(config.AGENT_CONFIG_PATH)
    executor = SimulatorExecutor(sim_config, config.RESULTS_DIR)

    print("IntellAgent simulation environment initialized")
    print(f"Results will be saved to: {config.RESULTS_DIR}")
    return executor


def generate_dataset(executor) -> None:
    # Generates the dataset only if it wasn't generated before.
    executor.load_dataset(config.DATASET_NAME)

    print("Finished generating the scenario dataset")
    sample = executor.dataset_handler.records[0].description.event_description
    print(f"Example generated scenario:\n{sample}")


def run_simulation(executor) -> None:
    print("Starting simulation...")
    print("This will generate scenarios, simulate conversations, and analyze results.")
    print("Estimated time: 2-5 minutes for 10 scenarios.")
    print("=" * 50)

    executor.run_simulation(config.EXPERIMENT_NAME)

    print("=" * 50)
    print("Simulation completed successfully!")
    print("Results are ready for analysis.")
