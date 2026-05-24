# Running the project

To run the simulation write on of the following commands:

Example with 100-byte and 1200-byte message

```bash
uv run main.py 100
```

```bash
uv run main.py 1200
```

Expected behaivour: when running the program with 1200-byte message it should preform message segmentation in three segments (500 bytes + 500 bytes + 200 bytes). Each segment conatining DATA has to receive ACK before sending out next package.

# Check if code compiles

```bash
uv run python -m py_compile main.py devices.py protocol.py config.py
```
