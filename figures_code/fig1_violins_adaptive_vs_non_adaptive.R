library(ggplot2)
library(dplyr)
library(tidyr)
library(extrafont)
# Reshape data to long format using dplyr
data_fig_1 <- data %>%
  pivot_longer(
    cols = c(first_percev_convg, first_actual_convg, final_distance),
    names_to = "variable",
    values_to = "Value")  %>% 
  mutate(variable = case_when(
    variable == "first_percev_convg" ~ "First Perceived Convergence",
    variable == "first_actual_convg" ~ "First Actual Convergence",
    variable == "final_distance" ~ "Final Mean Distance",
    TRUE ~ as.character(variable)  # Preserve other values if needed
    )) %>% 
  mutate(degrade = case_when(
    degrade == 0 ~ "No Degradation (0%)",
    degrade == 0.001 ~ "Low Degradation (0.001%)",
    degrade == 0.01 ~ "Moderate Degradation (0.01%)",
    degrade == 0.1 ~ "High Degradation (0.1%)",
    TRUE ~ as.character(degrade)  # Preserve other values if needed
  )) %>% 
  mutate(prototypes = case_when(
    prototypes == 3 ~ "Three Prototypes",
    prototypes == 5 ~ "Five Prototypes",
    prototypes == 10 ~ "Ten Prototypes",
    TRUE ~ as.character(prototypes)  # Preserve other values if needed
  ))

data_fig_1$degrade_factor <- 
  factor(data_fig_1$degrade, 
         levels = 
           c("No Degradation (0%)",
             "Low Degradation (0.001%)", 
             "Medium Degradation (0.01%)", 
             "High Degradation (0.1%)"))

data_fig_1$Prototypes <- 
  factor(data_fig_1$prototypes, 
         levels = 
           c("Three Prototypes", 
             "Five Prototypes", 
             "Ten Prototypes"))

data_fig_1$adaptiveness <- 
  factor(data_fig_1$adaptiveness, 
         levels = 
           c("Low Adaptability (1%)", 
             "Moderate Adaptability (5%)", 
             "High Adaptability (10%)"))

# Create violin plot
# Adaptive vs. Non-Adaptive
p1 <- ggplot(data_fig_1, aes(x = type, y = Value, fill = type)) +
  geom_violin(trim = FALSE, alpha = 0.7) +
  facet_wrap(~ variable, scales = "free_y") +
  theme_minimal(base_size = 11, base_family = "LM Roman 10") +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Convergence and alignment by type of player",
       x = NULL, y = "Value", fill = NULL) +
  theme(
    axis.text.x  = element_blank(),
    axis.ticks.x = element_blank(),
    axis.text.y  = element_text(size = 10),
    axis.title.y = element_text(size = 11),
    strip.text   = element_text(face = "bold", size = 9.6),  # slightly smaller
    plot.title   = element_text(size = 12, hjust = 0.5),
    legend.position = "bottom",
    legend.text  = element_text(size = 10),
    legend.margin = margin(t = -5),
    plot.margin  = margin(6, 12, 4, 6),                     # extra right margin
    plot.background  = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA)
  )

ggsave("convergence_by_type.png", 
       plot = p1,
       width = 6.9, height = 4, units = "in",
       dpi = 600)

# By Adaptivity

p2 <- ggplot(data_fig_1 %>% subset(type == "Adaptive"), 
             aes(x = adaptiveness, y = Value, fill = adaptiveness)) +
  geom_violin(trim = FALSE, alpha = 0.7) +
  stat_summary(fun = median, geom = "point",
               aes(group = 1), color = "black", size = 2) +
  facet_wrap(~ variable, scales = "free_y") +
  theme_minimal(base_size = 11, base_family = "LM Roman 10") +
  scale_fill_brewer(palette = "Set2",
                    labels = c("1% (Low)", "5% (Moderate)", "10% (High)")) +
  labs(title = "Convergence and alignment by adaptiveness level",
       x = NULL, y = "Value", fill = NULL) +
  theme(
    axis.text.x  = element_blank(),
    axis.ticks.x = element_blank(),
    axis.text.y  = element_text(size = 10),
    axis.title.y = element_text(size = 11),
    strip.text   = element_text(face = "bold", size = 9.6),
    plot.title   = element_text(size = 12, hjust = 0.5),
    legend.position = "bottom",
    legend.text  = element_text(size = 10),
    legend.margin = margin(t = -5),
    plot.margin  = margin(6, 12, 4, 6),
    plot.background  = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA)
  )

