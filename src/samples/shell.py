import subprocess

def java_version():
    try:
        # Merge stderr into stdout and treat any non-zero exit as an exception
        result = subprocess.run(
            ["java", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        # The command ran but exited with a non-zero status
        print(f"❌ 'java -version' failed (exit code {e.returncode})")
        print("Output was:")
        print(e.stdout)
    except FileNotFoundError:
        # 'java' binary wasn’t even found on PATH
        print("❌ Could not find 'java'—is it installed and on your PATH?")
    else:
        # Success!
        print("✅ Java version fetched successfully:")
        print(result.stdout)

if __name__ == "__main__":
    java_version()
