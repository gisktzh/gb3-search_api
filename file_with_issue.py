def function_with_issue(param: list = []): # <- this should at least trigger unused param; and better yet, add a warning about assigning mutable default params
    print("bla")