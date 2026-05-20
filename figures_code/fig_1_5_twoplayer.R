library(dplyr)
library(data.table)
library(ggplot2)
setwd("~/Agent_Based_Modelling/results")
#####################################

# Set the folder path containing the .csv files
folder_path <- "~/Agent_Based_Modelling/results/two_player"

# Get a list of all .csv files in the folder
csv_files <- list.files(path = folder_path, pattern = "\\.csv$", full.names = TRUE)
data <- lapply(csv_files, fread)

# Optionally, combine all data.tables into one (if they have the same structure)
data <- rbindlist(data, use.names = TRUE, fill = TRUE)
prototypes <- unique(data$prototypes)
adaptiveness <- unique(data$adaptiveness)
degrade <- unique(data$degrade)

adaptive <- data %>%
  select(conversations, prototypes,dimensions,
         adaptiveness,degrade,starting_distance,
         first_percev_convg=first_p_convergence_adaptive,
         first_actual_convg=first_a_convergence_adaptive,
         final_distance=final_distance_adaptive)
adaptive$type = "Adaptive"
adaptive$degrade = 0

non_adaptive <- data %>%
  select(conversations, prototypes,dimensions,
         adaptiveness,degrade,starting_distance,
         first_percev_convg=first_p_convergence_nonadaptive,
         first_actual_convg=first_a_convergence_nonadaptive,
         final_distance=final_distance_nonadaptive)
non_adaptive$type = "Non-adaptive"

data <- rbind(adaptive,non_adaptive) %>%
  mutate(adaptiveness = case_when(
    adaptiveness == 1 ~ "Low Adaptability (1%)",
    adaptiveness == 5 ~ "Moderate Adaptability (5%)",
    adaptiveness == 10 ~ "High Adaptability (10%)",
    TRUE ~ as.character(adaptiveness)  # Preserve other values if needed
  ))


