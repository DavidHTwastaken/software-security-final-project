# How to Run

## Starting the Server

Just run `docker compose up` in your terminal (make sure you're in the `app` directory).
It should make the server accessible at `http://localhost:5000`

If you want Docker to automatically sync when changes are made (for development),
run `docker compose watch` instead.

It's also possible to use both at the same time, for example with `docker compose watch --no-up & docker compose up` or by running the commands in separate terminals.

## Using the Web App

You'll need to sign in to perform the challenges. To this end, you can create an account or use an existing one (e.g. "john_doe": "password123").

After that, you can set the difficulty and select a bug.
