#! /usr/bin/env Rscript

suppressPackageStartupMessages( library(optparse) )
suppressPackageStartupMessages( library(logging) )

## specify our desired options in a list
option_list <- list(
                    make_option(c("-v", "--verbosity"), default="INFO",
                                help="Verbosity of output: DEBUG, INFO, WARN, or ERROR [default %default]"),
                    make_option(c("-p", "--polydegree"), metavar="polynomial degree", type="integer", default=1,
                                help="degree of polynomial to fit to data [default %default]"),
                    make_option("--pi", type="logical", default=TRUE,
                                help="whether to add prediction intervals [default %default]"),
                    make_option("--ci", type="logical", default=TRUE,
                                help="whether to add confidence intervals [default %default]"),
                    make_option("--level", type="double", default=0.95, metavar="confidence level / prediction interval",
                                help="level for confidence intervals and prediction bands [default %default]"),
                    make_option(c("-i", "--inputfile"), type="character",
                                help="name of input datafile"),
                    make_option(c("-f", "--fitfile"), type="character",
                                help="name of output file for regression summary"),
                    make_option(c("-o", "--plotfile"), type="character",
                                help="name of output file for pdf plot.  If not specified, no plot will be made.")
                    )

# get command line options, if help option encountered print help and exit,
# otherwise if options not found on command line then set defaults,
opt <- parse_args(OptionParser(option_list=option_list))

##Logging setup
basicConfig(level=opt$verbosity)

xydat <- read.delim(opt$inputfile, as.is=TRUE)

scatterBands <- function(xydat, degree=1, show.pi=TRUE, show.ci=TRUE, level=0.95, make.plot=TRUE){
    xylabs <- colnames(xydat)
    colnames(xydat) <- c("x", "y")
    fit <- lm(y ~ poly(x, degree), data=xydat)
    adj.rsquared <- summary(fit)$adj.r.squared
    pred.frame <- data.frame(x=seq(min(xydat$x),
                             max(xydat$x), length.out=100))
    pp <- predict(fit, int="p", newdata=pred.frame, level=level)
    pc <- predict(fit, int="c", newdata=pred.frame, level=level)
    if(make.plot){
        plot(y ~ x, data=xydat,
             xlab=xylabs[1],
             ylab=xylabs[2],
             pch=20, col="black",
             ylim=range(xydat, pp, pc))
        matlines(xydat$x, pc, lty=c(1,2,2), col="black")
        matlines(xydat$x, pp, lty=c(1,3,3), col="black")
        ##This dataframe will define the full legend:
        legend.dat <- list(pch=c(20, -1, -1),
                           lty=c(-1, 2, 3),
                           legend=c("data points",
                           paste(level*100, "% confidence interval for degree = ", degree, " fit", sep=""),
                           paste(level*100, "%  prediction interval", sep="")))
        ##keep only parts of the legend being plotted:
        keep.rows <- c(TRUE, show.ci, show.pi)
        legend.dat <- lapply(legend.dat, function(x) x[keep.rows])
        ##Put legend in the topleft:
        legend.dat$x <- "topleft"
        legend.dat$bty <- "n"
        ##and actually create the legend:
        do.call(legend, legend.dat)
        ##See ?plotmath for how to do super/subscripts in a plot
        legend("bottomright", bty = 'n',
               legend = substitute(paste("adjusted ", R^2, " = ", GF), list(GF = round(adj.rsquared, 2))))
    }
    return(fit)
}


if("outputfile" %in% names(opt)){
    loginfo(paste("creating",opt$plotfile, collapse=" "))
    pdf(opt$outputfile, useDingbats=FALSE)
    fit <- scatterBands(xydat=xydat,
                           degree=opt$polydegree,
                           show.pi=opt$pi,
                           show.ci=opt$ci,
                           level=opt$level,
                           make.plot=TRUE)
    dev.off()
}else{
    loginfo("not creating pdf.")
    fit <- scatterBands(xydat=xydat,
                           degree=opt$polydegree,
                           show.pi=opt$pi,
                           show.ci=opt$ci,
                           level=opt$level,
                           make.plot=FALSE)
}

output <- summary(fit)$coefficients
output <- cbind(output, summary(fit)$adj.r.squared)
colnames(output)[ncol(output)] <- "adj.r.squared"

if("fitfile" %in% names(opt)){
    loginfo(paste("creating",opt$fitfile))
    write.table(output, file=opt$fitfile, sep="\t")
}

logdebug(print(output))
