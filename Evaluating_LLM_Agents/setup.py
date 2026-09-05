"""Writes the LLM credentials, agent prompt, and simulation config files that
IntellAgent expects to find under the cloned repo's config/ and examples/ directories."""

import os

import yaml

import config


def write_llm_credentials() -> None:
    # OPENAI_API_KEY is optional: the current SIMULATION_CONFIG runs entirely on a
    # local Ollama model, which needs no credentials here. The openai/azure blocks
    # are still written (with blank values if unset) since simulator/utils/llm_utils.py
    # indexes them unconditionally for OpenAI runs, e.g. LLM_ENV['openai']['OPENAI_ORGANIZATION'].
    os.makedirs("config", exist_ok=True)
    llm_config = {
        "openai": {
            "OPENAI_API_KEY": config.OPENAI_API_KEY or "",
            "OPENAI_API_BASE": "",
            "OPENAI_ORGANIZATION": "",
        }
    }
    with open(config.LLM_ENV_PATH, "w") as f:
        yaml.dump(llm_config, f)

    print("LLM API credentials configured successfully.")
    print("Note: you can add multiple providers to this configuration file.")


def write_agent_prompt() -> None:
    os.makedirs(config.AGENT_INPUT_DIR, exist_ok=True)
    with open(config.AGENT_PROMPT_PATH, "w") as f:
        f.write(config.EDUCATION_PROMPT)

    print("Educational agent prompt created successfully.")
    print("Agent will be tested on policies like 'no direct problem solving' and 'age-appropriate language'.")


def write_simulation_config() -> None:
    with open(config.AGENT_CONFIG_PATH, "w") as f:
        yaml.dump(config.SIMULATION_CONFIG, f, default_flow_style=False)

    print("Configuration file created successfully.")
    print(f"Will generate {config.SIMULATION_CONFIG['dataset']['num_samples']} test scenarios.")
