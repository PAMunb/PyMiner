
# Bloco separado para tratar exception groups
class Test_exception:
    def function_test():
        try:
            # Simulação de código que pode gerar exception groups
            raise ExceptionGroup("multiple errors", [ValueError(), TypeError()])
        except* (ValueError, TypeError) as e:
            print("Caught an exception group:", e)
        except* Exception as e:
            print("Caught a general exception group:", e)
            
    def function_test_exception(self):
        # Bloco para tratar exceções normais
        try:
            # Simulação de código que pode gerar exceções normais
            raise RuntimeError("A runtime error occurred")
        except (RuntimeError, OSError) as e:
            print("Caught an exception:", e)