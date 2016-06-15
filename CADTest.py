### This code follows the main lines of the paper "Collective Anomaly Detection based on Long Short-Term Memory Recurrent Neural Network".
# It is an EXAMPLE illustrating the principal lines of the paper. The thresholds and parameters are not the ones used in the main experiment, and do not give similar results.
# The used data were preprocessed from the KDD 1999 tcpdump data (cf KDD1999_preprocess.py).

# Code by Loic BONTEMPS, INSA de Lyon.


from __future__ import print_function
from pybrain.datasets import SequentialDataSet
from itertools import cycle
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.supervised import RPropMinusTrainer
from sys import stdout
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np


# NB: data from day 7 was not used here.

# Original days of data -- 239 samples per day
training_data_unscaled = np.array([1294, 819, 421, 165, 136, 127, 128, 243, 262, 177, 453, 368, 299, 425, 1287, 1692, 976, 1137, 422, 299, 380, 285, 969, 378, 243, 277, 598, 524, 1016, 336, 141, 598, 362, 415, 868, 889, 1651, 295, 404, 466, 425, 389, 574, 407, 724, 415, 1513, 872, 1401, 348, 1188, 939, 555, 1845, 1004, 1232, 2876, 1015, 1242, 1350, 987, 798, 1315, 789, 1804, 1429, 184, 429, 1170, 1274, 4889, 1480, 1485, 1935, 3001, 1928, 2420, 2505, 1817, 787, 1408, 1998, 1296, 2133, 1430, 2392, 1451, 1463, 1194, 1489, 1923, 1805, 1679, 2686, 2011, 4078, 2546, 2615, 2801, 2228, 2958, 1911, 1488, 1832, 1347, 3281, 2092, 1682, 1816, 1293, 1636, 1511, 1482, 2788, 2455, 2874, 3500, 2086, 2468, 2801, 2759, 2259, 3804, 4073, 3381, 3983, 3360, 5194, 3102, 4455, 2859, 3064, 2941, 3080, 2242, 2995, 3130, 2424, 4664, 2911, 3169, 3378, 2680, 2219, 1683, 1129, 1192, 788, 2352, 930, 1827, 1993, 1721, 1353, 1658, 3619, 2020, 3348, 3643, 5766, 3532, 1503, 3005, 2716, 4170, 3516, 3054, 2408, 1566, 1360, 2408, 3715, 2457, 3092, 1563, 2327, 1845, 2207, 2303, 3059, 2012, 3939, 3345, 3773, 2409, 2744, 3429, 3037, 3215, 3252, 2773, 2828, 2218, 2811, 3210, 2308, 2060, 2072, 1591, 2735, 2318, 1859, 1400, 3845, 3043, 3239, 3362, 1955, 3050, 1954, 2327, 3616, 5648, 2364, 1578, 1738, 3495, 1966, 2723, 3618, 2855, 3409, 1169, 2130, 1591, 2986, 2895, 885, 1299, 2173, 1759, 2484, 2209, 2737, 1478, 2634, 2583, 1902, 3390, 2118, 1328, 2065, 4413, 2385, 1926, 1894, 2629, 4509, 2631, 1504, 1934, 2483, 1532, 3653, 2143, 1592, 2824, 2728, 1638, 1683, 1949, 1423, 1886, 2218, 2690, 2573, 1086, 3020, 2005, 2021, 2175, 1117, 2428, 2391, 3376, 2146, 2611, 2266, 1195, 2968, 4192, 1936, 1831, 2764, 2713, 1776, 2355, 3920, 2312, 1688, 1520, 3508, 1995, 1766, 3691, 1676, 2610, 4070, 2113])
training_data_unscaled_2 = np.array([353, 77, 1249, 158, 143, 276, 143, 149, 125, 246, 418, 535, 304, 556, 349, 547, 730, 459, 410, 1509, 985, 444, 1297, 1297, 467, 402, 592, 742, 2125, 686, 866, 844, 857, 1596, 954, 815, 729, 802, 279, 531, 292, 781, 852, 180, 704, 1324, 882, 564, 866, 1672, 1415, 1212, 760, 1180, 662, 619, 1263, 771, 736, 1037, 492, 932, 531, 1911, 562, 789, 636, 534, 476, 886, 2416, 1417, 335, 2260, 2901, 1507, 611, 1068, 3337, 1076, 367, 981, 942, 1378, 930, 1128, 589, 1462, 674, 536, 1594, 856, 1782, 395, 2615, 553, 1095, 543, 1106, 871, 388, 668, 1568, 1035, 569, 416, 1262, 220, 595, 653, 1040, 610, 986, 948, 548, 805, 1399, 1239, 833, 698, 358, 993, 3024, 587, 915, 2211, 2363, 1707, 2849, 3119, 2998, 980, 1668, 2165, 1717, 1165, 1658, 532, 2267, 949, 2674, 2701, 1520, 1758, 1307, 323, 1025, 367, 1375, 2344, 734, 1574, 1072, 1627, 1006, 1663, 1855, 2880, 2017, 2284, 2745, 1108, 1212, 2391, 645, 1978, 1083, 1213, 1965, 1310, 1677, 1528, 2031, 2327, 2308, 2545, 2138, 1955, 1476, 1108, 2299, 1124, 2207, 2408, 2205, 1385, 2452, 2478, 1177, 2134, 893, 1816, 3517, 1973, 3564, 4456, 5178, 4102, 2990, 3530, 1153, 2868, 3446, 2972, 1437, 2631, 2920, 1899, 2116, 2708, 3738, 3805, 3828, 2701, 2543, 2007, 2742, 2163, 2811, 2517, 2748, 1894, 2106, 1856, 3397, 2639, 3585, 3921, 1706, 2754, 4720, 2293, 2549, 2152, 4137, 1733, 1419, 2447, 1624, 3884, 2620, 3492, 3092, 3737, 1956, 1945, 1866, 3898, 1612, 1434, 4054, 2110, 2013, 803, 1834, 2490, 1653, 2511, 1931, 1514, 1710, 1405, 2185, 2102, 1437, 1461, 1133, 1625, 1631, 1525, 3667, 1960, 2334, 2103, 1572, 3853, 2605, 1311, 1861, 3774, 2662, 2466, 3474, 1978, 1490, 1307, 1479, 1801, 2467, 1247, 1457, 1592, 3211, 3315, 3799, 2874, 5288, 2697, 4237])
training_data_unscaled_3 = np.array([346, 228, 674, 295, 683, 151, 166, 503, 1060, 1037, 462, 2069, 353, 334, 463, 959, 587, 1475, 827, 1349, 370, 1137, 1935, 1327, 774, 919, 825, 691, 1577, 993, 731, 1659, 1737, 739, 1203, 1800, 647, 539, 704, 828, 1660, 1148, 1419, 1175, 1481, 3435, 2070, 1923, 1433, 812, 1288, 1764, 1622, 830, 1187, 3577, 1662, 1232, 1004, 1057, 1613, 2623, 1938, 765, 2303, 1713, 1078, 2273, 2101, 1879, 2159, 1175, 1162, 3355, 1348, 1865, 3612, 3369, 2359, 3354, 2335, 1688, 2723, 2460, 1731, 1075, 1635, 1062, 1652, 1458, 943, 866, 1275, 1413, 2977, 1610, 1738, 1504, 2150, 2592, 2104, 1769, 1626, 2934, 2562, 2568, 2064, 3410, 1961, 1388, 994, 3296, 1585, 1532, 916, 446, 1844, 663, 1524, 2055, 1214, 1053, 1003, 1926, 1920, 1624, 1079, 1602, 1496, 1698, 804, 1736, 1066, 808, 935, 977, 921, 552, 1306, 2452, 903, 2076, 1238, 2542, 2926, 1121, 964, 1624, 2182, 1437, 1254, 1376, 1679, 1941, 2856, 1613, 1641, 1291, 2126, 1480, 2864, 1401, 1384, 1860, 1902, 2172, 1660, 1494, 2873, 2138, 1839, 2328, 2668, 2457, 2544, 1526, 1545, 3185, 2737, 2116, 1789, 2791, 3205, 2626, 3434, 1645, 2073, 2443, 1159, 3039, 2452, 2731, 2805, 3107, 3810, 2336, 3459, 2455, 2641, 2399, 3705, 4126, 2941, 3151, 3619, 3870, 2591, 2411, 2605, 2591, 2507, 2769, 3767, 4248, 2710, 3648, 3055, 4124, 4680, 3003, 1986, 3948, 3469, 5307, 3020, 3645, 2129, 2960, 3383, 2925, 2072, 6762, 2193, 2060, 2802, 2331, 2835, 1718, 2042, 2539, 3450, 1788, 1816, 2201, 1541, 1194, 971, 1591, 868, 853, 1630, 1650, 2301, 3152, 2918, 4189, 1732, 3556, 2434, 1790, 1294, 1601, 2404, 1441, 1287, 1046, 2274, 1213, 2559, 1246, 1262, 2325, 2435, 1531, 1475, 1810, 2216, 1505, 1907, 2005, 1656, 1442, 1467, 1943, 2799, 1825, 2584, 1976, 2440, 2281, 1833, 1410, 1690, 4924, 1810, 2145, 757, 1972, 1499])
training_data_unscaled_4 = np.array([266, 766, 475, 430, 618, 166, 221, 231, 377, 478, 252, 167, 156, 117, 138, 233, 274, 84, 92, 78, 107, 94, 627, 90, 210, 383, 89, 155, 200, 92, 347, 284, 143, 182, 144, 751, 372, 255, 206, 440, 442, 341, 389, 127, 161, 854, 301, 186, 532, 513, 590, 937, 297, 264, 284, 445, 1029, 530, 863, 329, 743, 174, 254, 153, 163, 395, 560, 166, 193, 180, 195, 132, 135, 324, 473, 435, 1227, 515, 536, 455, 476, 451, 289, 307, 357, 959, 1312, 898, 539, 809, 857, 714, 765, 1189, 586, 439, 606, 1025, 529, 895, 662, 709, 1031, 1391, 1006, 1284, 860, 1264, 1549, 1330, 1276, 1302, 1213, 1400, 1358, 1328, 993, 1550, 1719, 1524, 1686, 939, 1810, 2422, 1995, 2046, 1214, 1909, 907, 1383, 771, 1303, 1039, 773, 939, 1124, 1540, 1080, 1364, 1247, 2144, 1397, 3216, 1948, 1215, 1315, 974, 1025, 1164, 2012, 1682, 1136, 1557, 1030, 1203, 635, 1007, 1156, 1479, 926, 1400, 1093, 1379, 1080, 918, 1537, 930, 1242, 1666, 1356, 2662, 1745, 824, 1110, 1391, 2297, 697, 1482, 1578, 985, 1173, 2083, 1471, 1013, 771, 1094, 3352, 1143, 1455, 1356, 1396, 1685, 2316, 1656, 1481, 2304, 1880, 2037, 1311, 1353, 1468, 1135, 1491, 1130, 1064, 1930, 2084, 3178, 1879, 2707, 1481, 3013, 3160, 3936, 3097, 2995, 3211, 2367, 1752, 3007, 2011, 2559, 2549, 2141, 2105, 3110, 1954, 1888, 3169, 2548, 2425, 3087, 2135, 2368, 2174, 2511, 1832, 2477, 3469, 3286, 2252, 3328, 3031, 1737, 5296, 4145, 3164, 2127, 2137, 1944, 2114, 2454, 1823, 1565, 1942, 3123, 1809, 2124, 2397, 1374, 2303, 1405, 3918, 4066, 2305, 2423, 2890, 2637, 2409, 1791, 3827, 2748, 1798, 3687, 3143, 3327, 1193, 1358, 3586, 4226, 1640, 3869, 2138, 3979, 2241, 2876, 3209, 2782, 1816, 1865, 1960, 1997, 1899, 2054, 2359, 2577, 2720, 2335, 2420])
training_data_unscaled_5 = np.array([225, 171, 184, 237, 340, 244, 130, 198, 402, 141, 748, 1002, 185, 559, 1012, 240, 480, 676, 380, 118, 341, 410, 882, 180, 431, 166, 83, 721, 328, 535, 121, 358, 793, 434, 901, 351, 126, 772, 951, 951, 333, 527, 210, 564, 590, 796, 774, 1583, 747, 1185, 939, 482, 1644, 1265, 1281, 1147, 551, 2190, 1170, 778, 911, 468, 745, 1504, 3463, 1447, 2148, 706, 1621, 1438, 2473, 2550, 3665, 2769, 3345, 2398, 2740, 902, 1873, 1494, 1584, 922, 2458, 2142, 1154, 1167, 3237, 1737, 1735, 1483, 1936, 1907, 1760, 2393, 2033, 3107, 1256, 4195, 3002, 1131, 2172, 1604, 2223, 1381, 1606, 2966, 2294, 2736, 2379, 2399, 2466, 1920, 2610, 1390, 1562, 1683, 1897, 1847, 2566, 3179, 3421, 2905, 2091, 1851, 1885, 1539, 2004, 1202, 3111, 2187, 1592, 2297, 2935, 1872, 1548, 1757, 1318, 1335, 1055, 1750, 1670, 2225, 2344, 1961, 2635, 2782, 2275, 2192, 2354, 3411, 2170, 2115, 1592, 1287, 1761, 2990, 2181, 1816, 1143, 1550, 848, 1429, 2625, 1342, 1416, 1707, 3318, 2793, 1452, 1176, 1017, 1163, 1394, 1722, 1096, 1926, 2794, 2455, 2297, 1844, 3827, 2729, 3121, 3218, 2267, 3319, 2993, 2757, 2440, 2644, 2995, 2246, 2531, 3088, 3118, 3164, 3184, 3789, 5535, 2936, 4836, 2714, 4231, 2865, 3505, 3249, 4301, 3598, 3184, 3450, 3639, 4519, 4035, 4421, 5064, 3298, 4549, 5777, 2984, 3621, 2889, 2482, 3152, 3744, 5032, 4733, 2455, 2864, 2847, 3232, 2325, 2587, 2943, 1888, 2856, 2444, 796, 2597, 2968, 3052, 3111, 3206, 2852, 2469, 1619, 3230, 4805, 2893, 1893, 2073, 1997, 2262, 1891, 2019, 2880, 1249, 1733, 2041, 1797, 2648, 2383, 2574, 1137, 2389, 1575, 3068, 1458, 1928, 1525, 2634, 1608, 2175, 1468, 912, 1756, 1608, 1969, 2496, 2894, 3463, 1272, 2382, 834, 2215, 1583, 3300, 1689, 2733, 2021, 2435, 1090, 1790, 2167, 1702, 2134, 2287, 1705, 1451, 2329])
training_data_unscaled_6 = np.array([495, 436, 659, 191, 509, 427, 760, 491, 602, 327, 608, 74, 431, 302, 245, 633, 408, 186, 303, 1243, 619, 615, 92, 638, 899, 387, 796, 1000, 675, 652, 126, 646, 2106, 427, 646, 511, 652, 503, 655, 312, 565, 404, 358, 660, 477, 84, 158, 165, 465, 155, 1121, 572, 925, 1032, 746, 800, 655, 263, 3098, 1128, 1714, 769, 1037, 499, 433, 802, 746, 683, 1305, 2192, 566, 945, 788, 648, 1291, 618, 1194, 2638, 454, 1333, 1509, 873, 1148, 1395, 955, 1626, 1024, 1094, 416, 881, 823, 1029, 1964, 1316, 1595, 1842, 1994, 3177, 3852, 2810, 2042, 2417, 1839, 2499, 1491, 1823, 1992, 1836, 1374, 1113, 1937, 1633, 1684, 1213, 1266, 1181, 1429, 3060, 1219, 1947, 1977, 2419, 1726, 4302, 2475, 1580, 1165, 1277, 1660, 1336, 1929, 1022, 1371, 2126, 1134, 1635, 2123, 1088, 882, 4070, 2815, 824, 1396, 2985, 2497, 2092, 2553, 2720, 3812, 1530, 3334, 1489, 637, 1858, 1797, 631, 1452, 1362, 1290, 1229, 2193, 1767, 994, 2516, 3812, 2570, 2633, 2385, 3197, 2517, 2159, 2843, 2272, 1658, 4013, 3683, 2608, 2534, 1764, 624, 2186, 1936, 1532, 2517, 2101, 1973, 1967, 2220, 1919, 1452, 2212, 572, 910, 1566, 1368, 2483, 1505, 937, 1456, 1416, 2156, 3094, 5479, 1073, 1475, 1591, 2094, 1180, 1020, 2083, 1435, 1450, 2299, 1037, 1121, 1774, 1485, 1445, 1397, 2430, 2607, 1881, 3245, 1761, 2646, 2444, 1923, 2420, 2597, 1992, 2816, 2482, 1937, 3440, 1916, 2045, 2023, 2058, 2522])
training_data_unscaled_8 = np.array([93, 955, 1087, 384, 1059, 1755, 2586, 1235, 1314, 1247, 1096, 1194, 887, 754, 2447, 1061, 961, 941, 826, 1266, 1358, 973, 2839, 2143, 960, 1296, 2273, 1726, 1683, 775, 1231, 829, 1179, 1149, 867, 1317, 2115, 3174, 1019, 4624, 4545, 2245, 1101, 2346, 2425, 2124, 1442, 1074, 1329, 960, 1262, 1709, 1219, 840, 1022, 1174, 2280, 2778, 1938, 3476, 2109, 3921, 844, 3312, 1310, 1075, 1012, 911, 1317, 876, 1845, 1573, 2867, 2075, 851, 1064, 1514, 873, 705, 411, 565, 871, 784, 567, 511, 452, 534, 645, 347, 220, 355, 649, 547, 1198, 609, 1137, 890, 1154, 941, 1665, 1482, 1363, 1756, 1615, 2434, 2188, 1474, 1920, 1224, 1890, 2515, 1733, 2267, 2401, 960, 1875, 2539, 1035, 873, 1318, 1170, 1864, 966, 1285, 1262, 1652, 1818, 1530, 977, 484, 490, 1511, 975, 559, 1019, 1062, 1571, 835, 920, 358, 400, 986, 1319, 1087, 1500, 1843, 1257, 3101, 2457, 1348, 3478, 2441, 798, 1371, 1285, 1178, 620, 1326, 1251, 1066, 1152, 1359, 1573, 1738, 2111, 1905, 650, 1312, 484, 1277, 544, 800, 437, 485, 1568, 1588, 1106, 1739, 1502, 1870, 1155, 2997, 418, 658, 1297, 1415, 1107, 1270, 1882, 1156, 1562, 2425, 1151, 1606, 1070, 1767, 1244, 1808, 1643, 1390, 1285, 3832, 1112, 1469, 1644, 3373, 3246, 2248, 2780, 7774, 2913, 1581, 3049, 1484, 1947, 3279, 2365, 1977, 2323, 2054, 2581, 2329, 2329, 2912, 3097, 1706, 2525, 2454, 1384, 2663, 2086, 1378, 2210, 2379, 2765, 2430, 1705, 2995, 1852])
training_data_unscaled_9 = np.array([71, 100, 90, 1117, 138, 763, 452, 437, 513, 1402, 1489, 1345, 887, 1159, 700, 201, 357, 438, 988, 886, 1478, 912, 955, 927, 815, 910, 666, 866, 1086, 707, 745, 992, 1451, 524, 1664, 1608, 588, 1126, 844, 2257, 1052, 1629, 1511, 1059, 2024, 1337, 1171, 2144, 1369, 987, 534, 728, 799, 407, 1644, 1024, 1751, 1556, 2412, 2003, 1390, 1344, 424, 553, 994, 1593, 2049, 3087, 1479, 1155, 742, 936, 1006, 1487, 2147, 1844, 1362, 1877, 2286, 2343, 4123, 1541, 2586, 2373, 583, 671, 960, 4001, 676, 1411, 1909, 831, 1545, 797, 1189, 4048, 2890, 1300, 6098, 1562, 1195, 694, 1499, 2140, 890, 2692, 3417, 2203, 1273, 681, 1425, 858, 1695, 2234, 2270, 2136, 1749, 3525, 1921, 1942, 2066, 579, 2281, 1936, 1032, 1131, 890, 1618, 1811, 979, 1680, 1186, 1175, 2370, 1009, 1605, 765, 1603, 1240, 595, 705, 837, 1283, 1127, 1445, 1369, 922, 493, 360, 856, 1030, 916, 537, 295, 1151, 899, 998, 1957, 1837, 2477, 1433, 925, 726, 632, 1099, 1201, 1183, 1009, 640, 1738, 1021, 756, 787, 1306, 1657, 1086, 1680, 1969, 788, 609, 1210, 1082, 1268, 1125, 1866, 1545, 2435, 1149, 1388, 1239, 1519, 1406, 1007, 1452, 1767, 875, 1795, 1500, 1735, 1415, 2521, 1204, 1373, 1470, 1829, 1735, 2266, 2087, 1807, 2405, 998, 1598, 1376, 1649, 708, 2690, 1600, 1668, 2066, 1660, 1437, 927, 2159, 2062, 1695, 1704, 2053, 2336, 1307, 1813, 3600, 1417, 2587, 2423, 3317, 2215, 1890, 2243, 2661])
training_data_unscaled_10 = np.array([187, 147, 200, 185, 105, 331, 209, 76, 75, 116, 282, 671, 363, 215, 182, 601, 760, 1013, 329, 479, 635, 856, 140, 1159, 1363, 982, 356, 1051, 150, 691, 216, 1634, 928, 328, 1787, 869, 813, 1574, 2206, 1646, 760, 2338, 462, 1455, 1687, 815, 943, 1093, 1532, 1932, 859, 767, 888, 1375, 733, 1576, 961, 660, 930, 1221, 1993, 4014, 2543, 728, 784, 3102, 1370, 1784, 1414, 2282, 1580, 1364, 2810, 827, 1829, 2359, 3896, 3399, 2105, 1618, 2030, 3046, 3058, 2167, 4106, 1889, 1891, 4608, 2294, 830, 1025, 1312, 1593, 1619, 1416, 1041, 1679, 2621, 3741, 3184, 1061, 1542, 1719, 2265, 1920, 1743, 2059, 1608, 2293, 1863, 2100, 2814, 1652, 3165, 1793, 1167, 2705, 3098, 1322, 1260, 1063, 1243, 1598, 4906, 3654, 1819, 1371, 1247, 2368, 1997, 2316, 2146, 1372, 1812, 2351, 1494, 1099, 1882, 1700, 2534, 1700, 1537, 1311, 1483, 1537, 2221, 2044, 1394, 3054, 1290, 1109, 2729, 2067, 3406, 2896, 2840, 1346, 2077, 3350, 1921, 2580, 899, 2067, 1677, 1360, 1506, 1098, 2214, 1693, 1374, 887, 1054, 1196, 1999, 2269, 1868, 3254, 1963, 2718, 2554, 1213, 2075, 1496, 1369, 2292, 3261, 1396, 3771, 2690, 2538, 3224, 3253, 1067, 3101, 3212, 2604, 1813, 3273, 2188, 2126, 2382, 2556, 2080, 4012, 1735, 3426, 3464, 1880, 1806, 2344, 2118, 1581, 4525, 4160, 3120, 3529, 4364, 3888, 4305, 2117, 2604, 3978, 2880, 3046, 3111, 2155, 2404, 2658, 2448, 2448, 1524, 1974, 2056, 2329, 1723, 2157, 5402, 3404, 2060])
testing_data_unscaled = np.array([397, 247, 241, 675, 377, 434, 757, 858, 965, 852, 1424, 531, 1512, 746, 844, 1068, 1009, 784, 1148, 2530, 351, 641, 563, 503, 3141, 496, 1526, 163, 820, 630, 302, 843, 325, 1017, 342, 469, 1111, 770, 1536, 892, 296, 661, 1186, 834, 766, 1626, 1008, 609, 1021, 914, 926, 1731, 1181, 593, 1359, 756, 690, 1309, 750, 854, 3129, 645, 881, 2386, 3484, 615, 536, 1209, 1039, 2090, 923, 718, 1524, 1237, 1413, 2293, 2448, 2684, 1214, 2285, 2687, 2583, 3201, 1316, 1641, 1228, 1659, 2349, 2124, 773, 1529, 1273, 2134, 790, 1336, 1884, 3503, 1438, 1897, 2893, 1226, 2726, 1494, 2041, 2541, 2009, 1254, 4455, 4166, 4820, 4552, 3967, 6512, 6264, 4050, 3361, 4203, 6275, 5893, 4504, 4588, 4342, 6503, 5880, 3266, 4190, 4210, 6303, 5865, 6255, 4435, 5395, 6920, 5835, 3532, 4992, 4165, 6107, 6909, 3674, 4059, 4276, 6035, 5801, 4096, 3836, 4053, 6197, 5903, 3717, 4951, 4168, 6298, 6299, 3375, 4285, 5233, 3731, 2988, 996, 1921, 1361, 1834, 1932, 1674, 1956, 1609, 668, 2581, 1312, 703, 1395, 1396, 911, 860, 2596, 1702, 1359, 2783, 921, 2278, 1184, 2314, 1419, 2341, 989, 1185, 1291, 794, 3855, 1059, 846, 1986, 733, 1059, 1283, 1360, 2173, 1273, 936, 2033, 769, 1993, 1335, 1817, 1048, 1410, 1037, 737, 1409, 1963, 1040, 1377, 918, 1474, 2552, 900, 938, 1181, 922, 518, 1412, 2060, 952, 1553, 834, 848, 551, 1026, 400, 1179, 1938, 1492, 959, 2217, 1133, 1057, 1141])


