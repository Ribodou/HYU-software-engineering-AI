from bottle import run
import bottles_functions



if __name__ == "__main__":
    run(bottles_functions.app, host="0.0.0.0", port=8081, quiet=True)

