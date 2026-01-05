import warnings

try:
    warnings.warn("Msg", "CategoryString", "StackLevelString")
except Exception as e:
    print(f"Error 1: {type(e).__name__}: {e}")

try:
    warnings.warn("Msg", UserWarning, "StackLevelString")
except Exception as e:
    print(f"Error 2: {type(e).__name__}: {e}")
