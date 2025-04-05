from concurrent.futures import ProcessPoolExecutor


def executeFunction(func, args: list) -> None:
    """
    This function executes a given function with dynamic arguments using a ProcessPoolExecutor.
    """
    futures = []
    with ProcessPoolExecutor() as executor:
        for arg in args:
            # Submit the function with the argument
            # It takes all the arguments in a list
            futures.append(executor.submit(func, *arg))

    # Wait for all futures to complete
    for future in futures:
        future.result()
