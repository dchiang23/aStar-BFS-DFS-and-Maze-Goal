from Maze import *

def main():
    random.seed(8675309)
    seeds = [random.randint(1111111,9999999) for i in range(30)]
    average_length_bfs = 0
    average_length_dfs = 0
    average_length_astar = 0
    average_num_cells_bfs = 0
    average_num_cells_dfs = 0
    average_num_cells_astar = 0
    bfs_goal = 0
    dfs_goal = 0
    aStar_goal = 0

    for seed in seeds:
        random.seed(seed)

        m = Maze(50,50, prop_blocked=0.25, search_order=SearchOrder.RANDOM)
        goal = m.bfs()
        m.calculatePathLength(goal)
        print(f"BFS: cells explored = {m._num_cells_explored} and path length = {m._path_length}")
        average_length_bfs+=m._path_length
        average_num_cells_bfs+=m._num_cells_explored
        if m._path_length != 0:
            bfs_goal+=1
        
            
        random.seed(seed)
        a = Maze(50,50, prop_blocked=0.25, search_order=SearchOrder.RANDOM)
        goal = a.dfs()
        a.calculatePathLength(goal)
        print(f"DFS: cells explored = {a._num_cells_explored} and path length = {a._path_length}")
        average_length_dfs+=a._path_length
        average_num_cells_dfs+=a._num_cells_explored
        if a._path_length != 0:
            dfs_goal+=1
        
        random.seed(seed)
        d = Maze(50,50, prop_blocked=0.25, search_order=SearchOrder.RANDOM)
        goal = d.aStar()
        d.calculatePathLength(goal)
        print(f"aStar: cells explored = {d._num_cells_explored} and path length = {d._path_length}")
        average_length_astar+=d._path_length
        average_num_cells_astar+=d._num_cells_explored
        if d._path_length != 0:
            aStar_goal+=1
        
        print("\n")

    average_length_bfs = average_length_bfs / bfs_goal
    average_length_dfs = average_length_dfs / dfs_goal
    average_length_astar = average_length_astar / aStar_goal
    average_num_cells_bfs = average_num_cells_bfs / bfs_goal
    average_num_cells_dfs = average_num_cells_dfs / dfs_goal
    average_num_cells_astar = average_num_cells_astar / aStar_goal

    print(f"average length for dfs is {average_length_dfs} and average num cells is {average_num_cells_dfs}")
    print(f"average length for bfs is {average_length_bfs} and average num cells is {average_num_cells_bfs}")
    print(f"average length for astar is {average_length_astar} and average num cells is {average_num_cells_astar}")
    print(f"dfs paths: {dfs_goal}")
    print(f"bfs paths: {bfs_goal}")
    print(f"astar paths: {aStar_goal}")

if __name__ == "__main__":

    main()