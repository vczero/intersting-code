# @author: wanglihua
# @time: 2021/10/2 18:24
# @target: 分油 + BFS 算法

# 序列化 [10, 3, 7] 为 10-3-7，便于记录和比较访问过的状态
def genFormatKey(oil_list):
    new_list = [str(i) for i in oil_list]
    return '-'.join(new_list)

# 默认容器最大大小 [10, 7, 3]，将桶标记为1号、2号桶、3号桶
# 倒油问题：有10、7、3斤的桶，目标平均分10斤油
# 初始状态 [10, 0, 0]
# 目标状态 5，只要有一个桶是5，另外剩下的就是5
# 倒油逻辑（桶编码推导）：
# 1.直接判断不可以的情况：1-1, 2-2, 3-3
# 2.空桶不可以倒入其他桶：
# 3.对方油满不可以倒入；
# 4.剩油判断
# bucket_volume 容器容量
# oil_container 父节点
def getNodes(bucket_volume, oil_container):
    expand_nodes = []
    for i in range(len(oil_container)):
        for j in range(len(oil_container)):
            # 子节点临时变量
            temp = oil_container.copy()
            # 自己不能倒给自己
            if i == j:
                continue
            # 自己没有油也不能倒
            elif oil_container[i] == 0:
                continue
            # 对方油满了不能倒，需要判断容器大小
            elif oil_container[j] == bucket_volume[j]:
                continue
            # 正常倒油: 直接倒入 或者 部分倒入
            elif oil_container[i] + oil_container[j] <= bucket_volume[j]:
                # 直接倒入
                temp[i] = 0
                temp[j] = oil_container[i] + oil_container[j]
                expand_nodes.append(temp)
            else:
                # 部分倒入
                temp[j] = bucket_volume[j]
                temp[i] = oil_container[i] - (bucket_volume[j] - oil_container[j])
                expand_nodes.append(temp)
    return expand_nodes

# PourBFS
def PourBFS(bucket_volume, init_state, goal_state):
    # 存放子节点，先进先出队列，一层层展开
    temp_queue = []
    # 访问状态记录
    visited_set = set()
    # 搜索结果数组
    result_arr = []
    # 初始化数据
    temp_queue.append(init_state)
    visited_set.add(genFormatKey(init_state))
    
    # 出队
    while len(temp_queue):
        # 1.取出队首
        temp_node = temp_queue.pop(0)
        print(temp_node)
        # 2.通过倒油过程获得子节点
        find_nodes = getNodes(bucket_volume, temp_node)
        # 3.判断该节点是否已经被访问过，若无，则将子节点压入到队尾
        for node in find_nodes:
            if genFormatKey(node) not in visited_set:
                temp_queue.append(node)
                visited_set.add(genFormatKey(node))
        # 4.存放从队首剔除的节点
        result_arr.append(temp_node)

        # 5.目标节点，终止搜索
        # 查找某一个桶是多少斤
        if isinstance(goal_state, int):
            if goal_state in temp_node:
                print('完成搜索，结果为：', temp_node)
                break

        # 查找完全分配，例如（5，5，0）
        if isinstance(goal_state, list):
            if genFormatKey(temp_node) == genFormatKey(goal_state):
                print('完成搜索，结果为：', temp_node)
                break

# 使用案例1：分出1个4斤的来
# PourBFS([10, 7, 3], [10, 0, 0], 4)
# 使用案例2：完全分出两个5斤
# PourBFS([10, 7, 3], [10, 0, 0], [5, 5, 0])
# 使用案例3：分出1个5斤的来
PourBFS([10, 7, 3], [10, 0, 0], 5)











