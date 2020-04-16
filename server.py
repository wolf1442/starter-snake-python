import os

import cherrypy
"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    def index(self):
        # If you open your snake URL in a browser you should see this message.
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        # The Battlesnake engine calls this function to make sure your snake is working.
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json
        print("START")
        return {
            "color": "#2F00FF",
            "headType": "bwc-scarf",
            "tailType": "regular"
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        data = cherrypy.request.json
        snake = Snake(data)
        move = snake.get_next_move()

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        print("END")
        return "ok"


class Snake:
    def __init__(self, request):
        self.request = request

    def get_next_move(self):
        move = "up"

        moves = self.get_preferred_move_order()
        for m in moves: 
            if self.is_move_safe(m):
                move = m
                break

        return move

    def get_head_coords(self):
        return self.request["you"]["body"][0]

    def get_preferred_move_order(self):
        return ["up", "left", "down", "right"]

    def is_move_safe(self, move):
      move_coords = self.translate_move_to_coords(move)
      if move_coords["x"] < 0:
        return False
      if move_coords["y"] < 0:
        return False
      if move_coords["x"] >= self.request["board"]["width"]:
        return False
      if move_coords["y"] >= self.request["board"]["height"]:
        return False

      return True
       
    def translate_move_to_coords(self)      
        head = self.get_head_coords()
        if move == "up":
          return {"x": head["x"], "y": head["y"] - 1}
        if move == "down":
          return {"x": head["x"], "y": head["y"] + 1}
        if move == "left":
          return {"x": head["x"] - 1, "y": head["y"]}
        if move == "right":
          return {"x": head["x"] + 1, "y": head["y"]}

        

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({
        "server.socket_port":
        int(os.environ.get("PORT", "8080")),
    })
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
