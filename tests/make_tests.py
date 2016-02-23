import unittest
import re
import argparse
import sys
import csv

class Bcolors:
    """Class used to colorize shell output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    def __init__(self, no_color=False):
        """
        Constructor
        @param no_color Disable color for output (default=False)
        """
        self.no_color = no_color

    def get(self, color):
        """
        Get a color string for output
        @param color the color to get
        @return the color string, or empty string if no_color set
        """
        res = ""
        if not self.no_color:
            res = color
        return res

def parse_doc(doc):
    """
        Parse docstring from tests
        @param doc the docstring
        @return dict containing docstring data
    """
    data = {}
    if doc is None:
        return {}
    res = re.findall("@(?P<key>.+?): (?P<val>[^@]+)", doc, re.DOTALL |re.MULTILINE)
    if res is not None:
        for key, val in res:
            val_lines = val.split("\n")
            val = "\n".join([line.strip() for line in val_lines])
            data[key.strip()] = val.strip()
    return data

def execute_tests_csv(tests, tests_to_execute, full_errors, listing):
    """
        Print tests in CSV
        @param tests: tests list
        @param tests_to_execute: filter for tests
        @param listing: if True, tests are not ran
        @param full_errors: if True, errors output are not truncated
        @return dict containing tests count by state
    """
    res = {"ok" : 0, "failed" : 0, "errors" : 0}
    writer = csv.writer(sys.stdout)
    for test in tests:
        _, ts_name, test_name = test.id().rsplit(".", 2)
        if tests_to_execute is None or test_name in tests_to_execute:

            out = []
            out.append(ts_name)
            out.append(test_name)
            doc = parse_doc(test._testMethodDoc)
            if "short" in doc:
                out.append(doc["short"])
            else:
                out.append("")
            if "description" in doc:
                out.append(doc["description"])
            else:
                out.append("")
            if "command" in doc:
                out.append(doc["command"])
            else:
                out.append("")

            if not listing:
                # Run tests
                result = unittest.TestResult()
                test.run(result)

                state = "OK"
                output = None
                if result.errors or result.failures:
                    state = "FAILED"
                    outputs = result.failures
                    if result.errors:
                        state = "ERROR"
                        outputs = result.errors
                        res["errors"] += 1
                    else:
                        res["failed"] += 1
                    output = outputs[0][1].strip()
                    if not full_errors:
                        output = output.rsplit("\n", 1)[-1]
                else:
                    res["ok"] += 1
                out.append(state)
                if output is not None:
                    out.append(output)
            writer.writerow(out)
    return res

def execute_tests_full(tests, tests_to_execute, listing, full_errors, color):
    """
        Print tests with full information
        @param tests: tests list
        @param tests_to_execute: filter for tests
        @param listing: if True, tests are not ran
        @param full_errors: if True, errors output are not truncated
        @param color: instance of Bcolors, to colorize output
        @return dict containing tests count by state
    """
    res = {"ok" : 0, "failed" : 0, "errors" : 0}
    for test in tests:
        _, ts_name, test_name = test.id().rsplit(".", 2)
        if tests_to_execute is None or test_name in tests_to_execute:

            out = []
            out.append("-" * 100)
            out.append("Test set :          %s" % (color.get(Bcolors.YELLOW) + ts_name + color.get(Bcolors.ENDC)))
            out.append("Test :              %s" % (color.get(Bcolors.MAGENTA) + test_name + color.get(Bcolors.ENDC)))
            doc = parse_doc(test._testMethodDoc)
            if "short" in doc:
                out.append("Short description : %s" % doc["short"])
            if "description" in doc:
                out.append("Description :")
                out.append("    %s" % doc["description"].replace("\n", "\n    "))
            if "command" in doc:
                out.append("Command :")
                out.append("    %s" % doc["command"].replace("\n", "\n    "))
            print "\n".join(out)

            if not listing:
                # Run tests
                result = unittest.TestResult()
                test.run(result)

                out = []
                state = "OK"
                output = None
                if result.errors or result.failures:
                    state = "FAILED"
                    outputs = result.failures
                    if result.errors:
                        state = "ERROR"
                        outputs = result.errors
                        res["errors"] += 1
                    else:
                        res["failed"] += 1
                    state = color.get(Bcolors.RED) + color.get(Bcolors.BOLD) + state + color.get(Bcolors.ENDC)
                    output = outputs[0][1].strip()
                    if not full_errors:
                        output = output.rsplit("\n", 1)[-1]
                    output = color.get(Bcolors.BLUE) + output + color.get(Bcolors.ENDC)
                else:
                    res["ok"] += 1
                    state = color.get(Bcolors.GREEN) + color.get(Bcolors.BOLD) + state + color.get(Bcolors.ENDC)
                out.append("Result :            %s" % state)
                if output is not None:
                    out.append("Ouput :             %s" % output)
                out.append("-" * 100)

                print "\n".join(out)
            print ""
    return res

def execute_tests_default(tests, tests_to_execute, listing, full_errors, color):
    """
        Print tests, one per line
        @param tests: tests list
        @param tests_to_execute: filter for tests
        @param listing: if True, tests are not ran
        @param full_errors: if True, errors output are not truncated
        @param color: instance of Bcolors, to colorize output
        @return dict containing tests count by state
    """
    res = {"ok" : 0, "failed" : 0, "errors" : 0}
    testsuite_name = ""
    for test in tests:
        _, ts_name, test_name = test.id().rsplit(".", 2)
        if tests_to_execute is None or test_name in tests_to_execute:
            if testsuite_name == "":
                testsuite_name = ts_name
                print color.get(Bcolors.YELLOW) + testsuite_name + color.get(Bcolors.ENDC)

            doc = parse_doc(test._testMethodDoc)
            if "short" in doc:
                print ("%s : %s" % (test_name, doc["short"])).ljust(100),
            else:
                print test_name.ljust(100),

            if not listing:
                # Run tests
                result = unittest.TestResult()
                test.run(result)

                if result.errors or result.failures:
                    state = "FAILED"
                    outputs = result.failures
                    if result.errors:
                        state = "ERROR"
                        outputs = result.errors
                        res["errors"] += 1
                    else:
                        res["failed"] += 1
                    print "[" + color.get(Bcolors.RED) + color.get(Bcolors.BOLD) + state + color.get(Bcolors.ENDC) + "]"
                    output = outputs[0][1].strip()
                    if not full_errors:
                        output = output.rsplit("\n", 1)[-1]
                    print color.get(Bcolors.BLUE) + "  =>  %s" % output + color.get(Bcolors.ENDC)
                else:
                    res["ok"] += 1
                    print "[" + color.get(Bcolors.GREEN) + color.get(Bcolors.BOLD) + "OK" + color.get(Bcolors.ENDC) + "]"
            else:
                print ""
    print ""
    return res

def execute_tests(tests, tests_to_execute, listing, full_errors, color, out_format="default"):
    """
        Call an execution function according to out_format
        @param tests: tests list
        @param tests_to_execute: filter for tests
        @param listing: if True, tests are not ran
        @param full_errors: if True, errors output are not truncated
        @param color: instance of Bcolors, to colorize output
        @param out_format: output format
        @return dict containing tests count by state
    """
    if out_format == "default":
        res = execute_tests_default(tests, tests_to_execute, listing, full_errors, color)
    elif out_format == "full":
        res = execute_tests_full(tests, tests_to_execute, listing, full_errors, color)
    elif out_format == "csv":
        res = execute_tests_csv(tests, tests_to_execute, listing, full_errors)
    else:
        raise ValueError("Wrong format")
    return res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Launch unit test for Shield")
    parser.add_argument("--no-color", dest="no_color", action="store_true", default=False, help="Do not use colored output")
    parser.add_argument("--tests", dest="tests", metavar="TEST[,...]", default=None, help="Tests to execute (comma separated list)")
    parser.add_argument("--list", dest="listing", action="store_true", default=False, help="List tests without execution")
    parser.add_argument("--format", dest="out_format", metavar="FORMAT_ID", choices=["default", "full", "csv"], default="default", help="Format of the output (default, full or csv)")
    parser.add_argument("--full-errors", dest="full_errors", action="store_true", default=False, help="Does not truncate exception in tests output")
    args = parser.parse_args()

    # Initialize color instance
    color = Bcolors(args.no_color)

    # Parse tests to execute
    tests_to_execute = args.tests
    if tests_to_execute is not None:
        tests_to_execute = tests_to_execute.split(",")


    # Initialize CSV table
    if args.out_format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(("Test Suite", "Test", "Short Description", "Description", "Command", "Result", "Output"))

    results = {"ok" : 0, "failed" : 0, "errors" : 0}
    # Load all tests from the "tests" folder
    testsuite = unittest.defaultTestLoader.discover("./tests")
    for tf in testsuite:
        for ts in tf:
            res = execute_tests(ts._tests, tests_to_execute, args.listing, args.full_errors, color, args.out_format)
            for key, val in res.iteritems():
                results[key] += val

    # Generate final line report
    count = 0
    nb_ok = 0
    final_report = []
    for key, val in results.iteritems():
        final_report.append("%s %s" % (val, key))
        if key == "ok":
            nb_ok = val
        count += val

    #Display last line report only if not listing and not csv
    if not args.listing and args.out_format != "csv":
        print ""
        print ", ".join(final_report)

    # exit 1 if not all OK
    res = 0
    if nb_ok != count:
        res = 1
    exit(res)

