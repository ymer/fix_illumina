from gwf import Workflow
import pandas as pd

gwf = Workflow()

studies = pd.read_csv("studies/studies.csv", sep="\s+")
studies_al = list(studies[studies.allelemap != "None"].study)

base = "http://www.well.ox.ac.uk/~wrayner/strand"

flips = []


for i, row in studies.iterrows():
    study = f"studies/{row.study}"

    fixbim = f"{study}_fixed.bim"

    if row.allelemap == "None":
        gwf.target(f"copy_bim_{i}", inputs=[], outputs=[fixbim]) << \
                f"cp {study}.bim {study}_fixed.bim"

    else:

        allele_file = f"{base}/{row.allelemap}.txt.zip"
        allelemap = f"{study}.allelemap.txt"
        gwf.target(f"get_map_{i}", inputs=[], outputs=[f"{allelemap}.zip"]) << \
                f"wget {allele_file} -O {allelemap}.zip"

        gwf.target(f"unzip_{i}", inputs=[f"{allelemap}.zip"], outputs=[allelemap]) << \
                f"""unzip {allelemap}.zip -d studies
                    mv studies/{row.allelemap}.txt {allelemap}"""

        gwf.target(f"update_bim_{i}", inputs=[allelemap], outputs=[fixbim]) << \
                f"Rscript scripts/updatebim.R {study}"

    fixfam = f"{study}_fixed.fam"
    gwf.target(f"fix_fam_{i}", inputs=[], outputs=[fixfam]) << \
            f"Rscript scripts/fixfam.R {study}"

    flip = f"{study}.flipscan"
    flips.append(flip)
    gwf.target(f"flip_scan_{i}", inputs=[fixfam, f"{study}_fixed.bim"], outputs=[flip]) << \
        f"plink --bim {study}_fixed.bim --fam {study}_fixed.fam --bed {study}.bed --flip-scan --out {study}"

    rmsnps = f"{study}.rm.snps"
    gwf.target(f"get_rm_snps_{i}", inputs=[flip], outputs=[rmsnps]) << \
            f"Rscript scripts/get_rm_snps.R {study}"

    gwf.target(f"extract_{i}", inputs=[f"{study}_fixed.bim", rmsnps], outputs=[f"studies2/{row.study}.bed"]) << \
            f"plink --bim {study}_fixed.bim --fam {study}_fixed.fam --bed {study}.bed --exclude {rmsnps} --make-bed --out studies2/{row.study}"


gwf.target("sum_flips", inputs=flips, outputs=[]) << \
        f"Rscript scripts/count_flips.R"


