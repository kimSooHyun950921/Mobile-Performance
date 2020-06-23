class ChangeAxis():
    def __init__(self,width, height, c_w, c_h, bias_x=0, bias_y=0):
        """picture: 원본 해상도 크기
           want_change: 바꾼 해상도 크기
           bias: 영점 조절정도"""
        self.picture_width = width
        self.picture_height = height
        self.want_change_width = c_w
        self.want_change_height = c_h
        self.bias_x = bias_x
        self.bias_y = bias_y


    def x_axis(self, input_x):
        """ 변경된 해상도의 좌표값이 들어갔을때, 
            원래 해상도의 좌표값으로 바꿔주는 코드"""
        x = (self.picture_width / self.want_change_width)*input_x
        return int(x)


    def y_axis(self, input_y):
        """ 변경된 해상도의 좌표값이 들어갔을때, 
            원래 해상도의 좌표값으로 바꿔주는 코드"""
        y = (self.picture_height / self.want_change_height)*input_y
        return int(y)


    def x(self, input_x):
        """ 이미지 가운데를 영점으로 바꾸는 코드"""
        return int(self.x_axis(input_x) + (self.picture_width / 2)) +\
               self.bias_x


    def x_bias(self, input_x):
        """좌표값이 들어왔을때, 좌표의 영점을 바이어스에 따라 조절하는코드"""
        return int(input_x + self.bias_x)


    def y_bias(self, input_y):
        """좌표값이 들어왔을때, 좌표의 영점을 바이어스에 따라 조절하는코드"""
        return int(input_y + self.bias_y)


    def c_x(self, input_x):
        """실제 크기의 해상도가 들어갔을떄, 
        변경된 해상도의 좌표로 변경하는코드"""
        return input_x * self.want_change_width / self.picture_width


    def c_y(self, input_y):
        """실제 크기의 해상도가 들어갔을떄, 
        변경된 해상도의 좌표로 변경하는코드"""
        return input_y * self.want_change_height / self.picture_height

        
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
#    ch = ChangeAxis(1280,720,40,100)
#    ch = ChangeAxis(1920, 1080, 2960, 1440)
    ch = ChangeAxis(1440, 2960, 530, 1080, 695)
    while True:
        x = int(input("input original x:"))
        y = int(input("input original y:"))
        if x > 3000 or y > 3000:
            break
        print("change x:", ch.x_bias(ch.c_x(x)))
        print("change y:", ch.y_bias(ch.c_y(y)))

        #r_x = int(input("input want to change x:"))
        #r_y = int(input("input want to change y:"))
        #print("original x:", ch.r_x(x))
        #print("original y:", ch.r_y(y))

