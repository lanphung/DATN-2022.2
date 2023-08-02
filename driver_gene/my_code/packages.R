install.packages("caret", dependencies = TRUE)
install.packages("randomForest")
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("GenomicRanges")

BiocManager::install("GenomeInfoDb")

BiocManager::install("GenomicFeatures")

BiocManager::install("TxDb.Hsapiens.UCSC.hg19.knownGene")

BiocManager::install("TxDb.Hsapiens.UCSC.hg38.knownGene")

BiocManager::install("S4Vectors")

BiocManager::install("org.Hs.eg.db")
install.packages("rlang")