# Scaling the data
training_data = preprocessing.scale(training_data_unscaled)
training_data_2 = preprocessing.scale(training_data_unscaled_2)
training_data_3 = preprocessing.scale(training_data_unscaled_3)
training_data_4 = preprocessing.scale(training_data_unscaled_4)
training_data_5 = preprocessing.scale(training_data_unscaled_5)
training_data_6 = preprocessing.scale(training_data_unscaled_6)
training_data_8 = preprocessing.scale(training_data_unscaled_8)
training_data_9 = preprocessing.scale(training_data_unscaled_9)
training_data_10 = preprocessing.scale(training_data_unscaled_10)
testing_data = preprocessing.scale(testing_data_unscaled)


# Initialization of the system: 1input & 1output
dataset = SequentialDataSet(1, 1)
dataset_2 = SequentialDataSet(1, 1)
dataset_3 = SequentialDataSet(1, 1)
dataset_4 = SequentialDataSet(1, 1)
dataset_5 = SequentialDataSet(1, 1)
dataset_6 = SequentialDataSet(1, 1)
dataset_8 = SequentialDataSet(1, 1)
dataset_9 = SequentialDataSet(1, 1)
dataset_10 = SequentialDataSet(1, 1)
dataset_bis = SequentialDataSet(1, 1)

