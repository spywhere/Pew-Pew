# class Color:
#   r=0
#   g=0
#   b=0

#   def __init__(r, g, b):
#       self.r=r
#       self.b=b
#       self.g=g

#   def getColor():
#           return '#%02x%02x%02x' % (int(self.r * 255), int(self.g * 255), int(
#                self.b * 255
#            ))


def Color(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)
