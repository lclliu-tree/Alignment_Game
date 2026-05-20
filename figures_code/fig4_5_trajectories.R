library(dplyr)
library(data.table)
library(ggplot2)
setwd("~/Agent_Based_Modelling/results/two_player")
#####################################
data <- fread("trajectory.csv")

data_adaptive <- data %>% 
  select(Update, `Adaptive Player 1`, `Adaptive Player 2`) %>%
  pivot_longer(
    cols = c(`Adaptive Player 1`, `Adaptive Player 2`),
    names_to = "Player",
    values_to = "Value")
# Plot
ggplot(data_adaptive, aes(x = Update, y = Value, color = Player)) +
  geom_line(size = 1.2) +  # Line thickness
  theme_minimal() +
  labs(
    title = "Adaptive players' meaning alignment",
    x = "Update Number",
    y = "Point in [0,1] space",
    color = "Player"
  ) +
  scale_fill_brewer(palette = "Set2") +
  theme(#axis.text.x = element_blank(),
        text=element_text(family="LM Roman 10", size=16),
        strip.text = element_text(face = "bold"),
        legend.position = "bottom")

data_nonadaptive <- data %>% 
  select(Update, `Nonadaptive Player 1`, `Nonadaptive Player 2`) %>%
  pivot_longer(
    cols = c(`Nonadaptive Player 1`, `Nonadaptive Player 2`),
    names_to = "Player",
    values_to = "Value")
# Plot
ggplot(data_nonadaptive, aes(x = Update, y = Value, color = Player)) +
  geom_line(size = 1.2) +  # Line thickness
  theme_minimal() +
  labs(
    title = "Non-adaptive players' meaning alignment",
    x = "Update Number",
    y = "Point in [0,1] space",
    color = "Player"
  ) +
  scale_fill_brewer(palette = "Set2") +
  theme(#axis.text.x = element_blank(),
        text=element_text(family="LM Roman 10", size=16),
        strip.text = element_text(face = "bold"),
        legend.position = "bottom")
####

library(dplyr)
library(data.table)
library(ggplot2)
library(tidyr)

setwd("~/Agent_Based_Modelling/results/two_player")
data <- fread("trajectory.csv")

# ---- Adaptive trajectory ----
data_adaptive <- data %>% 
  select(Update, `Adaptive Player 1`, `Adaptive Player 2`) %>%
  pivot_longer(
    cols = c(`Adaptive Player 1`, `Adaptive Player 2`),
    names_to = "Player",
    values_to = "Value")

p_adaptive <- ggplot(data_adaptive, aes(x = Update, y = Value, color = Player)) +
  geom_line(linewidth = 0.8) +
  theme_minimal(base_size = 11, base_family = "LM Roman 10") +
  scale_color_brewer(palette = "Set2") +
  labs(title = "Adaptive players' meaning alignment",
       x = "Update Number", y = "Point in [0,1] space",
       color = NULL) +
  theme(
    axis.text  = element_text(size = 10),
    axis.title = element_text(size = 11),
    plot.title = element_text(size = 12, hjust = 0.5),
    legend.position = "bottom",
    legend.text = element_text(size = 10),
    legend.margin = margin(t = -5),
    plot.margin = margin(6, 12, 4, 6),
    plot.background  = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA)
  )

# ---- Non-adaptive trajectory ----
data_nonadaptive <- data %>% 
  select(Update, `Nonadaptive Player 1`, `Nonadaptive Player 2`) %>%
  pivot_longer(
    cols = c(`Nonadaptive Player 1`, `Nonadaptive Player 2`),
    names_to = "Player",
    values_to = "Value")

p_nonadaptive <- ggplot(data_nonadaptive, aes(x = Update, y = Value, color = Player)) +
  geom_line(linewidth = 0.8) +
  theme_minimal(base_size = 11, base_family = "LM Roman 10") +
  scale_color_brewer(palette = "Set2") +
  labs(title = "Non-adaptive players' meaning alignment",
       x = "Update Number", y = "Point in [0,1] space",
       color = NULL) +
  theme(
    axis.text  = element_text(size = 10),
    axis.title = element_text(size = 11),
    plot.title = element_text(size = 12, hjust = 0.5),
    legend.position = "bottom",
    legend.text = element_text(size = 10),
    legend.margin = margin(t = -5),
    plot.margin = margin(6, 12, 4, 6),
    plot.background  = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA)
  )

# ---- Export ----
ggsave("trajectory_adaptive.png",
       plot = p_adaptive, width = 6.9, height = 3, units = "in",
       dpi = 600, bg = "white")

ggsave("trajectory_nonadaptive.png",
       plot = p_nonadaptive, width = 6.9, height = 3, units = "in",
       dpi = 600, bg = "white")


