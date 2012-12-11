class Turtle:
    def __init__(self, x0, y0):
        from math import radians

        self.pos = [x0, y0]
        self.angle = radians(-90)

    def fd(self, dist, path):
        from math import cos, sin

        x = self.pos[0] + dist * cos(self.angle)
        y = self.pos[1] + dist * sin(self.angle)
        if str(type(path)) == "<class 'tkinter.Canvas'>":
            path.create_line(self.pos[0], self.pos[1], x, y)
            path.pack()
        else:
            line = '<line x1="%f" y1="%f" x2="%f" y2="%f" style="stroke:rgb(0,0,255);stroke-width:1"/>\n' % (self.pos[0], self.pos[1], x, y)
            path = ''.join([path, line])
        self.pos = [x, y]

        return path

    def rt(self, angle):
        from math import radians

        self.angle += radians(angle)

    def lt(self, angle):
        from math import radians

        self.angle -= radians(angle)

    def move_to(self, x, y):
        self.pos[0] += x
        self.pos[1] += y


def main():
    l_start = 'F++F++F'
    l_law = {'F': 'F-F++F-F'}
    step = 400
    gen = 5
    angle = 60
    gui(l_start, l_law, step, gen, angle)

    l_start = 'F'
    l_law = {'F': 'F+F-'}
    step = 70
    gen = 10
    angle = 90
    svg(l_start, l_law, step, gen, angle)


def gui(l_start, l_law, step, gen, angle):
    l_finish = l_start
    for i in range(gen):
        l_finish = create_n_generation(l_finish, l_law)
        step /= 3
    tk_drawing_fractal(l_finish, step, angle)


def svg(l_start, l_law, step, gen, angle):
    text = '''<!DOCTYPE html>\n<html>\n<body>\n\n<p><h2>Кривая Леви</h2></p>\n\n'''
    l_finish = l_start
    for i in range(gen):
        text = ''.join([text, '<p><h3>%d поколение</h3></p>\n' % (i + 1)])
        l_finish = create_n_generation(l_finish, l_law)
        step -= (step / 4)
        text = ''.join([text, svg_drawing_fractal(l_finish, step, angle, i)])
    open("svg.html", "w").write(''.join([text, '''</body>\n</html>\n''']))


def create_n_generation(l_finish, l_law):
    l_tmp = ''
    for j in l_finish:
        boo = False
        for k in l_law:
            if j == k:
                l_tmp = ''.join([l_tmp, l_law[k]])
                boo = True
                break
        if not boo:
            l_tmp = ''.join([l_tmp, j])
    l_finish = l_tmp[:]
    return l_finish


def tk_drawing_fractal(l_finish, step, angle):
    from tkinter import Tk, Canvas

    root = Tk()
    root.title('Fractal')
    wid, hei = 500, 500
    canvas = Canvas(root, width=wid, height=hei)
    t = Turtle(wid * 0.9, hei / 4)

    t.lt(90)
    for i in l_finish:
        if i == 'F':
            t.fd(step, canvas)
        elif i == '+':
            t.lt(angle)
        elif i == '-':
            t.rt(angle)

    root.mainloop()


def svg_drawing_fractal(l_finish, step, angle, i):
    wid, hei = 550, 400
    t = Turtle(wid / 2, hei / 2)
    text = '''<svg  width="%dpx" height="%dpx" xmlns="http://www.w3.org/2000/svg" version="1.1">\n\n''' % (wid, hei)

    t.lt(90)
    for i in l_finish:
        if i == 'F':
            text = t.fd(step, text)
        elif i == '+':
            t.lt(angle)
        elif i == '-':
            t.rt(angle)

    return ''.join([text, '\n</svg>\n\n'])


if __name__ == "__main__":
    main()