# Associates the current sample to the input, and the future sample to the output
for current_sample, next_sample in zip(training_data, cycle(training_data[1:])):
    dataset.addSample(current_sample, next_sample)
for current_sample, next_sample in zip(training_data_2, cycle(training_data_2[1:])):
    dataset_2.addSample(current_sample, next_sample)   
for current_sample, next_sample in zip(training_data_3, cycle(training_data_3[1:])):
    dataset_3.addSample(current_sample, next_sample)         
for current_sample, next_sample in zip(training_data_4, cycle(training_data_4[1:])):
    dataset_4.addSample(current_sample, next_sample)    
for current_sample, next_sample in zip(training_data_5, cycle(training_data_5[1:])):
    dataset_5.addSample(current_sample, next_sample)
for current_sample, next_sample in zip(training_data_6, cycle(training_data_6[1:])):
    dataset_6.addSample(current_sample, next_sample)
for current_sample, next_sample in zip(training_data_8, cycle(training_data_8[1:])):
    dataset_8.addSample(current_sample, next_sample)
for current_sample, next_sample in zip(training_data_9, cycle(training_data_9[1:])):
    dataset_9.addSample(current_sample, next_sample)
for current_sample, next_sample in zip(training_data_10, cycle(training_data_10[1:])):
    dataset_10.addSample(current_sample, next_sample)

