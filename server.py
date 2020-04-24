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
            "color": "#CD681E ",
            "headType": "bwc-scarf",
            "tailType": "bwc-bonhomme"
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        data = cherrypy.request.json
        turn = data["turn"]
        print("")
        print(f"TURN: {turn}")
        snake = Snake(data)
        move = snake.get_next_move()
                # print(data)
        
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

    def all_enemy_heads(self):
        heads = []
        for snake in self.request["board"]["snakes"]:
            if snake["id"] != self.request["you"]["id"]:
                heads.append(snake["body"][0])
        return heads  

    # def all_enemy_bodies(self):
    #     bodies = []
    #     for snake in self.request["board"]["snakes"]:
    #         bodies.append(snake["body"])
    #     return bodies
         
            
        # return [self.request["board"]["snakes"][0]["body"][0]] 

    # def filter(all_heads):
    #  enemies = ['Cylde']
    #  if (all_heads in enemies):
    #    return False
    #  else:
    #    return True

    #  enemy_head = filter(enemies, all_heads)    

    # def opposing_four(enemy_head, move) :
    #     ehead = self.enemy_head(move)
    #     if move == "up":
    #       return {"x": ehead["x"], "y": ehead["y"] - 1}
    #     if move == "down":
    #       return {"x": ehead["x"], "y": ehead["y"] + 1}
    #     if move == "left":
    #       return {"x": ehead["x"] - 1, "y": ehead["y"]}
    #     if move == "right":
    #       return {"x": ehead["x"] + 1, "y": ehead["y"]}

        
    def get_preferred_move_order(self):
      moves = ["right", "down", "left", "up"]
      head = self.get_head_coords()
    
      # # stay in corner
      # head = self.get_head_coords()
      # if head["y"] > self.request["board"]["height"] + 5 :
      #   moves.remove("down")
      #   moves = ["down"] + moves
      # if head ["x"] > self.request["board"]["width"] + 5 :
      #   moves.remove("right")
      #   moves = ["right"] + moves


      # once health hits search for food and sort in distance
      me = self.request["you"]
      if me["health"] < 51 :
        food_distances = [
          (self.distance_to_coords(food_coords), food_coords)
          for food_coords in self.request["board"]["food"]
        ]
        food_distances.sort(key=lambda x: x[0])
        target_coords = food_distances[0][1]
      
      # moves towards food
        if head["x"] < target_coords["x"]:
          moves.remove("right")
          moves = ["right"] + moves
        elif head["x"] > target_coords["x"]:
          moves.remove("left")
          moves = ["left"] + moves

        if head["y"] < target_coords["y"]:
          moves.remove("down")
          moves = ["down"] + moves
        elif head["y"] > target_coords["y"]:
          moves.remove("up")
          moves = ["up"] + moves  

        
      return moves
    
    def is_move_safe(self, move):
      move_coords = self.translate_move_to_coords(move)
      
      if move_coords["x"] < 0 and move_coords["y"] == 0:
        return False
      if move_coords["y"] > self.request["board"]["height"]:
        return False
      if move_coords["x"] > self.request["board"]["width"] :
        return False
      if move_coords["y"] > self.request["board"]["height"] :
        return False

      # Don't move off board

      if move_coords["x"] < 0:
        return False    
      if move_coords["y"] < 0:
        return False
      if move_coords["x"] >= self.request["board"]["width"] :
        return False
      if move_coords["y"] >= self.request["board"]["height"]  :
        return False

     # Don't turn into ourselves

      for body_coords in self.request["you"]["body"][:-1]:
       if self.are_coords_equal(move_coords, body_coords):
         return False

    # don't run into other snakes! 
      for snake in self.request["board"]["snakes"]:
        for body_coords in snake["body"][:-1]:
          if self.are_coords_equal(move_coords, body_coords):
            return False

    # # don't run into other snakes
    #   for enemy_head in self.request["board"]["snakes"][0]: 
    #      if self.are_coords_equal(move_coords, ehead) :
    #       return False
      head = self.get_head_coords()
      for enemy_head in self.all_enemy_heads():
        
        # bottom right
        if move == "right" and enemy_head["x"] == head["x"] + 1 and enemy_head["y"] == head["y"] + 1:
          return False
       
        if move == "down" and enemy_head["x"] == head["x"] + 1 and enemy_head["y"] == head["y"] + 1:  
          return False
       
       
       
       
        # top right
        if move == "right" and enemy_head["x"] == head["x"] + 1 and enemy_head["y"] == head["y"] - 1:
          return False
      

                    
        if move == "up" and enemy_head["x"] == head["x"] + 1 and enemy_head["y"] == head["y"] - 1:  
          return False 
        
         
         
         # top left
        if move == "left" and enemy_head["x"] == head["x"] - 1 and enemy_head["y"] == head["y"] - 1:
          return False
           
 
        if move == "up" and enemy_head["x"] == head["x"] - 1 and enemy_head["y"] == head["y"] - 1:  
          return False 
        

         
         
         # bottom left
        if move == "left" and enemy_head["x"] == head["x"] - 1 and enemy_head["y"] == head["y"] + 1:
          return False
        
  
        if move == "down" and enemy_head["x"] == head["x"] - 1 and enemy_head["y"] == head["y"] + 1:  
          return False
       
        
        
         # directly up
        if move == "up" and enemy_head["x"] == head["x"] and enemy_head["y"] == head["y"] - 2:
          return False
         

        
        
        # directly down
        if move == "down" and enemy_head["x"] == head["x"] and enemy_head["y"] == head["y"] + 2:
          return False
          
    

        
        
        # directly left
        if move == "left" and enemy_head["x"] == head["x"] - 2 and enemy_head["y"] == head["y"]:
          return False    
        

         
         
         # directly right
        if move == "right" and enemy_head["x"] == head["x"] + 2 and enemy_head["y"] == head["y"]:
          return False  
        
 
      
                        
         #don't collide with own head
      for head_coords in snake["body"][:0]:
          if self.are_coords_equal(move_coords, head_coords):
            return False  

       
               
      return True
       
    def translate_move_to_coords(self, move) :     
        head = self.get_head_coords()
        if move == "up":
          return {"x": head["x"], "y": head["y"] - 1}
        if move == "down":
          return {"x": head["x"], "y": head["y"] + 1}
        if move == "left":
          return {"x": head["x"] - 1, "y": head["y"]}
        if move == "right":
          return {"x": head["x"] + 1, "y": head["y"]}

    def are_coords_equal(self, one, two):
      return (one.get("x") == two.get("x") and one.get("y") == two.get("y"))

    def distance_to_coords(self, coords):
      head = self.get_head_coords()
      return abs(head["x"] - coords ["x"]) + abs(head["y"] - coords["y"]) 

    

        
if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({
        "server.socket_port":
        int(os.environ.get("PORT", "8080")),
    })
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
