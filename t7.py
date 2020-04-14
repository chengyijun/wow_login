
def get_screenxy_from_bmp(main_bmp,son_bmp):
    #获取屏幕上匹配指定截图的坐标->(x,y,width,height)
    from PIL import Image

    img_main=Image.open(main_bmp)
    img_son=Image.open(son_bmp)
    datas_a=list(img_main.getdata())
    datas_b=list(img_son.getdata())
    for i,item in enumerate(datas_a):
        if datas_b[0]==item and datas_a[i+1]==datas_b[1]:
            yx=divmod(i,img_main.size[0])
            main_start_pos=yx[1]+yx[0]*img_main.size[0]

            match_test=True
            for n in range(img_son.size[1]):
                main_pos=main_start_pos+n*img_main.size[0]
                son_pos=n*img_son.size[0]

                if datas_b[son_pos:son_pos+img_son.size[0]] != datas_a[main_pos:main_pos+img_son.size[0]]:
                    match_test=False
                    break
            if match_test:
                return (yx[1],yx[0],yx[1]+img_son.size[0],yx[0]+img_son.size[1])
    return False

print(get_screenxy_from_bmp(u'./images/check.bmp',u'./images/loginbtn.bmp'))