ggsave("convergence_by_adaptability.png",
       plot = p2, width = 6.9, height = 3, units = "in",
       dpi = 600, bg = "white")

# Non-adaptive, by degradation
# 1. Refactor degrade
data_fig_1$degrade <- factor(data_fig_1$degrade,
                             levels = c("No Degradation (0%)",
                                        "Low Degradation (0.001%)",
                                        "Moderate Degradation (0.01%)",
                                        "High Degradation (0.1%)"))

# 2. Verify
levels(data_fig_1$degrade)
table(data_fig_1$degrade[data_fig_1$type == "Non-adaptive"], useNA = "ifany")

# 3. THEN rebuild p3

p3 <- ggplot(data_fig_1 %>% subset(type == "Non-adaptive"), 
             aes(x = degrade, y = Value, fill = degrade)) +
  geom_violin(trim = FALSE, alpha = 0.7) +
  #geom_boxplot(width = 0.1, alpha = 0.5, outlier.size = 0.5) +  # add this
  facet_wrap(~ variable, scales = "free_y") +
  theme_minimal(base_size = 11, base_family = "LM Roman 10") +
  scale_fill_brewer(palette = "Set2",
                    labels = c("0% (None)", "0.001% (Low)",
                               "0.01% (Moderate)", "0.1% (High)")) +
  labs(title = "Convergence and alignment by memory degradation level",
       x = NULL, y = "Value", fill = NULL) +
  theme(
    axis.text.x  = element_blank(),
    axis.ticks.x = element_blank(),
    axis.text.y  = element_text(size = 10),
    axis.title.y = element_text(size = 11),
    strip.text   = element_text(face = "bold", size = 9.6),
    plot.title   = element_text(size = 12, hjust = 0.5),
    legend.position = "bottom",
    legend.text  = element_text(size = 9),         # slightly smaller — 4 labels
    legend.margin = margin(t = -5),
    plot.margin  = margin(6, 12, 4, 6),
    plot.background  = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA)
  ) +
  guides(fill = guide_legend(nrow = 1))            # force one row if it fits


ggsave("converge_nonadaptives.png",
       plot = p3, width = 6.9, height = 3, units = "in",
       dpi = 600, bg = "white")

# Adaptive vs. Non-Adaptive
p3 <- ggplot(data_fig_1, aes(x = Prototypes, y = Value, fill = Prototypes)) +
  geom_violin(trim = FALSE, alpha = 0.7) +
  facet_wrap(variable ~type, ncol = 2, scales = "free_y") +  # Separate plots for each variable
  theme_minimal() +
  scale_fill_brewer(palette = "Set2") +
  labs(title = "Convergence and alignment by number of prototypes",
       x = "Type",
       y = "Value") +
  theme(axis.text.x = element_blank(),
        text=element_text(family="LM Roman 10", size=20),
        strip.text = element_text(face = "bold"),
        legend.position = "bottom")

# PNG backup at high DPI
ggsave("converge_nonadaptives.png", 
       plot = p3,
       width = 6.9, height = 4, units = "in",
       dpi = 600)

means_by_group <- data_fig_1 %>%
  group_by(adaptiveness) %>%
  select(adaptiveness, variable,Value) %>%
  subset(variable == "Final Mean Distance") %>%
  summarise(mean_value = mean(Value, na.rm = TRUE))
