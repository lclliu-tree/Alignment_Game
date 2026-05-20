library(dplyr)
library(tidyr)
library(data.table)
library(ggplot2)
setwd("~/Agent_Based_Modelling/results")

network_vs_clique <- master_data %>% 
  subset(copy_player == 2) %>%
  subset(connections < 5) %>%
  subset(cliques == connections) %>%
  select(cliques, network_distance, average_clique_distance) %>%
  rename(`Average Clique Distance` = average_clique_distance) %>%
  rename(`Network Distance` = network_distance )   
network_vs_clique <- network_vs_clique %>%
  pivot_longer(
    cols = c(`Network Distance`, `Average Clique Distance`),
    names_to = "Distance",
    values_to = "Value") %>% 
  mutate(cliques = case_when(
    cliques == 2 ~ "Two Cliques",
    cliques == 3 ~ "Three Cliques",
    cliques == 4 ~ "Four Cliques",
    cliques == 5 ~ "Five Cliques",
    TRUE ~ as.character(cliques)  # Preserve other values if needed
  ))

network_vs_clique$cliques <- 
  factor(network_vs_clique$cliques, 
         levels = c("Two Cliques", 
                    "Three Cliques", 
                    "Four Cliques", 
                    "Five Cliques"))

ggplot(network_vs_clique, aes(x = cliques, y = Value, fill = cliques)) +
  geom_violin() +
  labs(
    title = "Final Network and Clique Distances",
    x = "Number of Cliques",
    y = "Final Distance") +
  facet_wrap(~Distance) +
  ylim(0.6, 0.9) +
  theme_minimal() +
  scale_fill_brewer(palette = "Set2") +
  theme(axis.text.x = element_blank(),
    text=element_text(family="LM Roman 10", size=16),
    strip.text = element_text(face = "bold"),
    legend.position = "bottom")
