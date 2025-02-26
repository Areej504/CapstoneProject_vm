import os
import subprocess


def build_and_run_test_driver():
    """Build CMake to install cadmium dependencies and run test driver"""

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    build_dir = os.path.join(root_dir, "model", "vending_machine", "build")

    # Ensure build directory exists
    os.makedirs(build_dir, exist_ok=True)

    try:
        # Run `cmake ..`
        subprocess.run(["cmake", ".."], check=True, cwd=build_dir)

        # Run `cmake --build . -t td_Vending_Machine`
        subprocess.run(
            ["cmake", "--build", ".", "-t", "td_Vending_Machine"],
            check=True,
            cwd=build_dir
        )

        # Set the correct executable path based on OS
        executable_path = os.path.join(build_dir, "test", "td_Vending_Machine")
        if os.name == "nt":  # Windows
            executable_path += ".exe"

        # Ensure executable exists
        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"Executable not found: {executable_path}")

        # Run the test driver executable
        result = subprocess.run([executable_path], check=True, capture_output=True, text=True)
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing: {e.cmd}")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(f"Output:\n{e.stdout}")
        if e.stderr:
            print(f"Error:\n{e.stderr}")


if __name__ == '__main__':
    build_and_run_test_driver()
