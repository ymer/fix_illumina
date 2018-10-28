library(tidyverse)
library(glue)

args = commandArgs(trailingOnly=T)

study = args[1]

fam <- read_table(glue("{study}.fam"), col_names=c("FID", "IID", "1", "2", "SEX", "AFF")) %>% 
    mutate(AFF = sample(1:2, n(), replace = TRUE),
           SEX = 1)

write_tsv(fam, glue("{study}_fixed.fam"), col_names=F)

