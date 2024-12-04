import os
import subprocess
import sys
import shutil


def remove_pip_packages(python_executable, exclude_packages):
    """Remove all pip-installed packages except exclusions."""
    print(f"Checking for pip-installed packages using Python at {python_executable}...")
    try:
        packages = list_installed_packages(python_executable)
        if not packages:
            print("No pip-installed packages found.")
            return

        print(f"Found {len(packages)} pip-installed packages. Removing...")
        for package in packages:
            package_name = package.split("==")[0]  # Handle package version strings
            if package_name in exclude_packages:
                print(f"Skipping excluded package: {package_name}")
                continue

            print(f"Removing {package_name}...")
            # Build the command correctly
            command = python_executable[:]
            command += ["-m", "pip", "uninstall", "-y", package_name]
            subprocess.run(command, check=False)
            command = python_executable[:]
            
        print("All eligible pip-installed packages have been removed.")
    except Exception as e:
        print(f"Error removing pip packages: {e}")
 
def list_installed_packages(python_executable):
    """List installed pip packages."""
    try:
        # Build the command correctly
        command = python_executable[:] 
        command += ["-m", "pip", "freeze"]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().splitlines()
    except Exception as e:
        print(f"Error listing pip packages: {e}")
        return []

def remove_poetry_packages(python_executable, remove_files):
    """Remove all packages installed via poetry and optionally delete configuration files."""
    print(
        f"Checking for poetry-installed packages using Python at {python_executable}...")
    try:
        # Check if poetry is installed
        poetry_installed = subprocess.run(
            ["poetry", "--version"], capture_output=True, text=True, check=False).returncode == 0
        if not poetry_installed:
            print("Poetry is not installed on this system.")
            return

        # Get poetry project root
        poetry_root_result = subprocess.run(
            ["poetry", "env", "info", "--path"], capture_output=True, text=True, check=False)
        if poetry_root_result.returncode != 0:
            print("No poetry virtual environment detected.")
            return

        print("Removing poetry virtual environment...")
        subprocess.run(["poetry", "env", "remove", "--all"], check=False)
        print("All poetry-installed packages have been removed.")

        if remove_files:
            print(
                "WARNING: Removing `pyproject.toml` and `poetry.lock` files cannot be undone.")
            confirm = input(
                "Are you sure you want to delete these files? (yes/no): ").strip().lower()
            if confirm == "yes":
                if os.path.exists("pyproject.toml"):
                    os.remove("pyproject.toml")
                    print("Deleted `pyproject.toml`.")
                if os.path.exists("poetry.lock"):
                    os.remove("poetry.lock")
                    print("Deleted `poetry.lock`.")
            else:
                print("Skipping file deletion.")
    except Exception as e:
        print(f"Error removing poetry packages: {e}")


def resolve_python_executable(python_version):
    """
    Resolve the Python executable for the given version.
    - If python3.x is available, use it.
    - On Windows, fall back to py -x.x if python3.x is not recognized.
    """
    if not python_version:
        print("No Python version entered. Using the default 'python' command.")
        python_executable = "python"
    else:
        python_executable = f"python{python_version}"

    # Test if the command works
    try:
        subprocess.run([python_executable, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Using Python executable: {python_executable}")
        return python_executable
    except FileNotFoundError:
        # On Windows, fall back to `py -x.x`
        if os.name == "nt":
            py_command = ["py", f"-{python_version}"]
            try:
                subprocess.run(py_command + ["--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"# Falling back to Python Launcher: {' '.join(py_command)}")
                return py_command
            except FileNotFoundError:
                print(f"# Python version {python_version} not found via `python{python_version}` or `py -{python_version}`.")
                raise
        else:
            print(f"Python version {python_version} not found.")
            raise

    return python_executable

def main():
    print("Welcome to the package cleanup tool!")
    print("Choose the package manager to clean up:")
    print("1. pip")
    print("2. poetry")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        # Step 1: Ask the user to select Python version for pip
        python_version = input(
            "Enter the Python version to use (e.g., '3.10', '3.11'): ").strip()
        try:
            # Resolve the Python executable (string or list)
            python_executable = resolve_python_executable(python_version)
            print(f"# Resolved Python executable: {python_executable}")
        except Exception as e:
            print(f"Error resolving Python executable: {e}")
            return


        # Check if the selected Python version is valid
        try:
            if isinstance(python_executable, list):  # Handle `py` fallback as a list of arguments
                result = subprocess.run(python_executable + ["--version"], capture_output=True, text=True, check=True)
            else:
                result = subprocess.run([python_executable, "--version"], capture_output=True, text=True, check=True)
            print(f"# Python version: {result.stdout.strip()}")
        except Exception as e:
            print(f"# Failed to run Python: {e}")

        # Step 2: Ask the user for packages to exclude
        exclude_packages_input = input(
            "Enter package names to exclude (comma-separated), or leave blank for none: ").strip()
        exclude_packages = set(exclude_packages_input.split(
            ",")) if exclude_packages_input else set()

        # Step 3: Remove pip packages
        remove_pip_packages(python_executable, exclude_packages)

    elif choice == "2":
        # Ask the user if they want to delete poetry files
        remove_files = input(
            "Do you want to delete `pyproject.toml` and `poetry.lock` files? (yes/no): ").strip().lower() == "yes"
        # Step 1: Ask the user to select Python version for poetry
        python_version = input(
            "Enter the Python version to use for poetry (e.g., '3.10', '3.11'): ").strip()
        python_executable = f"python{python_version}"

        # Check if the selected Python version is valid
        try:
            subprocess.run([python_executable, "--version"], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            print(
                f"Python version {python_version} not found. Please ensure it's installed and accessible in PATH.")
            return

        # Step 3: Remove poetry packages
        remove_poetry_packages(python_executable, remove_files)

    else:
        print("Invalid choice. Exiting.")

    print("Cleanup process complete.")


if __name__ == "__main__":
    main()
