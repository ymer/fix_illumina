library(tidyverse)
library(glue)

args <- commandArgs(trailingOnly=T)

study <- args[1]

flips <- read_table(glue("{study}.flipscan")) %>% filter(NEG > 0 | duplicated(.[["SNP"]]))

write_tsv(flips, glue("{study}.rm.snps"), col_names=F)