for current_sample, next_sample in zip(testing_data, cycle(testing_data[1:])):
    dataset_bis.addSample(current_sample, next_sample)    



# Initializing the LSTM RNN: 23 nodes in the hidden layer
network = buildNetwork(1, 23, 1, hiddenclass=LSTMLayer, outputbias=False, recurrent=True)

# Training data
trainer = RPropMinusTrainer(network, dataset=dataset, delta0 = 0.01)
trainer_2 = RPropMinusTrainer(network, dataset=dataset_2, delta0 = 0.01)
trainer_3 = RPropMinusTrainer(network, dataset=dataset_3, delta0 = 0.01)
trainer_4 = RPropMinusTrainer(network, dataset=dataset_4, delta0 = 0.01)
trainer_5 = RPropMinusTrainer(network, dataset=dataset_5, delta0 = 0.01)
trainer_6 = RPropMinusTrainer(network, dataset=dataset_6, delta0 = 0.01)
trainer_8 = RPropMinusTrainer(network, dataset=dataset_8, delta0 = 0.01)
trainer_9 = RPropMinusTrainer(network, dataset=dataset_9, delta0 = 0.01)
trainer_10 = RPropMinusTrainer(network, dataset=dataset_10, delta0 = 0.01)


# Initiazlizing storage for the error curves
train_errors = [] 
train_errors_2 = [] 
train_errors_3 = [] 
train_errors_4 = [] 
train_errors_5 = [] 
train_errors_6 = [] 
train_errors_8 = [] 
train_errors_9 = [] 
train_errors_10 = [] 

