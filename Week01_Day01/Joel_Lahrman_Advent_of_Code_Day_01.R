setwd("C:\\Users\\jlahrman\\OneDrive - LMI\\Documents\\Advent_of_Code\\Week01_Day01")

#path = "C:\\Users\\jlahrman\\OneDrive - LMI\\Documents\\Advent_of_Code\\Week01_Day01\"

day1data = read.csv("day_01_input.csv", header = FALSE, stringsAsFactors = FALSE)
# Now I have to change the data frame to a vector, not sure where i found to do this
day1data = day1data[,]

target_sum = 2020

week_1_answer <- function(inputs,combo_elements){

  # Use combn to create a dataframe of all combinations
  combos = t(combn(inputs,combo_elements,simplify = TRUE))
  
  # add a column that sums the value. Could also use transform method below but this is another way...
  combos = cbind(combos, total = rowSums(combos))
  
  # change array to data frame, makes it easier to work with
  combos <- as.data.frame(combos)
  
  answer = combos[combos$total == target_sum,]
  # remove total column - I don't want it to wind up in the product
  answer = answer[,!(names(answer) %in% c('total'))]
  # now multiply all values in the row
  answer = transform(answer, prod=Reduce(`*`, answer))
  print(combo_elements)
  print(answer)

}

for (j in c(2,3)) {
  week_1_answer(day1data,j)
}
  
#I should fool around with the apply functions a bit, they are handy...
#practice = apply(combn(day1data,2),2,paste)
