import pygtk
import gtk

import path


class PathGui:
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def choose_heuristic(self, widget, function):
        if widget.get_active():
            self.heuristic = function

    def __init__(self):
        self.maze = path.Maze(8,8,
           [[ 0 , 0 , 0 ,'X','X', 0 ,'X','S'],
            [ 0 ,'X', 0 , 0 ,'X', 0 , 0 , 0 ],
            [ 0 ,'X','X', 0 , 0 , 0 ,'X','X'],
            [ 0 ,'X', 0 , 0 ,'X', 0 , 0 , 0 ],
            [ 0 , 0 , 0 ,'X','X', 0 ,'X', 0 ],
            [ 0 ,'X', 0 , 0 ,'X', 0 ,'X', 0 ],
            [ 0 ,'X','X', 0 , 0 , 0 ,'X','X'],
            [ 0 ,'G', 0 , 0 ,'X', 0 , 0 , 0 ]])

        self.running = False
        self.buttons = []
        self.heuristic = self.maze.dijkstra
        ## After this, it's all GUI stuff
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("PathMaster")
        self.window.connect("delete_event", self.delete_event)

        hbox = gtk.HBox()
        table = gtk.Table(8, 8, True)
        for row in range(8):
            row_list = []
            for col in range(8):
                button = self.make_box(row, col)
                row_list.append(button)
                table.attach(button, col, col+1, row, row+1)
                button.show()
            self.buttons.append(row_list)
        hbox.pack_start(table)
        
        # Add in the Other UI stuff
        settings = gtk.VBox()
        dijkstra = gtk.RadioButton(label="No Applied Heuristic")
        dijkstra.connect("toggled", self.choose_heuristic, self.maze.dijkstra)
        dijkstra.set_active(True)
        dijkstra.show()
        manhattan = gtk.RadioButton(dijkstra, label="Manhattan Distance Heuristic")
        manhattan.connect("toggled", self.choose_heuristic, self.maze.manhattan)
        manhattan.show()
        perfect = gtk.RadioButton(dijkstra, "A Perfect Heuristic")
        perfect.connect("toggled", self.choose_heuristic, self.maze.perfect)
        perfect.show()
        
        settings.pack_start(dijkstra)
        settings.pack_start(manhattan)
        settings.pack_start(perfect)
        
        continue_button = gtk.Button("Continue Algorithm")
        continue_button.connect("clicked", self.next_step)
        re_start_button = gtk.Button("Start Algorithm")
        re_start_button.connect("clicked", self.first_step)
        continue_button.show()
        re_start_button.show()

        settings.pack_end(continue_button)
        settings.pack_end(re_start_button)
        
        settings.show()

        hbox.pack_start(settings)
        self.window.add(hbox)
        table.set_size_request(600, 600)
        table.show()
        hbox.show()
        self.window.show()

    def button_rotate(self, widget, (x, y)):
        """Change the underlying maze
        
        The transitions are:
        Open -> Wall -> Start -> End
        """
        currtype = self.maze.maze.grid[x][y]
        if currtype == 'X':
            self.maze.maze.grid[x][y] = 'S'
            widget.set_label('S')
        elif currtype == 'S':
            self.maze.maze.grid[x][y] = 'G'
            widget.set_label('G')
        elif currtype == 'G':
            self.maze.maze.grid[x][y] = 0
            widget.set_label(' ')
        else: # Must be an open space
            self.maze.maze.grid[x][y] = 'X'
            widget.set_label('X')

    def first_step(self, widget):
        if self.running: # Want to reset
            tempmaze = path.Maze(8,8)
            for row in range(8):
                for column in range(8):
                    if self.maze.maze.grid[row][column] == 'X':
                        tempmaze.maze.grid[row][column] = 'X'
                    elif self.maze.maze.grid[row][column] == 'G':
                        tempmaze.maze.grid[row][column] = 'G'
                    elif self.maze.maze.grid[row][column] == 'S':
                        tempmaze.maze.grid[row][column] = 'S'
            self.maze = tempmaze
            self.update_maze()
            self.running = False
            widget.set_label("Start Algorithm")
        else:
            self.maze.start_solve(self.heuristic)
            self.running = True
            widget.set_label("Reset Grid")

    def next_step(self, widget):
        # Run the map again and update the grid
        if self.running:
            self.maze.continue_solve()
            self.update_maze()
            if self.maze.pathlen != -1: self.running = False

    def update_maze(self):
        for x in range(8):
            for y in range(8):
                temp = self.maze.maze.grid[x][y]
                if temp != 0:
                    self.buttons[x][y].set_label(str(temp))
                else: self.buttons[x][y].set_label(' ')


    def make_box(self, x, y):
        button = gtk.Button()
        button.connect("clicked", self.button_rotate, (x, y))
        label = self.maze.maze.grid[x][y]
        button.set_label(' ') if label == 0 else button.set_label(label)
        return button

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    PathGui()
    main()