# Training
EPOCHS_per_CYCLE = 6
NUM_CYCLES = 15
EPOCHS = EPOCHS_per_CYCLE * NUM_CYCLES
for i in xrange(NUM_CYCLES):
    trainer.trainEpochs(EPOCHS_per_CYCLE)
    train_errors.append(trainer.testOnData())
    trainer_2.trainEpochs(EPOCHS_per_CYCLE)
    train_errors_2.append(trainer_2.testOnData()) 
    trainer_3.trainEpochs(EPOCHS_per_CYCLE)
    train_errors_3.append(trainer_3.testOnData())
    trainer_4.trainEpochs(EPOCHS_per_CYCLE)
    train_errors_4.append(trainer_4.testOnData())
    trainer_5.trainEpochs(EPOCHS_per_CYCLE)
    train_errors_5.append(trainer_5.testOnData())
    trainer_6.trainEpochs(EPOCHS_per_CYCLE)
    train_errors_6.append(trainer_6.testOnData())
    trainer_8.trainEpochs(EPOCHS_per_CYCLE)
    train_errors_8.append(trainer_8.testOnData())
    trainer_9.trainEpochs(EPOCHS_per_CYCLE)
    train_errors_9.append(trainer_9.testOnData())
    trainer_10.trainEpochs(EPOCHS_per_CYCLE)
    train_errors_10.append(trainer_10.testOnData())

    epoch = (i+1) * EPOCHS_per_CYCLE
    print("\r epoch {}/{}".format(epoch, EPOCHS), end="")
    stdout.flush()

