library(tesseract)
library(pdftools)
library(stringr)
library(qdapRegex)


right = function(text, num_char) {
  substr(text, nchar(text) - (num_char-1), nchar(text))
}

path <- "C:/Users/Enrique/Documents/MarketOCR"

setwd(path)

convertpdf <- list.files(pattern = "\\.pdf$")

for (i in 1:length(convertpdf)) {
  unlist(pdftools::pdf_convert(pdf = convertpdf[i], format = 'tiff', pages = 1, dpi = 400))
}

tifffile <- list.files(pattern = "\\.tiff")

cardenas <- tesseract::ocr(tifffile[1])

#split on \n to create list
pricelist <- stringr::str_split(cardenas, "\n")

#extract right 9 digits
for (i in 1:length(pricelist[[1]])) {
  pricelist[[1]][i] <- right(pricelist[[1]][i], num_char=9)
  pricelist[[1]][i] <- grep(pattern = "\\$[0-9].[0-9][0-9]", pricelist[[1]][i], value=TRUE)
}

grep(pattern = "\\$[0-9].[0-9][0-9]", pricelist[[1]][12], value=TRUE)
