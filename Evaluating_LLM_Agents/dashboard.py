"""Launches the Streamlit results dashboard for the simulation run."""

import subprocess
import threading
import time

import config


def _run_streamlit() -> None:
    try:
        subprocess.run(["streamlit", "run", config.DASHBOARD_SCRIPT], cwd=".")
    except Exception as e:
        print(f"Error running Streamlit: {e}")


def launch_dashboard() -> None:
    print("Starting IntellAgent Results Dashboard...")
    print("This will launch an interactive visualization of your agent's performance.")
    print("Please wait a moment for the dashboard to load.")

    thread = threading.Thread(target=_run_streamlit, daemon=True)
    thread.start()

    # Give Streamlit a moment to come up before we try to display it.
    time.sleep(5)

    try:
        from IPython.display import IFrame, display

        display(IFrame(src=config.DASHBOARD_URL, width=1000, height=600))
        print("\nDashboard loaded successfully!")
        print("Navigate to the 'Session Visualizer' page to explore conversation traces.")
    except Exception:
        print(f"\nDashboard is running at: {config.DASHBOARD_URL}")
        print("Please open this URL in a new browser tab to view your results.")
        print("Once there, navigate to the 'Session Visualizer' page.")
