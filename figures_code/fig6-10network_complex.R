library(dplyr)
library(tidyr)
library(data.table)
library(ggplot2)
setwd("~/Agent_Based_Modelling/results")

network_vs_clique <- master_data %>% 
  subset(network_type == "complex_network") %>%
  select(cliques, copy_player,network_distance, average_clique_distance) %>%
  rename(`Average Clique Distance` = average_clique_distance) %>%
  rename(`Network Distance` = network_distance )
network_vs_clique <- network_vs_clique %>%
  pivot_longer(
    cols = c(`Network Distance`, `Average Clique Distance`),
    names_to = "Distance",
    values_to = "Value") %>% 
  mutate(cliques = case_when(
    cliques == 5 ~ "Five Cliques",
    TRUE ~ as.character(cliques)  # Preserve other values if needed
  )) %>% 
  mutate(copy_player = case_when(
    copy_player == 5 ~ "Five Players",
    copy_player == 4 ~ "Four Players",
    copy_player == 3 ~ "Three Players",
    copy_player == 2 ~ "Two Players",
    TRUE ~ as.character(copy_player)  # Preserve other values if needed
  )) %>%
  rename(Cliques = cliques) %>%
  rename(`Connection Size` = copy_player)

network_vs_clique$`Connection Size` <- 
  factor(network_vs_clique$`Connection Size`, 
         levels = c("Two Players", 
                    "Three Players",
                    "Four Players",
                    "Five Players"))

ggplot(network_vs_clique, aes(x = `Connection Size`, 
                              y = Value, 
                              fill = `Connection Size`)) +
  geom_violin() +
  labs(
    title = "Final Network and Clique Distances",
    x = "Connection Size",
    y = "Final Distance") +
  facet_wrap(~Distance) +
  ylim(0.6, 0.9) +
  theme_minimal() +
  scale_fill_brewer(palette = "Set2") +
  theme(axis.text.x = element_blank(),
        text=element_text(family="LM Roman 10", size=16),
        strip.text = element_text(face = "bold"),
        legend.position = "bottom")

network_connect_Num_and_size <- master_data %>% 
  subset(network_type == "complex_network") %>%
  select(connections, copy_player, network_distance, average_clique_distance) %>%
  rename(`Average Clique Distance` = average_clique_distance) %>%
  rename(`Network Distance` = network_distance ) %>%
  pivot_longer(
    cols = c(`Network Distance`, `Average Clique Distance`),
    names_to = "Distance",
    values_to = "Value") %>% 
  mutate(copy_player = case_when(
    copy_player == 5 ~ "Five Players",
    copy_player == 4 ~ "Four Players",
    copy_player == 3 ~ "Three Players",
    copy_player == 2 ~ "Two Players",
    TRUE ~ as.character(copy_player)  # Preserve other values if needed
  )) %>%
  mutate(connections = case_when(
    connections == 5 ~ "5C",
    connections == 6 ~ "6C",
    connections == 7 ~ "7C",
    connections == 8 ~ "8C",
    connections == 9 ~ "9C",
    connections == 10 ~ "10C",
    TRUE ~ as.character(connections)  # Preserve other values if needed
  )) %>%
  rename(`Connection Count` = connections) %>%
  rename(`Connection Size` = copy_player)

network_connect_Num_and_size$`Connection Count` <- 
  factor(network_connect_Num_and_size$`Connection Count`, 
         levels = c("5C", 
                    "6C",
                    "7C",
                    "8C",
                    "9C",
                    "10C"))

ggplot(network_connect_Num_and_size %>%
         subset(Distance=="Network Distance"), 
       aes(x = `Connection Count`, 
           y = Value, 
           fill = `Connection Count`)) +
  geom_violin() +
  labs(
    title = "Final Network and Clique Distances",
    x = "Connection Count",
    y = "Final Distance") +
  ylim(0.65, 0.9) +  # Adjust y-axis range if needed
  facet_wrap(~`Connection Size`, ncol = 2) +
  theme_minimal() +
  scale_color_brewer(palette = "Set2") +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),  # Rotate x-axis text for readability
    text = element_text(family = "LM Roman 10", size = 16),
    strip.text = element_text(face = "bold"),
    legend.position = "bottom"
  )
