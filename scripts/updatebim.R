library(tidyverse)
library(glue)

args = commandArgs(trailingOnly=T)

study = args[1]

read_bim <- function(fn, suf) {
    read_tsv(fn, col_names=c(glue("CHR_{suf}"), "SNP", glue("GPOS_{suf}"), glue("POS_{suf}"), glue("A1_{suf}"), glue("A2_{suf}")))
}

ill <- read_tsv(glue("studies/{study}.allelemap.txt"), col_names=c("SNP", "AB", "TG")) %>% 
    separate(AB, c("A", "B"), " ") %>% 
    separate(TG, c("An", "Bn"), " ")

bim <- read_bim(glue("studies/{study}.bim"), "study")

df <- inner_join(bim, ill, by="SNP") %>% 
    mutate(A1 = ifelse(A1_study == 1, An, Bn)) %>% 
    mutate(A2 = ifelse(A2_study == 1, An, Bn)) %>%
    select(CHR_study, SNP, GPOS_study, POS_study, A1, A2)

write_tsv(df, glue("studies/{study}_fixed.bim"), col_names=F)