print("final error =", train_errors[-1])

# Plot the error curve
plt.plot(range(0, EPOCHS, EPOCHS_per_CYCLE), train_errors)
plt.xlabel('epoch')
plt.ylabel('error')
plt.show()


############################################


#Testing and error detection
average = 0
position = 0
my_error_position = 0
array_sum = 0
DC = 0
tab_avg_error = []
the_errors = []

MAT = 20
circular_array  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
detector  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Thresholds for collective anomaly detection, up to the user and their systems to set them
AVERAGE_THRESH = 0.8
DC_Thresh = 8
RET = 0.9


# Testing and detecting collective errors
for current_sample, target in dataset_bis.getSequenceIterator(0):

	# Test the data -- comp is the output of the network
    comp = network.activate(current_sample)

    # Error calculation
    erreur = comp - target
    the_errors.insert(my_error_position, abs(erreur))
  
    position += 1
    position  = position % MAT      
 
    # Integrating the newly calculated error value to the circular array
    circular_array.pop(position)
    circular_array.insert(position, abs(erreur))

    if abs(erreur) <= RET:                    
	    detector.pop(position)
	    detector.insert(position, 0)
     
    elif abs(erreur) > RET:                
    	detector.pop(position)
    	detector.insert(position, 1)
		
    # Computing the information from the circular array
	DC = sum(detector)
	array_sum = sum(circular_array)
    averaged_error = array_sum/20
    tab_avg_error.insert(my_error_position, averaged_error)

	# Triggering ALARM if necessary
    if averaged_error > AVERAGE_THRESH:
    	if DC > DC_Thresh:
        	print("ALARM at %4.1f" % my_error_position)

    my_error_position += 1
    print(my_error_position)
    print("       Current sample = %4.1f" % current_sample)
    print("Predicted next sample = %4.1f" % comp)
    print("   Actual next sample = %4.1f" % target)

plt.plot(tab_avg_error)
plt.show()