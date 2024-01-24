import os
import sys
import subprocess
import arguments
import logger
import time
import report

def treat_newick(newick):
  return newick.replace("@", "at")

def get_gene_trees_file(pargenes_dir):
  return os.path.join(pargenes_dir, "aster_run", "gene_trees.newick")

def extract_gene_trees_support(pargenes_dir, gene_trees_filename):
  results = os.path.join(pargenes_dir, "supports_run", "results")
  count = 0
  with open(gene_trees_filename, "w") as writer:
    for f in os.listdir(results):
      if (f.endswith(".raxml.support") and not "tbe" in f):
        with open(os.path.join(results, f)) as reader:
          writer.write(treat_newick(reader.read()))
        count += 1
  logger.info("ParGenes/Astral: " + str(count) + " gene trees (with support values) were found in ParGenes output directory")

def extract_gene_trees_ml(pargenes_dir, gene_trees_filename):
  results = os.path.join(pargenes_dir, "mlsearch_run", "results")
  count = 0
  with open(gene_trees_filename, "w") as writer:
    for msa in os.listdir(results):
      tree_file = os.path.join(results, msa, msa + ".raxml.bestTree")
      try:
        with open(tree_file) as reader:
          writer.write(treat_newick(reader.read()))
        count += 1
      except:
        continue
  logger.info("ParGenes/Aster: " + str(count) + " trees were found in ParGenes output directory")

def extract_gene_trees(pargenes_dir, gene_trees_filename):
  """ Get all ParGenes ML gene trees and store then in gene_trees_filename
  """
  with_supports = os.path.isdir(os.path.join(pargenes_dir, "supports_run"))
  results = ""
  if (with_supports):
    extract_gene_trees_support(pargenes_dir, gene_trees_filename)
  else:
    extract_gene_trees_ml(pargenes_dir, gene_trees_filename)

def get_additional_parameters(parameters_file):
  if (parameters_file == None or parameters_file == ""):
    return []
  aster_options = open(parameters_file, "r").readlines()
  if (len(aster_options) != 0):
    return aster_options[0][:-1].split(" ")
  else:
    return []

###################################
#def get_alignments_list(pargenes_dir):
#""" Collect a list of alignments as input to aster (caster*)
#  - pargenes_dir     (str):        pargenes output directory
#"""
#
#  return list_or_file
###################################

def run_aster(pargenes_dir, aster_bin, parameters_file):
  """ Run aster on the ParGenes ML trees or Alignment files
  - pargenes_dir     (str):        pargenes output directory
  - aster_bin        (str):        name of binary
  - parameters_file  (list(str)):  a file with the list of additional arguments to pass to astral
  """
  aster_args = get_additional_parameters(parameters_file)
  aster_run_dir = os.path.join(pargenes_dir, "aster_run")
  aster_output = os.path.join(astral_run_dir, "output_species_tree.newick")
  aster_logs = os.path.join(astral_run_dir, "aster_logs.txt")
  logger.info("Aster additional parameters:")
  logger.info(aster_args)
  try:
    os.makedirs(aster_run_dir)
  except:
    pass
  #gene_trees = get_gene_trees_file(pargenes_dir)
  #extract_gene_trees(pargenes_dir, gene_trees)
  ###########
  #library_path = os.path.abspath(os.path.join(aster_bin, os.pardir))
  #library_path = os.path.join(library_path, "lib")
  ##astral_jar = os.path.basename(astral_jar)
  #command = ""
  #command += "java "
  #command += "-D\"java.library.path=" + library_path + "\" "
  #command +="-jar "
  #command += astral_jar + " "
  #command += "-i " + gene_trees + " "
  #command += "-o " + astral_output + " "
  ###########
  #astral -t 4 -i gene_trees.newick -o astral.output_species_tree.newick
  command = aster_bin + " "
  # Need to check if we are using trees or alignments as input!
  if aster_bin.startswith("astral"):
    gene_trees = get_gene_trees_file(pargenes_dir)
    extract_gene_trees(pargenes_dir, gene_trees)
    command += "-i " + gene_trees + " "
  elif aster_bin.startswith("caster"):
    ##################### Need the list of alignments
    #command += "-i " + alignment_list + " " #######
  command += "-o " + aster_output + " "
  ###########
  for arg in aster_args:
    command += arg + " "
  sys.stderr.write(command)
  command = command[:-1]
  split_command = command.split(" ")
  out = open(aster_logs, "w")
  logger.info("Starting aster... Logs will be redirected to " + aster_logs)
  p = subprocess.Popen(split_command, stdout=out, stderr=out)
  p.wait()
  if (0 != p.returncode):
    logger.error("Aster execution failed")
    report.report_and_exit(pargenes_dir, 1)

def run_aster_pargenes(aster_bin, op):
  run_aster(op.output_dir, aster_bin, op.aster_global_parameters)

if (__name__ == '__main__'):
  if (len(sys.argv) != 2 and len(sys.argv) != 3):
    print("Error: syntax is:")
    print("<aster_binary> pargenes_dir [aster_parameters_file]")
    print("aster_parameters_file is optional and should contain additional parameters to pass to aster call)")
    exit(1)
  pargenes_dir = sys.argv[1]
  parameters_file = None
  if (len(sys.argv) > 2):
    parameters_file = sys.argv[2]
  start = time.time()
  logger.init_logger(pargenes_dir)
  logger.timed_log(start, "Starting aster pargenes script...")
  scriptdir = os.path.dirname(os.path.realpath(__file__))
  #########################
  #aster_bin = os.path.join(scriptdir, "..", "pargenes_binaries", aster_xxxxxxxxxx)
  #aster_bin = os.path.join(scriptdir, "..", "pargenes_binaries", "astral.jar")
  #########################
  run_aster(pargenes_dir, aster_bin, parameters_file)
  logger.timed_log(start, "End of aster pargenes script...")

