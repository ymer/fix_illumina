#!/usr/bin/env Rscript
library(tidyverse)
library(glue)
 
studies <- read_delim("studies/studies.csv", delim=" ", col_types=cols())

for (study in studies$study){
    print(study)

    flips <- read_table(glue("studies/{study}.flipscan"))
 
    print(table(flips$NEG))
 
    print(flips %>% nrow())
    print("------")
}

