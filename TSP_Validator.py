from ast import literal_eval
import multiprocessing
import subprocess
import time
# Function to evaluate code against test cases


def evaluate_code(code, input_file):

    with open(input_file, "r") as input_data:
        lines = input_data.readlines()
        i = 0
        input_lines = []

        while i < len(lines):
            # Read multi-line input until an empty line is encountered

            input_lines.append(lines[i])
            i += 1

        process = subprocess.Popen(
            ["python", code],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            print("Going For Evaluation.")
            actual_output, std_err = process.communicate(
                input="".join(input_lines), timeout=300)
        except subprocess.TimeoutExpired:
            print("Terminating Process Due Timeout.")
            process.terminate()
            actual_output, std_err = process.communicate()

    return actual_output, std_err


# Read Python code file name from the terminal input
print("------------WELCOME TO TSP VALIDATOR----------------")
print("Make Sure All the Test Cases , Validator and Your Script are in same Directory.")
code_file = input("Enter the Python code file name (e.g., script.py): ")

# Read input file and output file names from the terminal input
# input_files = input("Enter the input file name (e.g., input.txt): ")
input_files = [ 'reuc_10', 'rnoneuc_10','reuc_25', 'rnoneuc_25', 'reuc_50', 'rnoneuc_50', 'reuc_100', 'rnoneuc_100']


# Evaluate the code against the test cases
for i, input_file in enumerate(input_files):
    print(f'Test case: {i} , test_file: {input_file}')
    try:
        with open(input_file, 'r') as file:

            plines = file.readlines()
            file.close()

            # mat is the pairwise distance matrix
            # n is the number of cities

            n = int(plines[1])
            mat = []
            for i in range(2+n, 2+(2*n)):
                line = plines[i].split()
                row = [float(s) for s in line]
                mat.append(row)

        print(f"Number Of City for Test Case : {n}")

        evaluation_results, std_err = evaluate_code(code_file, input_file)

        if std_err:
            print("There is Some Error in Your Code. Here it is :")
            print(std_err)

        elif evaluation_results:
            print(
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ YOUR RESULT ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
            print(evaluation_results)
            print(
                '--------------------------------------------------------------------------------')
            print(
                " ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ EVALUATION ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")

            last_ = evaluation_results.split('\n')[-1]
            if (last_ == ''):
                last_ = evaluation_results.split('\n')[-2]

            if last_.__contains__(","):
                try:
                    t = type(literal_eval(last_))
                    print(
                        f"Your Path should be space Seprated. NOt a {t}", end=' ')
                except:
                    print("Your Path should be space Seprated.", end=' ')
                finally:
                    print("It should NOt contain Commas.")
                    print(); print(); print(); print(); print() ;print(); print(); print()
                    continue

            print(f'Final Path Considered for Evaluation:- {last_}')

            last_line = last_.split()

            if (len(last_line) == n):
                print("Path has correct no. of cities.")
            else:
                print(" Path has incorrect no. of cities.")
                print(); print(); print(); print(); print() ;print(); print(); print()

                continue

            try:
                last_line_int = [int(x) for x in last_line]
            except:
                print('Your Script Should Print Integetrs, It is not printing integers.')
                continue

            last_line_int_copy = list(last_line_int)
            last_line_int_copy.sort()
            flag = False
            for i in range(len(last_line_int_copy)-1):
                if last_line_int_copy[i] == last_line_int_copy[i+1]:
                    print('city repitition - invalid tour:')
                    print(last_line_int_copy[i])
                    flag = True
                    break
            if flag:
                continue

            print("valid tour - computing the cost")
            cost = 0
            for i in range(len(last_line_int)-1):
                cost += mat[last_line_int[i]][last_line_int[i+1]]
            cost += mat[last_line_int[n-1]][last_line_int[0]]
            print(cost)

        else:
            print(
                "!!!!!!!!!!!!!!!!!!!!!!!! YOUR SCRIPT IS PRINTING NOTHING  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print(); print(); print(); print(); print() ;print(); print(); print()

    except:
        print(f"Test Files {input_file}are not in the directory.")
        print(); print(); print(); print(); print() ;print(); print(); print()