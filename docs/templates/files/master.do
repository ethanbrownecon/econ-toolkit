/*==============================================================================
  Project:  My project
  File:     00_master.do
  Purpose:  Run every do-file in order, from raw data to final output
==============================================================================*/

global root "~/projects/my-project"

do "$root/code/01_clean.do"
do "$root/code/02_analysis.do"
do "$root/code/03_figures.do"
