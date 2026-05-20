library(dplyr)
library(data.table)
library(ggplot2)
setwd("~/Agent_Based_Modelling/results")

complex_data <- fread("final-1-complexnetwork.csv")
complex_data$average_clique_distance =
  rowMeans(complex_data[, c("clique_1_distance", 
                            "clique_2_distance", 
                            "clique_3_distance",
                            "clique_4_distance",
                            "clique_5_distance")])
complex_data <- complex_data %>%
  select(-c(clique_1_distance,
            clique_2_distance,
            clique_3_distance,
            clique_4_distance,
            clique_5_distance))
complex_data$network_type = "complex_network"

simple_data2 <- fread("final-1-lowconnectednetwork_cliques_2.csv")
simple_data2$average_clique_distance = 
  rowMeans(simple_data2[, c("clique_1_distance", "clique_2_distance")])
simple_data2 <- simple_data2 %>% 
  select(-c(clique_1_distance,
            clique_2_distance))

simple_data3 <- fread("final-1-lowconnectednetwork_cliques_3.csv")
simple_data3$average_clique_distance = 
  rowMeans(simple_data3[, c("clique_1_distance", 
                            "clique_2_distance", 
                            "clique_3_distance")])
simple_data3 <- simple_data3 %>%
  select(-c(clique_1_distance,
            clique_2_distance,
            clique_3_distance))

simple_data4 <- fread("final-1-lowconnectednetwork_cliques_4.csv")
simple_data4$average_clique_distance =
  rowMeans(simple_data4[, c("clique_1_distance", 
                            "clique_2_distance", 
                            "clique_3_distance",
                            "clique_4_distance")])

simple_data4 <- simple_data4 %>%
  select(-c(clique_1_distance,
            clique_2_distance,
            clique_3_distance,
            clique_4_distance))

simple_data <- 
  rbind(simple_data2,
        rbind(simple_data3,
              simple_data4))
rm(simple_data2,simple_data3,simple_data4)
simple_data$copy_player = 2
simple_data$network_type = "simple_network"
master_data <- rbind(complex_data,simple_data)
fwrite(master_data,"master_data_networks.csv")
