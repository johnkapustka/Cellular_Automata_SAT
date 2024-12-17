import itertools
import random

def cellular_automata_solver(clauses, num_literals):
    """Solves a SAT problem using a cellular automaton-like approach."""
    # Initialize cellular automata grid
    grid = [[None for _ in range(len(clauses))] for _ in range(num_literals)]

    for assignment in itertools.product([False, True], repeat=num_literals):
        for clause_id, clause in enumerate(clauses):
            for lit_id in range(num_literals):
                var_name = f"x{lit_id + 1}"
                # Determine if the current literal satisfies this clause under the given assignment
                literal_satisfies = ((assignment[lit_id] and (var_name in clause)) or
                                     (not assignment[lit_id] and (f"~{var_name}" in clause)))

                if lit_id == 0:
                    grid[lit_id][clause_id] = literal_satisfies
                else:
                    grid[lit_id][clause_id] = grid[lit_id - 1][clause_id] or literal_satisfies

                # Early termination if the last literal fails any clause
                if lit_id == num_literals - 1 and not grid[lit_id][clause_id]:
                    break

            if not grid[-1][clause_id]:
                break

        # If all clauses are satisfied, return the solution
        if all(grid[-1]):
            solution = {f"x{i + 1}": val for i, val in enumerate(assignment)}
            return True, solution

    # Return False if no solution is found
    return False, {}

def verify_solution(clauses, solution):
    """Verifies whether the given solution satisfies all the clauses."""
    for clause in clauses:
        satisfied = any(
            (lit.startswith("~") and not solution[lit[1:]]) or
            (not lit.startswith("~") and solution[lit])
            for lit in clause
        )
        if not satisfied:
            return False
    return True

def generate_3sat_problem(num_literals, num_clauses):
    """Generates a random 3SAT problem."""
    literals = [f"x{i + 1}" for i in range(num_literals)]
    problem = []
    for _ in range(num_clauses):
        clause = random.sample(literals, 3)
        clause = [lit if random.choice([True, False]) else f"~{lit}" for lit in clause]
        problem.append(clause)
    return problem

def print_clauses(clauses):
    """Prints the clauses in a human-readable format."""
    print("Generated 3SAT Problem:")
    for idx, clause in enumerate(clauses, 1):
        print(f"Clause {idx}: {' OR '.join(clause)}")

def run_solver(num_literals, num_clauses):
    """Runs the solver for the given number of literals and clauses."""
    clauses = generate_3sat_problem(num_literals, num_clauses)
    print_clauses(clauses)

    # Solve the problem
    is_satisfiable, solution = cellular_automata_solver(clauses, num_literals)

    if is_satisfiable:
        print("\nThe problem is satisfiable!")
        print("Satisfying assignment:")
        for literal, value in solution.items():
            print(f"  {literal} = {'True' if value else 'False'}")

        # Verify the solution
        is_valid = verify_solution(clauses, solution)
        print("\nThe solution is verified to be correct!" if is_valid else "\nThe solution is incorrect!")
    else:
        print("\nThe problem is not satisfiable.")

def run_batch_tests(num_literals_range, ratio_range, num_trials):
    """Runs a batch of tests for different clause-to-literal ratios and collects results."""
    results = []
    for ratio in ratio_range:
        total_satisfied = 0
        for num_literals in num_literals_range:
            num_clauses = int(num_literals * ratio)
            satisfiable_count = 0

            for _ in range(num_trials):
                clauses = generate_3sat_problem(num_literals, num_clauses)
                is_satisfiable, _ = cellular_automata_solver(clauses, num_literals)
                if is_satisfiable:
                    satisfiable_count += 1
            
            total_satisfied += satisfiable_count

            # Record results as (num_literals, ratio, satisfiable_percentage)
        results.append((ratio, total_satisfied / (num_trials * len(num_literals_range))))
    return results