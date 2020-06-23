class ChangeAxis():
    def __init__(self,width, height, c_w, c_h, bias_x=0, bias_y=0):
        """picture: 원본 해상도 크기
           want_change: 바꾼 해상도 크기
           bias: 영점 조절정도"""
        self.picture_width = width
        self.picture_height = -height
        self.want_change_width = c_w
        self.want_change_height = c_h
        self.bias_x = bias_x
        self.bias_y = bias_y


    def x_axis(self, input_x):
        """ 해상도 바꾸는 코드"""
        x = (self.picture_width / self.want_change_width)*input_x
        return int(x)


    def y_axis(self, input_y):
        """해상도 바꾸는 코드"""
        y = (self.picture_height / self.want_change_height)*input_y
        return int(y)


    def x(self, input_x):
        """ 이미지 가운데를 영점으로 바꾸는 코드"""
        return int(self.x_axis(input_x) + (self.picture_width / 2)) +\
               self.bias_x


    def y(self, input_y):
        """ 이미지 가운데를 영점으로 바구는 코드"""
        return int(self.y_axis(input_y) - (self.picture_height / 2)) +\
               self.bias_y


    def r_x(self, pic_x):
        """해상도 복원"""
        origin_change_x = pic_x - ((self.picture_width / 2) + self.bias_x)
        input_x = origin_change_x / (self.picture_width / self.want_change_width)
        return int(input_x)


    def r_y(self, pic_y):
        """해상도 복원 코드"""
        origin_change_y = pic_y + (self.picture_height / 2) - self.bias_y
        input_y = origin_change_y / \
                  (self.picture_height / self.want_change_height)
        return int(input_y)                                                    


if __name__ == "__main__":
    ch = ChangeAxis(530,1080,40,100, 695)
    while True:
               x = int(input("input original x:"))
               y = int(input("input original y:"))
               if x > 3000 or y > 3000:
                   break
               print("change x:", ch.r_x(x))
               print("change y:", ch.r_y(y))

        #r_x = int(input("input want to change x:"))
        #r_y = int(input("input want to change y:"))
        #print("original x:", ch.r_x(r_x))
        #print("original y:", ch.r_y(r_y))

