library(tesseract)
library(pdftools)

path <- "/home/pi/Downloads/MarketPdf"

setwd(path)

convertpdf <- list.files(pattern = "\\.pdf$")

for (i in 1:length(convertpdf)) {
  unlist(pdftools::pdf_convert(pdf = convertpdf[i], format = 'tiff', pages = 1, dpi = 600))
}

tifffile <- list.files(pattern = "\\.tiff")

cardenas <- tesseract::ocr(tifffile[1])

cardenas <- iconv(cardenas, "UTF-8", "ASCII", sub = "")

#copy and paste s2 to output.txt in flash drive E:/HPSCANS folder if done on lenovo

fileConn<-file("output.txt")
writeLines(cardenas, fileConn)
close(fileConn)
