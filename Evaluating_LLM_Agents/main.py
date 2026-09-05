"""
IntellAgent evaluation demo: configure a policy-bound education chatbot,
generate adversarial test scenarios, run the simulation, and open the
results dashboard.

Requires the plurai-ai/intellagent repo cloned as a sibling of this folder
(../intellagent) with its dependencies installed.
"""

import os

import config
from dashboard import launch_dashboard
from setup import write_agent_prompt, write_llm_credentials, write_simulation_config
from simulation import generate_dataset, init_executor, run_simulation


def main():
    os.chdir(config.INTELLAGENT_DIR)

    write_llm_credentials()
    write_agent_prompt()
    write_simulation_config()

    executor = init_executor()
    generate_dataset(executor)
    run_simulation(executor)
    launch_dashboard()


if __name__ == "__main__":
    main()
