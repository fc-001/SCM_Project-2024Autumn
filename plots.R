library(ggplot2)
library(scales)
data <- data.frame(
  Year = 2014:2023,
  Inventory = c(36.99, 42.5, 53.79, 55.82, 81.19, 123.3, 108.8, 107.9, 104.7, 82.69),
  Impairment = c(1140, 1385, 1210, 1852, 2266, 6866, 6786, 7732, 7618, 6982)
)

p <- ggplot(data, aes(x = Year)) +
  # 左轴：存货
  geom_line(aes(y = Inventory), color = "blue", size = 1) +
  geom_point(aes(y = Inventory), color = "blue", size = 2, shape = 16) +
  scale_y_continuous(
    name = "Inventory (10M¥)", 
    limits = c(0, 130), 
    sec.axis = sec_axis(~ . * (8000 / 130), name = "Inventory Impairment (10K¥)", labels = comma)
  ) +
  
  # 右轴：存货减值准备
  geom_line(aes(y = Impairment * (130 / 8000)), color = "red", size = 1) + 
  geom_point(aes(y = Impairment * (130 / 8000)), color = "red", size = 2, shape = 17) +
  
  labs(
    title = "Inventory & Inventory Impairment of YongHui during the Past 10 Years",
    x = "Year", y = "Inventory (10M¥)"
  ) +
  
  theme_minimal(base_size = 12) +
  theme(
    legend.position = "bottom",
    legend.title = element_blank(),
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    axis.title.y.left = element_text(color = "blue", face = "bold"),
    axis.title.y.right = element_text(color = "red", face = "bold")
  )
print(p)




data2 <- data.frame(
  Year = 2014:2023,
  CurrentRatio = c(1.487, 1.505, 2.047, 1.652, 1.201, 0.987, 0.951, 0.842, 0.844, 0.77),
  QuickRatio = c(0.991, 0.969, 1.151, 1.198, 0.794, 0.595, 0.639, 0.526, 0.484, 0.435)
)
p2 <- ggplot(data2, aes(x = Year)) +
  # 流动比率
  geom_line(aes(y = CurrentRatio, color = "Current Ratio"), size = 1.2) +
  geom_point(aes(y = CurrentRatio, color = "Current Ratio"), size = 2) +
  # 速动比率
  geom_line(aes(y = QuickRatio, color = "Quick Ratio"), size = 1.2) +
  geom_point(aes(y = QuickRatio, color = "Quick Ratio"), size = 2) +
  labs(
    title = "Current Ratio & Quick Ratio of YongHui during the Past 10 Years",
    x = "Year",
    y = "Ratio",
    color = "Metrics"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position = "bottom",
    legend.title = element_text(size = 10, face = "bold"),
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    axis.title.y = element_text(size = 12, face = "bold")
  ) +
  scale_color_manual(values = c("Current Ratio" = "green", "Quick Ratio" = "orange"))
print(p2)