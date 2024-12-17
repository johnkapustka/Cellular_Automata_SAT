import Cellular_SAT
import sys

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ["-batch", "-single"]:
        print("Usage: python 3SAT-Test.py [ -batch <literals> <max_ratio> <trials> | -single <literals> <clauses> ]")
        return 1
    
    elif sys.argv[1] == "-batch":
        if len(sys.argv) != 5:
            print("Usage: python 3SAT-Test.py [ -batch <literals> <max_ratio> <trials> | -single <literals> <clauses> ]")
            return 1
        
        literals = int(sys.argv[2])
        max_ratio = int(sys.argv[3])
        num_trials = int(sys.argv[4])
        num_literals_range = [x for x in range(3, literals + 1)]  # Different problem sizes
        ratio_range = [x for x in range(1, max_ratio + 1)]  # Clause-to-literal ratios to test

        results = Cellular_SAT.run_batch_tests(num_literals_range, ratio_range, num_trials)
        for result in results:
            print(f"Clause/literal ratio: {result[0]}   Percent Solved: {result[1]:.2%}")
    
    elif sys.argv[1] == "-single":
        if len(sys.argv) != 4:
            print("Usage: python 3SAT-Test.py [ -batch <literals> <max_ratio> <trials> | -single <literals> <clauses> ]")
            return 1
        
        literals = int(sys.argv[2])
        clauses = int(sys.argv[3])
        Cellular_SAT.run_solver(literals, clauses)

    return 0

if __name__ == "__main__":
    main()