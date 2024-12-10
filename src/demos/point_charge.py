# 2020/1/12 Morris

# import package
from vpython import canvas, vec

from toolbox.charge import ec, Charge

def main():
    scene = canvas(width=1000, height=600, align='left', range=3E-13)
    charge = Charge(position=vec(0, 0, 0), radius=1.2E-14, coulomb=1 * ec)
    charge.show_field()
    while True:
        pass

if __name__=="__main__":
    main()
