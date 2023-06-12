# -*- coding:utf-8 -*-
# @FileName  :life_game.py
# @Time      :2023/6/5 19:58

"""
结对编程实验
"""

from random import randint

import pygame

pygame.init()


class GameMap:
    def __init__(self, rows, cols, p=0.2):
        self.grid = []
        self.rows = rows
        self.cols = cols
        self.p = p
        self.grid_size = rows * cols
        self.reset()

    def reset(self):
        """
        初始化/重置地图网格
        :return:
        """
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        for _ in range(int(self.grid_size * self.p)):
            index = randint(0, self.grid_size - 1)
            self.grid[index // self.cols][index % self.cols] = 1

    def get_neighbor_count(self, i, j) -> int:
        """
        计算一个点邻居的数量
        :param i: i
        :param j: j
        :return: 邻居数量
        """
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                ni, nj = i + dx, j + dy
                if 0 <= ni < self.rows and 0 <= nj < self.cols and self.grid[ni][nj] == 1:
                    count += 1
        return count

    def update(self) -> None:
        """
        更新地图网格
        :return: None
        """
        new_grid = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                alive_neighbors = self.get_neighbor_count(i, j)
                if self.grid[i][j] == 1:
                    if alive_neighbors == 2 or alive_neighbors == 3:
                        new_grid[i][j] = 1
                elif self.grid[i][j] == 0:
                    if alive_neighbors == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid

    def get_grid(self):
        return self.grid


class LifeGame:
    def __init__(self, rows, cols, p=0.2, refresh_rate=0.2, cell_size=18):
        self.map = GameMap(rows=rows, cols=cols, p=p)
        self.refresh_rate = refresh_rate
        self.cell_size = cell_size

        # 设置时钟
        self.clock = pygame.time.Clock()

        # 设置屏幕尺寸
        self.screen_width = self.map.cols * cell_size
        self.screen_height = self.map.rows * cell_size

        # 创建屏幕对象
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption("Grid Display")

    def game_circle(self) -> None:
        """
        每次更新画面调用的函数
        :return: None
        """
        # 清空屏幕
        self.screen.fill((255, 255, 255))
        # 绘制网格
        for row in range(self.map.rows):
            for col in range(self.map.cols):
                cell_color = (0, 0, 0) if self.map.get_grid()[row][col] == 1 else (255, 255, 255)
                pygame.draw.rect(self.screen, cell_color,
                                 (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

        # 更新屏幕
        pygame.display.flip()

    def handle_events(self) -> None:
        """
        捕获事件并且处理
        :return: None
        """
        for event in pygame.event.get():
            # 退出事件执行函数
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def start(self) -> None:
        """
        开始游戏
        :return:
        """
        while True:
            self.handle_events()
            self.game_circle()
            self.map.update()

            # 设置刷新率
            self.clock.tick(self.refresh_rate)


if __name__ == '__main__':
    LifeGame(rows=40, cols=40, p=0.3, refresh_rate=5).start()
