#!/usr/bin/env Rscript --vanilla --verbose

suppressPackageStartupMessages( library(optparse) )

## specify our desired options in a list
option_list <- list(
                    make_option(c("-n", "--number"), metavar="number of datapoints",
                                type="integer", default=100,
                                help="Number of xy datapoints to simulate [default %default]"),
                    make_option("--xmin", default=0, type="double",
                                help="Lower bound of simulated x [default %default]"),
                    make_option("--xmax", default=1, type="double",
                                help="Upper bound of simulated x [default %default]"),
                    make_option("--sd", default=0.1, type="double", metavar="standard deviation",
                                help="standard deviation of normal residuals [default %default]"),
                    make_option(c("-q", "--quadratic"), default=TRUE, type="logical",
                                help="If TRUE, the relationship between y and x will be quadratic (y~x^2), otherwise linear [default %default]"),
                    make_option(c("-o", "--outputfile"), type="character",
                                help="name of output file for simulated data")
                    )

# get command line options, if help option encountered print help and exit,
# otherwise if options not found on command line then set defaults,
opt <- parse_args(OptionParser(option_list=option_list))

##simulate data
simdat <- data.frame(x = seq(opt$xmin, opt$xmax, length.out=opt$number))
exponent <- ifelse(opt$quadratic, 2, 1)
simdat$y <- simdat$x^exponent + rnorm(opt$number, sd=opt$sd)

##write simulated data
write.table(simdat, file=opt$outputfile, sep="\t", row.names=FALSE)
