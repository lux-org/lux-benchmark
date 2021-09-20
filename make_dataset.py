from utils.data_utils import generate_airbnb_copies, generate_communities_copies, save_downsample_communities, save_downsample_airbnb
generate_airbnb_copies(100)
generate_airbnb_copies(250)
generate_communities_copies(100) # assumes lux-datasets is in the same directory as lux-benchmark
save_downsample_communities(20000)
save_downsample_communities(5000)
save_downsample_communities(50000)


save_downsample_airbnb(30000)
save_downsample_airbnb(40000)
save_downsample_airbnb(100000)
save_downsample_airbnb(1000000)