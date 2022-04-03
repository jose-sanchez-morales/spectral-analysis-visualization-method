from pipeline.code.pipeline_manager import run_option
import argparse
import logging

# This is the entry point to the pipeline manager

# Set up the argument parser
parser = argparse.ArgumentParser()

# Only 1 specific argument allows to run the pipeline at the moment
parser.add_argument("option", type=str, choices={"run_code"},
                    help="type the specified option to run the pipeline.")

# Future arguments should have this form
parser.add_argument("--argument",
                    type=int,
                    help="Argument X to be passed into the Y module "
                         "must have the format '--argument $int'")

args = parser.parse_args()

if args.option == "run_code":
    run_option(args.option)
else:
    logging.error(" 'run_code' missing, and is required for " + args.option)
