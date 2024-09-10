try:
    # código que pode gerar exceções
    pass
except* (ValueError, TypeError) as e:
    print("Caught an exception group:", e)
except (RuntimeError, OSError) as e:
    print("Caught another exception group:", e)
except* Exception as e:
    print("Caught a general exception group:", e)
