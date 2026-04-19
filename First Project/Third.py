class Robot:
    directions = ["up","right","down","left"]
    def __init__(self, x,y,direction):
        self.x = x
        self.y = y
        self.direction = direction
    def move (self,grid):
        n = len(grid)
        m = len(grid[0])
        dx,dy=0,0
        if self.direction == "up":
            dx, dy = -1, 0
        elif self.direction == "down":
            dx, dy = 1, 0
        elif self.direction == "left":
            dx, dy = 0, -1
        elif self.direction == "right":
            dx, dy = 0, 1
        nx = self.x + dx
        ny = self.y + dy
        while 0<=nx<n and 0<=ny<m and grid[nx][ny] !="#":
            if grid[nx][ny] == ".":
                grid[nx][ny] = "c"
            self.x = nx
            self.y = ny
            nx += dx
            ny += dy
        self.turn()
    def turn(self):
            i = Robot.directions.index(self.direction)
            self.direction = Robot.directions[(1+i)%4]

class Game:
    def __init__(self,r1,r2):
        self.r1 = r1
        self.r2 = r2
        self.grid = [
            list("#..#.."),
            list(".#...."),
            list("#....."),
            list(".#...."),
            list("...#..")
        ]
        if self.grid[r1.x][r1.y] == ".":
            self.grid[r1.x][r1.y] = "c"
        if self.grid[r2.x][r2.y] == ".":
            self.grid[r2.x][r2.y] = "c"
    def simulate(self):
        for _ in range(15):
            self.r1.move(self.grid)
            self.r2.move(self.grid)
    def count_cleaned(self):
        count = 0
        for row in self.grid:
            for c in row:
                if c == "c":
                    count += 1
        return count

x1, y1, d1 = input().split()
x2, y2, d2 = input().split()

r1 = Robot(int(x1), int(y1), d1)
r2 = Robot(int(x2), int(y2), d2)

game = Game(r1, r2)
game.simulate()

print(game.count_cleaned())